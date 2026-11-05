"""A Mermaid → DOT átalakító: a valódi ábra, szintetikus minták és a támogatott részhalmaz határai."""

import re

import pytest

from hibrid_app import mermaid as mm
from tests.conftest import ROOT

ABRAK = {
    p.relative_to(ROOT).as_posix(): re.findall(r"```mermaid\n(.*?)```", p.read_text(encoding="utf-8"), re.DOTALL)
    for p in [*ROOT.glob("kutatas/*.md"), *ROOT.glob("koncepcio/**/*.md")]
}
ABRAK = {k: v for k, v in ABRAK.items() if v}
MODELL = ABRAK["koncepcio/00-mukodesi-modell.md"][0]


# --- a valódi ábra -------------------------------------------------------------------------


def test_minden_dokumentumabra_tamogatott():
    """Ha egy dokumentumba nem támogatott ábra kerül, a teszt jelzi (a nézet kódblokkra esne vissza)."""
    assert ABRAK  # van legalább egy ábra
    for abrak in ABRAK.values():
        for forras in abrak:
            mm.dot(forras)  # nem dob hibát


def test_a_modell_abraja_csomopontjai():
    a = mm.olvas(MODELL)
    assert a.irany == "LR"
    assert {k: (c.alak, c.alcsoport) for k, c in a.csomopontok.items()} == {
        "K1": ("teglalap", "K"), "G0": ("hatszog", None), "M0": ("teglalap", "M"), "M1": ("teglalap", "M"),
        "G1": ("hatszog", None), "B1": ("teglalap", "B"), "T1": ("teglalap", "T"), "Z": ("teglalap", None),
    }  # fmt: skip
    assert a.alcsoportok == {
        "K": "KERET — prediktív", "M": "KÍSÉRLETI SZAKASZ — időkeretes",
        "B": "BEVEZETÉSI ÁG — prediktív", "T": "TERMÉKÁG — agilis",
    }  # fmt: skip
    assert a.csomopontok["G1"].felirat == "G1 — PoC-kapu\ngo · pivot · no-go"


def test_a_modell_abraja_elei():
    a = mm.olvas(MODELL)
    assert {(e.forras, e.cel, e.felirat) for e in a.elek} == {
        ("K1", "G0", None), ("G0", "M0", None), ("M0", "M1", None), ("M1", "G1", None),
        ("G1", "B1", "go"), ("G1", "T1", "go"), ("G1", "M1", "pivot"), ("G1", "Z", "no-go"),
        ("T1", "B1", "kiadott verzió"), ("B1", "T1", "visszajelzés, hibák"), ("B1", "Z", None),
    }  # fmt: skip
    assert len(a.elek) == 11  # a halmaz nem nyel el duplikátumot


def test_a_modell_dotja_teljes():
    d = mm.dot(MODELL)
    assert d.startswith("digraph {") and d.rstrip().endswith("}")
    assert d.count("{") == d.count("}")
    assert d.count("subgraph cluster_") == 4
    for azonosito in ("K1", "G0", "M0", "M1", "G1", "B1", "T1", "Z"):
        assert len(re.findall(rf"^\s+{azonosito} \[label=", d, re.MULTILINE)) == 1  # pontosan egyszer definiált
    assert d.count(" -> ") == 11
    assert 'G1 -> M1 [label="pivot"];' in d
    assert 'G1 [label="G1 — PoC-kapu\\ngo · pivot · no-go", shape=hexagon' in d
    assert 'label="KÍSÉRLETI SZAKASZ — időkeretes"' in d


# --- az irány felülbírálása és a szembeni élpárok -------------------------------------------


def test_a_szembeni_feliratos_elpar_masodik_tagja_kulon_portot_kap():
    d = mm.dot(MODELL)
    assert 'T1 -> B1 [label="kiadott verzió"];' in d  # az első tag port nélkül
    assert 'B1 -> T1 [tailport=e, headport=e, label="visszajelzés, hibák"];' in d


@pytest.mark.parametrize(("irany", "port"), [("LR", "e"), ("RL", "w"), ("TB", "s"), ("BT", "n")])
def test_a_port_az_aramlasi_iranyhoz_igazodik(irany, port):
    forras = MODELL.replace("flowchart LR", f"flowchart {irany}")
    d = mm.dot(forras)
    assert f"rankdir={irany};" in d
    assert f'B1 -> T1 [tailport={port}, headport={port}, label="visszajelzés, hibák"];' in d


def test_a_td_irany_tb_nek_felel_meg():
    d = mm.dot(MODELL.replace("flowchart LR", "flowchart TD"))
    assert "rankdir=TB;" in d and "tailport=s, headport=s" in d


def test_az_elpar_csak_ket_felirat_eseten_kap_portot():
    felirat_nelkul = "flowchart LR\nA --> B\nB --> A\n"
    egyik_feliratos = "flowchart LR\nA -- x --> B\nB --> A\n"
    masik_feliratos = "flowchart LR\nA --> B\nB -- y --> A\n"
    for forras in (felirat_nelkul, egyik_feliratos, masik_feliratos):
        assert "port=" not in mm.dot(forras)
    mindketto = mm.dot("flowchart LR\nA -- x --> B\nB -- y --> A\n")
    assert mindketto.count("tailport=") == 1
    assert "B -> A [tailport=e, headport=e, label=\"y\"];" in mindketto


