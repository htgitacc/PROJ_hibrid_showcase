"""A `kutatas/tudasbazis.md` beolvasása és kereshetővé tétele.

A fájl szerkezete: `## Kategória` → `### Szócikk` → mezők soronként (`**Mit jelent:** …`).
A mezők sorrendjét és a szócikkek betűrendjét a fájl adja, ez a modul csak olvas.
"""

import html
import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from hibrid_app import config

FAJL = config.KUTATAS_DIR / "tudasbazis.md"
FAJL_REL = "kutatas/tudasbazis.md"  # repó-relatív, a hivatkozások feloldásához

_FEJEZET = re.compile(r"^## (.+)$")
_SZOCIKK = re.compile(r"^### (.+)$")
_MEZO = re.compile(r"^\*\*([^:*]+):\*\*\s*(.*)$")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]*)\)")
_KULSO_LINK = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")  # http:, https:, mailto: …


@dataclass(frozen=True)
class Szocikk:
    kategoria: str
    cim: str
    horgony: str
    mezok: tuple[tuple[str, str], ...]  # (mező neve, szöveg), a fájlbeli sorrendben

    def mezo(self, nev: str) -> str:
        return next((szoveg for n, szoveg in self.mezok if n == nev), "")


def horgony(cim: str) -> str:
    """A szócikk horgonya, ugyanúgy, ahogy a dokumentumok linkjei (és a `tools/ellenorzes.py`) képezik."""
    return re.sub(r"[^\w -]", "", cim.lower()).replace(" ", "-")


def olvas(szoveg: str) -> list[Szocikk]:
    """A markdown szövegből a szócikkek, fájlbeli sorrendben. A szócikk nélküli fejezetek kimaradnak."""
    szocikkek: list[Szocikk] = []
    kategoria = cim = None
    mezok: list[list[str]] = []

    def lezar():
        if cim is not None and mezok:
            # a sorvégi `\` a fájlban kemény sortörés; a megjelenítésben felesleges
            szocikkek.append(Szocikk(kategoria, cim, horgony(cim), tuple((n, t.rstrip("\\").rstrip()) for n, t in mezok)))

    for sor in szoveg.splitlines():
        if m := _FEJEZET.match(sor):
            lezar()
            kategoria, cim, mezok = m.group(1).strip(), None, []
        elif m := _SZOCIKK.match(sor):
            lezar()
            cim, mezok = m.group(1).strip(), []
        elif cim is None:
            continue
        elif m := _MEZO.match(sor):
            mezok.append([m.group(1).strip(), m.group(2)])
        elif sor.strip() and mezok:  # több soros mező folytatása
            mezok[-1][1] += " " + sor.strip()
    lezar()
    return szocikkek


def betolt(fajl: Path = FAJL) -> list[Szocikk]:
    return olvas(fajl.read_text(encoding="utf-8"))


def kategoriak(szocikkek: list[Szocikk]) -> list[str]:
    """A kategóriák a fájlbeli sorrendben."""
    return list(dict.fromkeys(s.kategoria for s in szocikkek))


def _egyszerusit(szoveg: str) -> str:
    """Kis- és nagybetűtől, ékezettől független összevetéshez: „Félreolvasás” = „felreolvasas”."""
    alap = unicodedata.normalize("NFKD", szoveg.casefold())
    return "".join(c for c in alap if not unicodedata.combining(c))


def keres(szocikkek: list[Szocikk], szoveg: str = "", kategoria: str | None = None) -> list[Szocikk]:
    """Szűrés kategóriára és szövegre. A szöveg minden szavának szerepelnie kell a szócikkben
    (címben vagy bármelyik mezőben); a találatok a fájlbeli sorrendben maradnak."""
    szavak = _egyszerusit(szoveg).split()
    talalatok = []
    for s in szocikkek:
        if kategoria and s.kategoria != kategoria:
            continue
        teljes = _egyszerusit(" ".join([s.cim, *(t for _, t in s.mezok)]))
        if all(szo in teljes for szo in szavak):
            talalatok.append(s)
    return talalatok


def linkek_atirasa(
    szoveg: str,
    lathato: set[str] | None,
    dokumentum_url: Callable[[str], str | None] = lambda hivatkozas: None,
) -> str:
    """A szövegben a hivatkozások átírása a felületre.

    * `#horgony`: link marad, ha a szócikk látszik (`lathato`); különben sima szöveg (nem mutat
      sehova). `lathato=None`: minden `#horgony` link marad (dokumentumoldalakon);
    * külső link (`https:`, `mailto:` …): változatlan;
    * másik oldalra mutató link: a `dokumentum_url` adja a relatív URL-t, és `<a target="_self">`
      lesz belőle (a sima markdown-link új lapot nyitna); a szöveget `unsafe_allow_html=True`-val
      kell megjeleníteni. Ha az URL `None`, a link neve mellé kerül a fájlnév.
    """

    def csere(m: re.Match) -> str:
        nev, cel = m.group(1), m.group(2)
        if _KULSO_LINK.match(cel):
            return m.group(0)  # külső link: marad markdown-link (új lapot nyit, ahogy kell)
        if cel.startswith("#"):
            return m.group(0) if lathato is None or cel[1:] in lathato else nev
        url = dokumentum_url(cel)
        if url:
            return f'<a href="{html.escape(url, quote=True)}" target="_self">{nev}</a>'
        return f"{nev} (`{cel.split('#')[0]}`)"

    return _LINK.sub(csere, szoveg)
