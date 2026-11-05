"""A `koncepcio/sablonok/` mintái: katalógus, szétbontás, letölthető csomag.

A katalógus a `sablonok/README.md` táblájából épül, így a dokumentum az egyetlen forrás:
új minta felvétele = egy fájl és egy sor a táblában.
"""

import io
import re
import zipfile
from dataclasses import dataclass
from datetime import date

from hibrid_app import config

README = config.SABLONOK_DIR / "README.md"
UTMUTATO_FEJLEC = "## Kitöltési útmutató"

_SOR = re.compile(r"^\|\s*\[([^\]]+)\]\(([^)]+\.md)\)\s*\|(.*)\|\s*$")


# Melyik üres mintához melyik kitöltött példa tartozik (repó-relatív útak). A mérőszámkártya
# kitöltött változata a mérési rendszer dokumentumában él, a többié a `xyo-mintak/` mappában.
KITOLTOTT = {
    "meroszamkartya.md": ("koncepcio/02-meresi-rendszer.md",),
    "celkartya.md": ("koncepcio/xyo-mintak/celkartyak.md",),
    "kapudontes.md": ("koncepcio/xyo-mintak/kapudontesek.md",),
    "adatleltar.md": ("koncepcio/xyo-mintak/adatleltar.md",),
    "ai-act-besorolasi-lap.md": ("koncepcio/xyo-mintak/ai-act-besorolasi-lap.md",),
}


@dataclass(frozen=True)
class Minta:
    cim: str
    fajl: str  # a sablonok/ mappán belüli fájlnév
    mire: str
    mikor: str
    kapu: str
    ki: str

    @property
    def kitoltott(self) -> tuple[str, ...]:
        """A kitöltött példa(k) repó-relatív útja; üres, ha nincs."""
        return KITOLTOTT.get(self.fajl, ())

    def szoveg(self) -> str:
        return (config.SABLONOK_DIR / self.fajl).read_text(encoding="utf-8")

    def bajtok(self) -> bytes:
        """A fájl pontos tartalma, ahogy a repóban áll (a letöltés ezt adja)."""
        return (config.SABLONOK_DIR / self.fajl).read_bytes()


def katalogus() -> list[Minta]:
    """A README „A mintak” táblájának sorai, a táblabeli sorrendben."""
    mintak = []
    for sor in README.read_text(encoding="utf-8").splitlines():
        m = _SOR.match(sor)
        if not m:
            continue
        mezok = [c.strip() for c in m.group(3).split("|")]
        if len(mezok) != 4:
            raise ValueError(f"A README-tábla sora nem 5 oszlopos: {sor!r}")
        mintak.append(Minta(m.group(1), m.group(2), *mezok))
    return mintak


def szakasz(szoveg: str, fejlec: str) -> str:
    """A `## fejlec` szakasz törzse a következő `## ` fejlécig (vagy a végéig); üres, ha nincs ilyen."""
    m = re.search(rf"^## {re.escape(fejlec)}\s*$(.*?)(?=^## |\Z)", szoveg, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() + "\n" if m else ""


def hasznalati_szabalyok() -> str:
    """A README „Hogyan használd jól” szakasza."""
    return szakasz(README.read_text(encoding="utf-8"), "Hogyan használd jól")


def szetbont(szoveg: str) -> tuple[str, str]:
    """(a minta, a kitöltési útmutató): a „## Kitöltési útmutató” fejlécnél vágva.

    A minta a fájl elejétől az útmutató fejléce elé, az útmutató a fejléctől a végéig tart.
    Ha nincs útmutató-fejléc, az útmutató üres.
    """
    ele, fejlec, utana = szoveg.partition("\n" + UTMUTATO_FEJLEC)
    if not fejlec:
        return szoveg, ""
    return ele.rstrip() + "\n", UTMUTATO_FEJLEC + utana


def lefokoz(szoveg: str, szintek: int = 2) -> str:
    """A markdown-címsorokat `szintek` szinttel lejjebb viszi (legfeljebb hatodik szintig);
    a kódblokkokon belül nem nyúl a sorokhoz. Így a kártyába ágyazott minta címsorai nem
    nagyobbak a kártya saját címénél."""
    kimenet, kodblokkban = [], False
    for sor in szoveg.splitlines():
        if sor.startswith("```"):
            kodblokkban = not kodblokkban
        elif not kodblokkban and (m := re.match(r"^(#{1,6}) ", sor)):
            sor = "#" * min(len(m.group(1)) + szintek, 6) + sor[len(m.group(1)) :]
        kimenet.append(sor)
    return "\n".join(kimenet) + "\n"


def torzs(szoveg: str) -> str:
    """A minta szövege az első `# Cím` sor nélkül (a címet a kártya mutatja)."""
    sorok = szoveg.splitlines()
    if sorok and sorok[0].startswith("# "):
        sorok = sorok[1:]
    return "\n".join(sorok).lstrip("\n") + "\n"


def csomag(mintak: list[Minta] | None = None) -> bytes:
    """Zip: a mintak és a README a `sablonok/` mappában (a README relatív linkjei így élnek), meg egy
    OLVASSEL.txt a tartalommal. A fájlok bájtra azonosak a repóbeliekkel."""
    mintak = katalogus() if mintak is None else mintak
    puffer = io.BytesIO()
    with zipfile.ZipFile(puffer, "w", zipfile.ZIP_DEFLATED) as arch:
        arch.writestr("sablonok/README.md", README.read_bytes())
        for m in mintak:
            arch.writestr(f"sablonok/{m.fajl}", m.bajtok())
        sorok = [
            "Hibrid PM — üres mintak (Xyo Tudásasszisztens példa)",
            f"Készült: {date.today().isoformat()}",
            "",
            "Tartalom (sablonok/ mappa):",
            "  README.md  —  a mintak listája és a használati szabályok",
            *(f"  {m.fajl}  —  {m.cim}: {m.mire}" for m in mintak),
            "",
            "Minden minta három részből áll: használat, a minta, kitöltési útmutató.",
            "A kitöltött példákra mutató linkek a teljes repóra vonatkoznak, a mappán kívül nem élnek.",
        ]
        arch.writestr("OLVASSEL.txt", "\n".join(sorok) + "\n")
    return puffer.getvalue()
