"""A dokumentumokban használt Mermaid-folyamatábrák átalakítása Graphviz DOT-tá.

A Streamlit nem rajzol Mermaid-ot, a `st.graphviz_chart` viszont külső forrás nélkül (a frontend
része) kirajzolja a DOT-ot. Az átalakító **szándékosan szűk**: csak azt a részhalmazt érti, amit a
dokumentumok használnak, és minden mást `ValueError`-ral jelez. Ilyenkor a nézet a forráskódot
mutatja, így egy új szintaxis nem tör el oldalt, csak egyszerűbben jelenik meg.

Támogatott: `flowchart LR|RL|TB|TD|BT` (vagy `graph`), `subgraph ID["felirat"]` … `end`,
csomópontok `ID["felirat"]` (téglalap) és `ID{{"felirat"}}` (hatszög), élek láncokban
(`A --> B --> C`), élfelirattal (`A -- szöveg --> B`, `A -- "szöveg" --> B`), `<br/>` sortörés.
"""

import re
from dataclasses import dataclass, field

from hibrid_app import szinek

_FEJLEC = re.compile(r"^(?:flowchart|graph)\s+(LR|RL|TB|TD|BT)\s*$")
_ALCSOPORT = re.compile(r'^subgraph\s+(\w+)(?:\["([^"]*)"\])?\s*$')
_CSOMOPONT = re.compile(r'(\w+)(?:\["([^"]*)"\]|\{\{"([^"]*)"\}\})?')
_EL = re.compile(r'\s*(?:-->|--\s+(?:"(?P<idezett>[^"]*)"|(?P<sima>[^"\s](?:[^"]*?[^"\s])?))\s+-->)\s*')
_IRANY = {"LR": "LR", "RL": "RL", "TB": "TB", "TD": "TB", "BT": "BT"}


@dataclass
class Csomopont:
    azonosito: str
    felirat: str
    alak: str = "teglalap"  # vagy "hatszog"
    alcsoport: str | None = None


@dataclass
class El:
    forras: str
    cel: str
    felirat: str | None = None


@dataclass
class Abra:
    irany: str
    csomopontok: dict[str, Csomopont] = field(default_factory=dict)
    elek: list[El] = field(default_factory=list)
    alcsoportok: dict[str, str] = field(default_factory=dict)  # azonosító → felirat


def _felirat(szoveg: str) -> str:
    """`<br/>` → sortörés; a többi karaktert változatlanul hagyja."""
    return re.sub(r"<br\s*/?>", "\n", szoveg)


def olvas(forras: str) -> Abra:
    """A Mermaid-forrásból szerkezet; nem támogatott sornál `ValueError`."""
    sorok = [s.strip() for s in forras.strip().splitlines() if s.strip()]
    if not sorok or not (m := _FEJLEC.match(sorok[0])):
        raise ValueError("Nem támogatott ábra: hiányzik a „flowchart LR” jellegű fejléc.")
    abra = Abra(_IRANY[m.group(1)])
    nyitott: str | None = None  # az éppen nyitott alcsoport

    def csomopont(m: re.Match) -> str:
        azonosito, teglalap, hatszog = m.group(1), m.group(2), m.group(3)
        if azonosito not in abra.csomopontok:
            abra.csomopontok[azonosito] = Csomopont(azonosito, azonosito, alcsoport=nyitott)
        cs = abra.csomopontok[azonosito]
        if teglalap is not None:
            cs.felirat = _felirat(teglalap)
        elif hatszog is not None:
            cs.felirat, cs.alak = _felirat(hatszog), "hatszog"
        return azonosito

    for sor in sorok[1:]:
        if m := _ALCSOPORT.match(sor):
            if nyitott is not None:
                raise ValueError("Nem támogatott ábra: beágyazott alcsoport.")
            nyitott = m.group(1)
            abra.alcsoportok[nyitott] = _felirat(m.group(2) or nyitott)
            continue
        if sor == "end":
            if nyitott is None:
                raise ValueError("Nem támogatott ábra: `end` nyitott alcsoport nélkül.")
            nyitott = None
            continue
        # csomópont-lánc: CS (él CS)*
        poz = 0
        m = _CSOMOPONT.match(sor, poz)
        if not m:
            raise ValueError(f"Nem támogatott ábra, ismeretlen sor: {sor!r}")
        elozo, poz = csomopont(m), m.end()
        while poz < len(sor):
            el = _EL.match(sor, poz)
            if not el:
                raise ValueError(f"Nem támogatott ábra, ismeretlen sor: {sor!r}")
            felirat = el.group("idezett") if el.group("idezett") is not None else el.group("sima")
            m = _CSOMOPONT.match(sor, el.end())
            if not m:
                raise ValueError(f"Nem támogatott ábra, ismeretlen sor: {sor!r}")
            kovetkezo = csomopont(m)
            abra.elek.append(El(elozo, kovetkezo, _felirat(felirat) if felirat is not None else None))
            elozo, poz = kovetkezo, m.end()
    if nyitott is not None:
        raise ValueError("Nem támogatott ábra: lezáratlan alcsoport.")
    return abra


