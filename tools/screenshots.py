"""A showcase-README képernyőképeinek gyártása — egységes méretben, egy paranccsal.

Futtatás a repó gyökeréből (a Chromium egyszeri telepítése: `.venv/bin/playwright install chromium`):

    .venv/bin/python tools/screenshots.py                  # → docs/screenshots/
    .venv/bin/python tools/screenshots.py --only 03        # csak a 03-mal kezdődő kép
    .venv/bin/python tools/screenshots.py --out kepek/

Saját szervert indít egy szabad porton (127.0.0.1), és a végén leállítja. A képek 1440×1000
pixelesek, világos témában; a hosszú oldalaknál a lap tetejét (a nézet első képernyőjét) mutatják.
"""

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from felulet_ellenorzes import megnyit, szabad_port, szerver_indit

WIDTH, HEIGHT = 1440, 1000

# (fájlnév, útvonal, megvárandó elem, a kép tetejére görgetendő címsor szövegének kezdete vagy None)
KEPEK = [
    ("01-attekintes", "", "h1", None),
    ("02-mukodesi-modell", "00-mukodesi-modell", "h1", "0.2. A modell egy ábrán"),
    ("03-g1-kapu", "g1-kapu", "h1", None),
    ("04-meroszamkartya", "02-meresi-rendszer", "h1", "MK-04"),
    ("05-xyo-minta", "kapudontesek", "h1", None),
    ("06-tudasbazis", "tudasbazis?szocikk=golden-set", "h1", None),
    ("07-mintatar", "mintatar", "h1", None),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(ROOT / "docs" / "screenshots"), help="célmappa")
    parser.add_argument("--only", help="csak az ilyen előtagú fájlnevű kép (pl. 03)")
    args = parser.parse_args()
    ki = Path(args.out)
    ki.mkdir(parents=True, exist_ok=True)

    port = szabad_port()
    szerver = szerver_indit(port)
    try:
        with sync_playwright() as p:
            bongeszo = p.chromium.launch()
            oldal = bongeszo.new_page(viewport={"width": WIDTH, "height": HEIGHT})
            for nev, ut, var, cel in KEPEK:
                if args.only and not nev.startswith(args.only):
                    continue
                megnyit(oldal, f"http://127.0.0.1:{port}", ut, var)
                oldal.add_style_tag(content="[data-testid=stToolbar], [data-testid=stDeployButton] { display: none; }")
                if cel:
                    cim = oldal.locator("h1, h2, h3").filter(has_text=cel).first
                    if not cim.count():
                        raise SystemExit(f"{nev}: nincs „{cel}” kezdetű címsor — a tartalom változott?")
                    cim.evaluate("e => e.scrollIntoView({block: 'start'})")
                    oldal.wait_for_timeout(500)
                fajl = ki / f"{nev}.png"
                oldal.screenshot(path=str(fajl))
                print("kész:", fajl.relative_to(ROOT) if fajl.is_relative_to(ROOT) else fajl)
            bongeszo.close()
    finally:
        szerver.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
