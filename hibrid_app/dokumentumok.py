"""A kutatás és a koncepció dokumentumai a felületen: regiszter és hivatkozás-feloldás.

Minden dokumentum saját oldal (`st.Page`), saját útvonallal. A dokumentumok relatív
markdown-linkjeit (`../kutatas/04-szabalyozas.md`, `tudasbazis.md#dpia`, `sablonok/`) a
`feloldas` fordítja a felület relatív URL-jeire (a tudásbázis szócikkei `?szocikk=` paraméterrel). Az útvonalak **relatívak** (nincs vezető `/`),
hogy egy később választott alapútvonal (pl. `/hibrid/`) alatt is működjenek.
"""

import posixpath
import re
from dataclasses import dataclass
from urllib.parse import quote

from hibrid_app import config, mintatar

KUTATAS = "Kutatás"
KONCEPCIO = "Koncepció"
XYO_MINTAK = "Xyo-minták"
TUDASBAZIS_FAJL = "kutatas/tudasbazis.md"  # saját oldala van
SABLONOK_MAPPA = "koncepcio/sablonok"
XYO_MINTAK_MAPPA = "koncepcio/xyo-mintak"
FOGLALT_UTAK = {"tudasbazis", "mintatar", "g1-kapu"}  # a többi oldal útvonala

_KULSO = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")  # http:, https:, mailto: …


@dataclass(frozen=True)
class Dokumentum:
    rel: str  # a repó gyökeréhez viszonyítva: "kutatas/01-hibrid-a-piacon.md"
    cim: str  # a fájl első `# ` sora
    szekcio: str
    url: str  # az oldal útvonala

    def szoveg(self) -> str:
        return (config.ROOT / self.rel).read_text(encoding="utf-8")


def _cim(szoveg: str, tartalek: str) -> str:
    return next((s[2:].strip() for s in szoveg.splitlines() if s.startswith("# ")), tartalek)


def _url(rel: str) -> str:
    stem = posixpath.splitext(posixpath.basename(rel))[0]
    return "koncepcio" if rel == "koncepcio/README.md" else stem


def _gyujt(mappa, szekcio: str, kizar: set[str]) -> list[Dokumentum]:
    fajlok = sorted(
        (p for p in mappa.glob("*.md") if p.relative_to(config.ROOT).as_posix() not in kizar),
        key=lambda p: (p.name != "README.md", p.name),  # a README elöl, a többi névsorban
    )
    docs = []
    for p in fajlok:
        rel = p.relative_to(config.ROOT).as_posix()
        docs.append(Dokumentum(rel, _cim(p.read_text(encoding="utf-8"), p.stem), szekcio, _url(rel)))
    return docs


def lista() -> list[Dokumentum]:
    """Kutatás, koncepció, majd a kitöltött Xyo-minták; a tudásbázis és az üres sablonok saját oldalon vannak."""
    return (
        _gyujt(config.KUTATAS_DIR, KUTATAS, {TUDASBAZIS_FAJL})
        + _gyujt(config.KONCEPCIO_DIR, KONCEPCIO, set())
        + _gyujt(config.XYO_MINTAK_DIR, XYO_MINTAK, set())
    )


def feloldas(forras: str, href: str) -> str | None:
    """A `forras` (repó-relatív fájl) markdown-linkjének (`href`) célja a felületen: relatív URL,
    vagy `None`, ha külső, dokumentumon belüli (`#…`) vagy nem a felületen élő cél."""
    if _KULSO.match(href):
        return None
    ut, _, torzs = href.partition("#")
    if not ut:  # üres link vagy dokumentumon belüli `#horgony`
        return None
    cel = posixpath.normpath(posixpath.join(posixpath.dirname(forras), ut))
    horgony = f"#{torzs}" if torzs else ""

    if cel == TUDASBAZIS_FAJL:
        # Hosszú oldalon a betöltéskori #horgony-ugrás pontatlan (az oldal még nő), ezért a szócikk
        # query-paraméterrel jön: az oldal kiemelve, felül mutatja.
        return f"tudasbazis?szocikk={quote(torzs)}" if torzs else "tudasbazis"
    if cel == SABLONOK_MAPPA or cel == f"{SABLONOK_MAPPA}/README.md":
        return "mintatar"
    if posixpath.dirname(cel) == SABLONOK_MAPPA:
        fajl = posixpath.basename(cel)
        if any(m.fajl == fajl for m in mintatar.katalogus()):
            return "mintatar#" + (torzs or fajl.removesuffix(".md"))
        return None
    return next((d.url + horgony for d in lista() if d.rel == cel), None)
