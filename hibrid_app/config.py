"""Központi útvonalak és konstansok."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

APP_TITLE = "Hibrid PM — AI-projekt"
KUTATAS_DIR = ROOT / "kutatas"
KONCEPCIO_DIR = ROOT / "koncepcio"
SABLONOK_DIR = KONCEPCIO_DIR / "sablonok"
XYO_MINTAK_DIR = KONCEPCIO_DIR / "xyo-mintak"

KESKENY_PX = 700  # ennél keskenyebb képernyőn érvényes a szűk képernyős elrendezés (táblázatok, ábrák)
