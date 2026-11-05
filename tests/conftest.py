"""Közös tesztsegédek: útvonal és a Streamlit-zaj elnémítása."""

import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# A Streamlit cache futtatókörnyezet nélkül figyelmeztet — a tesztekben ez zaj.
logging.getLogger("streamlit").setLevel(logging.ERROR)


def olvas(rel_path: str) -> str:
    """Egy repó-relatív szövegfájl tartalma (a dokumentumok olvasásához)."""
    return (ROOT / rel_path).read_text(encoding="utf-8")


def tabla(szoveg: str, horgony: str) -> list[list[str]]:
    """A `horgony` szöveget tartalmazó sor utáni első markdown-tábla sorai.

    A fejléc- és az elválasztó sor kimarad; a cellák szóközmentesek, a `*` kiemelések nélkül.
    """
    sorok = szoveg.splitlines()
    kezdet = next(i for i, s in enumerate(sorok) if horgony in s)
    i = next(j for j in range(kezdet, len(sorok)) if sorok[j].startswith("|"))
    eredmeny = []
    while i < len(sorok) and sorok[i].startswith("|"):
        cellak = [c.strip().replace("*", "") for c in sorok[i].strip().strip("|").split("|")]
        if not set("".join(cellak)) <= set("-: "):  # az elválasztó sor kimarad
            eredmeny.append(cellak)
        i += 1
    return eredmeny[1:]  # a fejléc kimarad


def sor(tablasorok: list[list[str]], elotag: str) -> list[str]:
    """Az a sor, amelynek első cellája az `elotag`-gal kezdődik (pontosan egy lehet)."""
    talalat = [s for s in tablasorok if s[0].startswith(elotag)]
    assert len(talalat) == 1, f"{elotag!r}: {len(talalat)} találat"
    return talalat[0]
