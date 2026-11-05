"""Böngészős felületi ellenőrzés: amit az AppTest nem lát (elrendezés, linkek, letöltés, ábra).

Futtatás a repó gyökeréből (a Chromium egyszeri telepítése: `.venv/bin/playwright install chromium`):

    .venv/bin/python tools/felulet_ellenorzes.py              # csak ellenőrzés
    .venv/bin/python tools/felulet_ellenorzes.py --ki kepek/  # + képernyőkép minden oldalról (1440, 390 px)
    .venv/bin/python tools/felulet_ellenorzes.py --cim http://127.0.0.1:8525/hibrid  # a futó éles példány

Saját szervert indít egy szabad porton (127.0.0.1), és a végén leállítja; `--cim` esetén a megadott,
már futó példányt méri (pl. az éles unitot a `/hibrid` előtag alatt). Hibánál 1-es kilépési kód.
A mérések: (1) egyik oldal sem csordul túl vízszintesen 390 és 1440 px-en; (2) a dokumentumok, a
tudásbázis és a mintatár közti linkek ugyanabban a lapban nyílnak; (3) a tudásbázis-kártya és az
oldalon belüli horgony; (4) a mintatár letöltései bájtra egyeznek a repóbeliekkel; (5) az ábra
széles képernyőn a tartalomra skálázódik, keskenyen görgethető.
"""

import argparse
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from hibrid_app import mintatar, navigacio

KESKENY, SZELES = (390, 844), (1440, 900)


def szabad_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def szerver_indit(port: int) -> subprocess.Popen:
    kornyezet = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    folyamat = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless", "true",
         "--server.address", "127.0.0.1", "--server.port", str(port)],
        cwd=ROOT, env=kornyezet, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )  # fmt: skip
    for _ in range(60):
        try:
            if urllib.request.urlopen(f"http://127.0.0.1:{port}/_stcore/health", timeout=1).status == 200:
                return folyamat
        except OSError:
            time.sleep(0.5)
    folyamat.terminate()
    raise RuntimeError("A szerver nem indult el 30 másodpercen belül.")


def megnyit(oldal: Page, alap: str, ut: str, var: str = "h1") -> None:
    oldal.goto(f"{alap}/{ut}", wait_until="networkidle")
    oldal.wait_for_selector(var, timeout=30000)
    oldal.wait_for_timeout(1000)


def tetejehez(oldal: Page, azonosito: str) -> int | None:
    return oldal.evaluate(
        "(id) => { const e = document.getElementById(id); return e ? Math.round(e.getBoundingClientRect().top) : null; }",
        azonosito,
    )


def tulcsordulas(oldal: Page) -> tuple[int, int]:
    return oldal.evaluate("() => { const e = document.querySelector('[data-testid=stMain]'); return [e.scrollWidth, e.clientWidth]; }")


