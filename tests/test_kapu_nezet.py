"""A G1-oldal: előtöltések, csúszkák, a döntés megjelenése (AppTest, valódi Streamlit-futással)."""

import pytest
from streamlit.testing.v1 import AppTest

from hibrid_app import adatok
from hibrid_app import kapu_nezet as n
from tests.conftest import ROOT

SCRIPT = "from hibrid_app import kapu_nezet\nkapu_nezet.g1_kapu()\n"


def oldal() -> AppTest:
    at = AppTest.from_string(SCRIPT, default_timeout=60).run()
    assert not at.exception, at.exception
    return at


def dontes(at: AppTest) -> str:
    """A megjelenített döntés: GO, PIVOT vagy NO-GO (pontosan egy kiemelő doboz van)."""
    dobozok = [("GO", at.success), ("PIVOT", at.warning), ("NO-GO", at.error)]
    jelen = [(nev, d[0].value) for nev, d in dobozok if len(d) == 1]
    assert len(jelen) == 1, jelen
    nev, szoveg = jelen[0]
    assert f"Döntés: {nev}" in szoveg
    return nev


def test_alapertelmezett_a_xyo_g1_es_pivot():
    at = oldal()
    assert at.selectbox(key=n.K_ELOTOLTES).value == n.NEVEK[0]
    assert dontes(at) == "PIVOT"
    assert "Context recall" in at.warning[0].value  # az indoklás megnevezi a sárga mutatót


@pytest.mark.parametrize(
    ("nev", "vart"),
    [
        ("Xyo — 3. iteráció (a G1, március 3.)", "PIVOT"),
        ("Xyo — pivot után (G1', március 19.)", "GO"),
        ("Xyo — 0. iteráció (baseline)", "NO-GO"),
        ("Xyo — 1. iteráció (darabolás)", "NO-GO"),
        ("Xyo — 2. iteráció („csak a forrásból”)", "NO-GO"),
    ],
)
def test_elotoltesek_dontese(nev, vart):
    at = oldal()
    at.selectbox(key=n.K_ELOTOLTES).select(nev).run()
    assert not at.exception, at.exception
    assert dontes(at) == vart


def test_elotoltes_atirja_a_csuszkakat():
    at = oldal()
    at.selectbox(key=n.K_ELOTOLTES).select("Xyo — 0. iteráció (baseline)").run()
    m = adatok.ITERACIOK[0]
    assert at.slider(key=n.K_FAITHFULNESS).value == m.faithfulness
    assert at.slider(key=n.K_RECALL).value == m.context_recall
    assert at.slider(key=n.K_HELYES).value == m.helyes_elutasitas
    assert at.slider(key=n.K_KOLTSEG).value == m.koltseg_ft
    assert at.checkbox(key=n.K_HIBAHELY).value is False


def test_a_recall_kuszobon_atfordul_a_dontes():
    """Az 0,84-es recall pivot; 0,85-nél go; 0,69-nél no-go (kill criterion 2)."""
    at = oldal()
    at.slider(key=n.K_RECALL).set_value(0.85).run()
    assert dontes(at) == "GO"
    at.slider(key=n.K_RECALL).set_value(0.69).run()
    assert dontes(at) == "NO-GO"
    assert "Kill criterion 2" in at.error[0].value


def test_hibahely_nelkul_nincs_pivot():
    at = oldal()
    at.checkbox(key=n.K_HIBAHELY).uncheck().run()
    assert dontes(at) == "NO-GO"
    assert "nem azonosított" in at.error[0].value


def test_szivargas_mindig_no_go():
    at = oldal()
    at.selectbox(key=n.K_ELOTOLTES).select("Xyo — pivot után (G1', március 19.)").run()
    assert dontes(at) == "GO"
    at.number_input(key=n.K_LEAKAGE).set_value(1).run()
    assert dontes(at) == "NO-GO"
    assert "Kill criterion 1" in at.error[0].value


def test_pivot_csak_egyszer():
    at = oldal()
    at.checkbox(key=n.K_PIVOT_VOLT).check().run()
    assert dontes(at) == "NO-GO"
    assert "Kill criterion 3" in at.error[0].value