def test_a_modell_tobbi_elepar_nem_kap_portot():
    """A G1 ↔ M1 pár (csak az egyik feliratos) és minden más él port nélkül marad."""
    assert mm.dot(MODELL).count("port=") == 2  # tailport + headport, egyetlen élen


def test_a_terkoz_beallitasok_rogzitettek():
    """Szemmel választott értékek (a felirat-ütközések ezzel tűntek el): ne változzanak csendben."""
    assert 'bgcolor="transparent"; nodesep=0.6; ranksep=1.0;' in mm.dot(MODELL)


def test_a_fürtcimkek_balra_igazitottak():
    assert mm.dot(MODELL).count('labeljust="l"') == 4


# --- szintetikus minták --------------------------------------------------------------------


def test_lanc_es_iranyok():
    a = mm.olvas("flowchart TD\n A --> B --> C\n")
    assert a.irany == "TB"
    assert [(e.forras, e.cel) for e in a.elek] == [("A", "B"), ("B", "C")]
    assert mm.olvas("graph RL\nA --> B").irany == "RL"
    assert mm.olvas("flowchart BT\nA --> B").irany == "BT"


@pytest.mark.parametrize(
    ("sor", "felirat"),
    [
        ("A -- go --> B", "go"),
        ('A -- "kiadott verzió" --> B', "kiadott verzió"),
        ("A -- visszajelzés, hibák --> B", "visszajelzés, hibák"),
        ("A -- no-go --> B", "no-go"),
        ('A -- "idézett -- kötőjelekkel" --> B', "idézett -- kötőjelekkel"),
    ],
)
def test_elfeliratok(sor, felirat):
    a = mm.olvas(f"flowchart LR\n{sor}")
    assert [(e.forras, e.cel, e.felirat) for e in a.elek] == [("A", "B", felirat)]


def test_az_irany_atkerul_a_dotba():
    assert "rankdir=TB;" in mm.dot("flowchart TD\nA --> B")
    assert "rankdir=RL;" in mm.dot("flowchart RL\nA --> B")
    assert "rankdir=LR;" in mm.dot("flowchart LR\nA --> B")


def test_br_sortores():
    a = mm.olvas('flowchart LR\nA["egy<br/>kettő<br>három"]')
    assert a.csomopontok["A"].felirat == "egy\nkettő\nhárom"


def test_csomopont_felirata_az_elso_definiciotol_ervenyes_es_frissul():
    a = mm.olvas('flowchart LR\nA --> B\nA["Alfa"]\nB{{"Béta"}}\n')
    assert (a.csomopontok["A"].felirat, a.csomopontok["A"].alak) == ("Alfa", "teglalap")
    assert (a.csomopontok["B"].felirat, a.csomopontok["B"].alak) == ("Béta", "hatszog")


def test_jelolo_nelkuli_csomopont_felirata_az_azonositoja():
    assert mm.olvas("flowchart LR\nX --> Y").csomopontok["X"].felirat == "X"


def test_alcsoport_felirat_nelkul():
    a = mm.olvas('flowchart LR\nsubgraph S\n A["a"]\nend\n')
    assert a.alcsoportok == {"S": "S"} and a.csomopontok["A"].alcsoport == "S"


def test_alcsoportba_eso_csomopont_marad_ott_ha_kivul_hivatkozzak():
    a = mm.olvas('flowchart LR\nsubgraph S\n A["a"]\nend\nA --> B\n')
    assert a.csomopontok["A"].alcsoport == "S" and a.csomopontok["B"].alcsoport is None


def test_dot_escape():
    """A DOT idézőjeles szövegében a \\ és a " escape-elt, a sortörés \\n."""
    assert mm._dot_szoveg('a "b" c\\d\ne') == '"a \\"b\\" c\\\\d\\ne"'
    d = mm.dot('flowchart LR\nA["perjel \\ itt"]')
    assert 'label="perjel \\\\ itt"' in d


# --- a támogatott részhalmaz határai: minden más hibát ad ---------------------------------


@pytest.mark.parametrize(
    "forras",
    [
        "",
        "A --> B",  # nincs fejléc
        "sequenceDiagram\nA->>B: hi",
        "flowchart LR\nA --- B",  # nem nyíl
        "flowchart LR\nA -.-> B",
        "flowchart LR\nA ==> B",
        "flowchart LR\nA --> ",  # hiányzó cél
        "flowchart LR\nA[\"x\"] --> B[nem idézett]",
        "flowchart LR\nclassDef x fill:#f00",
        "flowchart LR\nsubgraph S\nsubgraph T\nend\nend",  # beágyazott
        "flowchart LR\nsubgraph S\nsubgraph T\nA\nend",  # beágyazott, egyetlen end-del
        "flowchart LR\nA --go --> B",  # a „--” után szóköz kell (szigorú szintaxis)
        "flowchart LR\nend",  # nyitott alcsoport nélkül
        "flowchart LR\nsubgraph S\nA --> B",  # lezáratlan
        "flowchart LR\nA --> B %% megjegyzés",
    ],
)
def test_nem_tamogatott_forras_hibat_ad(forras):
    with pytest.raises(ValueError, match="Nem támogatott ábra"):
        mm.dot(forras)