def _dot_szoveg(szoveg: str) -> str:
    """DOT idézőjeles szöveg: \\ és " escape-elve, a sortörés `\\n`."""
    return '"' + szoveg.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


# Az áramlási irányba néző oldal (a szembeni él ide kerül, hogy ne essen egybe az oda-éllel)
_ELOLDAL = {"LR": "e", "RL": "w", "TB": "s", "BT": "n"}


def dot(forras: str) -> str:
    """Graphviz DOT a Mermaid-forrásból (`ValueError`, ha az ábra nem támogatott).

    Az egymással szembeni élpár (A→B és B→A) második tagját külön portra kötjük, **ha mindkettő
    feliratos**: különben az Graphviz egyetlen kétfejű nyílként egymásra rajzolná őket, és a két
    felirat ugyanarra a helyre kerülne.
    """
    abra = olvas(forras)
    sorok = [
        "digraph {",
        f"  rankdir={abra.irany};",
        '  bgcolor="transparent"; nodesep=0.6; ranksep=1.0;',
        (
            f'  node [shape=box, style="rounded,filled", fillcolor="{szinek.ABRA_CSOMOPONT}", '
            f'color="{szinek.KIEMELES}", fontcolor="{szinek.SZOVEG}", fontsize=11, penwidth=1.2];'
        ),
        f'  edge [color="{szinek.ABRA_EL}", fontcolor="{szinek.SZOVEG}", fontsize=10, penwidth=1.2];',
    ]
    for azonosito, felirat in abra.alcsoportok.items():
        sorok.append(f"  subgraph cluster_{azonosito} {{")
        sorok.append(
            f'    label={_dot_szoveg(felirat)}; labeljust="l"; style="rounded"; color="{szinek.KIEMELES}"; '
            f'fontcolor="{szinek.KIEMELES}"; fontsize=12;'
        )
        for cs in abra.csomopontok.values():
            if cs.alcsoport == azonosito:
                sorok.append(f"    {_csomopont_dot(cs)}")
        sorok.append("  }")
    for cs in abra.csomopontok.values():
        if cs.alcsoport is None:
            sorok.append(f"  {_csomopont_dot(cs)}")
    feliratos = {(e.forras, e.cel) for e in abra.elek if e.felirat}
    korabbi: set[tuple[str, str]] = set()
    for el in abra.elek:
        attributumok = []
        if (el.cel, el.forras) in korabbi and (el.cel, el.forras) in feliratos and el.felirat:
            port = _ELOLDAL[abra.irany]
            attributumok += [f"tailport={port}", f"headport={port}"]
        if el.felirat:
            attributumok.append(f"label={_dot_szoveg(el.felirat)}")
        korabbi.add((el.forras, el.cel))
        sorok.append(f"  {el.forras} -> {el.cel}" + (f" [{', '.join(attributumok)}]" if attributumok else "") + ";")
    sorok.append("}")
    return "\n".join(sorok) + "\n"


def _csomopont_dot(cs: Csomopont) -> str:
    alak = f', shape=hexagon, fillcolor="{szinek.ABRA_KIEMELT}"' if cs.alak == "hatszog" else ""
    return f"{cs.azonosito} [label={_dot_szoveg(cs.felirat)}{alak}];"