def test_a_tablazat_mutatja_a_savokat():
    at = oldal()
    tabla = "\n".join(md.value for md in at.markdown if "Mutató | Szerep a kapun" in md.value)
    assert "Context recall | kritikus | 0,84 | :orange[**sárga**]" in tabla
    assert "Permission leakage | kizáró | 0/12 eset | :green[**zöld**]" in tabla
    assert "8/8 (100%); téves elutasítás 2/24 (8,3%)" in tabla
    assert "41 Ft/kérdés → 3,17 M Ft/év (a keret 88%-a)" in tabla
    assert "answer relevancy" in "\n".join(c.value for c in at.caption)  # a diagnosztikai mutató kimarad


def test_a_teljes_alkalmazas_az_uj_oldallal_is_lefut():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception, at.exception


# --- az előtöltés minden mezője, és minden csúszka átér a döntésig -------------------------

EGYEDI = '''
import dataclasses
from hibrid_app import adatok
from hibrid_app import kapu_nezet as n

egyedi = dataclasses.replace(
    adatok.ITERACIOK[3], szivargas=2, teves_elutasitas=5, latency_p95_s=12.3, koltseg_ft=33,
    faithfulness=0.81, context_recall=0.77, helyes_elutasitas=6,
)
n.ELOTOLTESEK = n.ELOTOLTESEK + (n.Elotoltes("Egyedi", egyedi, pivot_volt=True, hiba_helye_azonositott=False),)
n.NEVEK = [e.nev for e in n.ELOTOLTESEK]
n.g1_kapu()
'''


def test_az_elotoltes_minden_mezot_betolt_es_a_jelzoket_visszaallitja():
    at = AppTest.from_string(EGYEDI, default_timeout=60).run()
    at.checkbox(key=n.K_OLCSOBB).check()
    at.checkbox(key=n.K_ADATMINOSEG).check().run()
    at.selectbox(key=n.K_ELOTOLTES).select("Egyedi").run()
    assert not at.exception, at.exception
    assert at.number_input(key=n.K_LEAKAGE).value == 2
    assert at.slider(key=n.K_FAITHFULNESS).value == 0.81
    assert at.slider(key=n.K_RECALL).value == 0.77
    assert at.slider(key=n.K_HELYES).value == 6
    assert at.slider(key=n.K_TEVES).value == 5
    assert at.slider(key=n.K_LATENCY).value == 12.3
    assert at.slider(key=n.K_KOLTSEG).value == 33
    assert at.checkbox(key=n.K_PIVOT_VOLT).value is True
    assert at.checkbox(key=n.K_HIBAHELY).value is False
    assert at.checkbox(key=n.K_OLCSOBB).value is False  # az előtöltés visszaállítja
    assert at.checkbox(key=n.K_ADATMINOSEG).value is False


def test_a_pivot_utani_elotoltes_bejeloli_a_pivot_megvoltat():
    at = oldal()
    at.selectbox(key=n.K_ELOTOLTES).select("Xyo — pivot után (G1', március 19.)").run()
    assert at.checkbox(key=n.K_PIVOT_VOLT).value is True
    assert at.checkbox(key=n.K_HIBAHELY).value is False


def test_a_teves_elutasitas_csuszka_atter_a_dontesig():
    """3/24 = 12,5% téves elutasítás: a refusal sárga, a recall is → két sárga → no-go."""
    at = oldal()
    at.slider(key=n.K_TEVES).set_value(3).run()
    assert dontes(at) == "NO-GO"


def test_a_latency_csuszka_atter_a_dontesig():
    at = oldal()
    at.slider(key=n.K_RECALL).set_value(0.85).run()
    assert dontes(at) == "GO"
    at.slider(key=n.K_LATENCY).set_value(16.0).run()  # piros támogató, azonosított hibahely → pivot
    assert dontes(at) == "PIVOT"


def test_az_olcsobb_valtozat_jelolo_atter_a_dontesig():
    at = oldal()
    at.slider(key=n.K_RECALL).set_value(0.85).run()
    at.slider(key=n.K_KOLTSEG).set_value(70).run()  # 70 Ft × 77 280 ≈ 5,4 M Ft: a keret 150%-a
    assert dontes(at) == "NO-GO" and "Kill criterion 4" in at.error[0].value
    at.checkbox(key=n.K_OLCSOBB).check().run()
    assert dontes(at) == "PIVOT"


def test_az_adatminoseg_jelolo_atter_a_dontesig():
    at = oldal()
    assert dontes(at) == "PIVOT"
    at.checkbox(key=n.K_ADATMINOSEG).check().run()
    assert dontes(at) == "NO-GO" and "Kill criterion 5" in at.error[0].value