def ellenorzes(alap: str, kepek: Path | None) -> list[str]:
    hibak: list[str] = []
    utak = [o.url or "" for o in navigacio.leirasok()]

    with sync_playwright() as p:
        bongeszo = p.chromium.launch()

        # 1) elrendezés: nincs vízszintes túlcsordulás, képernyőkép
        for nev, (w, h) in (("390", KESKENY), ("1440", SZELES)):
            kontextus = bongeszo.new_context(viewport={"width": w, "height": h})
            oldal = kontextus.new_page()
            for ut in utak:
                megnyit(oldal, alap, ut)
                tartalom, lathato = tulcsordulas(oldal)
                if tartalom > lathato + 1:
                    hibak.append(f"{w} px, /{ut}: vízszintes túlcsordulás ({tartalom} > {lathato})")
                if kepek:
                    oldal.screenshot(path=str(kepek / f"{nev}-{ut or 'attekintes'}.png"), full_page=False)
            kontextus.close()
        print(f"1) elrendezés: {len(utak)} oldal × 2 méret átnézve")

        kontextus = bongeszo.new_context(viewport={"width": SZELES[0], "height": SZELES[1]}, accept_downloads=True)
        oldal = kontextus.new_page()

        # 2) dokumentum → tudásbázis-kártya, ugyanabban a lapban
        megnyit(oldal, alap, "04-xyo-pelda")
        link = oldal.locator("a[href^='tudasbazis?szocikk=']:visible").first
        lapok = len(kontextus.pages)
        link.click()
        oldal.wait_for_load_state("networkidle")
        oldal.wait_for_timeout(1500)
        if len(kontextus.pages) != lapok or "tudasbazis?szocikk=" not in oldal.url:
            hibak.append(f"dokumentum → tudásbázis link: új lap nyílt vagy rossz az URL ({oldal.url})")
        if oldal.get_by_text("Kiválasztott szócikk").count() != 1:
            hibak.append("a tudásbázis-kártya nem jelent meg")
        oldal.get_by_role("button", name="Az összes szócikk").click()
        oldal.wait_for_timeout(1500)
        if oldal.get_by_text("Kiválasztott szócikk").count() != 0:
            hibak.append("az „Az összes szócikk” gomb nem törölte a kártyát")
        print("2) dokumentum → tudásbázis-kártya: ugyanabban a lapban")

        # 3) dokumentum → dokumentum; oldalon belüli horgony pontosan a fejléc alá ugrik
        megnyit(oldal, alap, "00-osszefoglalo")
        link = oldal.locator("a[href='01-hibrid-a-piacon']:visible").first
        if link.count():
            link.click()
            oldal.wait_for_load_state("networkidle")
            if not oldal.url.endswith("/01-hibrid-a-piacon"):
                hibak.append(f"dokumentum → dokumentum link rossz URL-re vitt: {oldal.url}")
        else:
            hibak.append("a 00-osszefoglalo nem hivatkozik a 01-hibrid-a-piacon dokumentumra")
        megnyit(oldal, alap, "tudasbazis", var="text=szócikk a")
        horgony = oldal.locator("p a[href^='#']:visible").first  # a „Lásd” link (nem a címsorok horgony-ikonja)
        cel = horgony.get_attribute("href")[1:]
        horgony.click()
        oldal.wait_for_timeout(1200)
        fent = tetejehez(oldal, cel)
        if fent is None or abs(fent - 60) > 3:
            hibak.append(f"tudásbázis, oldalon belüli ugrás: #{cel} a {fent} px-en áll (60 az elvárt)")
        print("3) dokumentum → dokumentum és oldalon belüli ugrás ellenőrizve")

        # 4) mintatár: letöltések bájtra egyeznek a repóbelivel
        megnyit(oldal, alap, "mintatar")
        katalogus = mintatar.katalogus()
        gombok = oldal.get_by_role("button", name="Letöltés (.md)")
        with tempfile.TemporaryDirectory() as ideiglenes:
            for i, minta in enumerate(katalogus):
                with oldal.expect_download() as letoltes:
                    gombok.nth(i).click()
                fajl = Path(ideiglenes) / minta.fajl
                letoltes.value.save_as(fajl)
                if letoltes.value.suggested_filename != minta.fajl or fajl.read_bytes() != minta.bajtok():
                    hibak.append(f"mintatár: a(z) {minta.fajl} letöltése nem egyezik a repóbelivel")
            with oldal.expect_download() as letoltes:
                oldal.get_by_role("button", name=f"Mind az {len(katalogus)} minta (zip)").click()
            zip_fajl = Path(ideiglenes) / "mind.zip"
            letoltes.value.save_as(zip_fajl)
            import zipfile

            with zipfile.ZipFile(zip_fajl) as z:
                for minta in katalogus:
                    if z.read(f"sablonok/{minta.fajl}") != minta.bajtok():
                        hibak.append(f"mintatár zip: a(z) {minta.fajl} nem egyezik a repóbelivel")
        print(f"4) mintatár: {len(katalogus)} minta és a zip bájtra egyezik")

        # 5) az ábra: széles képernyőn a tartalomra skálázódik, keskenyen görgethető
        megnyit(oldal, alap, "00-mukodesi-modell")
        oldal.wait_for_timeout(2500)
        tarolo = oldal.locator(".st-key-abra-0")
        if tarolo.evaluate("e => e.scrollWidth") > tarolo.evaluate("e => e.clientWidth") + 1:
            hibak.append("ábra: széles képernyőn nem szabadna görgethetőnek lennie")
        if oldal.locator(".st-key-abra-tipp-0").is_visible():
            hibak.append("ábra: a görgetési tipp széles képernyőn látszik")
        kontextus.close()
        keskeny = bongeszo.new_context(viewport={"width": KESKENY[0], "height": KESKENY[1]}).new_page()
        megnyit(keskeny, alap, "00-mukodesi-modell")
        keskeny.wait_for_timeout(2500)
        tarolo = keskeny.locator(".st-key-abra-0")
        if tarolo.evaluate("e => e.scrollWidth") <= tarolo.evaluate("e => e.clientWidth") + 1:
            hibak.append("ábra: keskeny képernyőn görgethetőnek kellene lennie")
        if not keskeny.locator(".st-key-abra-tipp-0").is_visible():
            hibak.append("ábra: a görgetési tipp keskeny képernyőn nem látszik")
        print("5) ábra: széles és keskeny elrendezés ellenőrizve")

        bongeszo.close()
    return hibak


def main() -> int:
    argumentumok = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    argumentumok.add_argument("--cim", help="egy már futó példány alapcíme (pl. http://127.0.0.1:8525/hibrid)")
    argumentumok.add_argument("--ki", type=Path, help="könyvtár a képernyőképeknek (nincs megadva: nem készül)")
    kapcsolok = argumentumok.parse_args()
    if kapcsolok.ki:
        kapcsolok.ki.mkdir(parents=True, exist_ok=True)

    if kapcsolok.cim:
        hibak = ellenorzes(kapcsolok.cim.rstrip("/"), kapcsolok.ki)
    else:
        port = szabad_port()
        szerver = szerver_indit(port)
        try:
            hibak = ellenorzes(f"http://127.0.0.1:{port}", kapcsolok.ki)
        finally:
            szerver.terminate()
            szerver.wait(timeout=10)
    if hibak:
        print("\nHIBÁK:")
        for hiba in hibak:
            print(f" - {hiba}")
        return 1
    print("\nMinden böngészős ellenőrzés rendben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
