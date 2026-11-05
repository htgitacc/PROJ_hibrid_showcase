"""Az adatréteg és a dokumentumok egyezése: a Xyo-példa számai a szövegben és itt azonosak.

A dokumentum az elsődleges: ha egy szám eltér, a teszt bukik, és el kell dönteni, melyik a helyes.
"""

import re

import pytest

from hibrid_app import adatok as a
from tests.conftest import olvas, sor, tabla

XYO = olvas("koncepcio/04-xyo-pelda.md")
MERES = olvas("koncepcio/02-meresi-rendszer.md")


def szamertek(cella: str) -> float:
    """Az első szám a cellából, tizedesvesszővel: „11,2 s” → 11.2."""
    return float(re.search(r"\d+(?:,\d+)?", cella).group().replace(",", "."))


def hanyad(cella: str) -> tuple[int, int, float | None]:
    """„5/8 (62,5%)” → (5, 8, 62.5); „8/8 · 2/24” csak az elsőt adja. A százalék elhagyható."""
    m = re.match(r"(\d+)/(\d+)(?: \((\d+(?:,\d+)?)%\))?", cella)
    szazalek = float(m.group(3).replace(",", ".")) if m.group(3) else None
    return int(m.group(1)), int(m.group(2)), szazalek


# --- 4.4: a kísérleti szakasz iterációinak táblája -------------------------------------------------------


@pytest.mark.parametrize("i", range(4))
def test_iteracio_tabla_egyezik(i):
    tab = tabla(XYO, "### Az eredmények iterációnként")
    m = a.ITERACIOK[i]
    oszlop = i + 2  # 0: mutató, 1: küszöb
    assert szamertek(sor(tab, "MK-01")[oszlop]) == m.faithfulness
    assert szamertek(sor(tab, "MK-02")[oszlop]) == m.context_recall
    assert szamertek(sor(tab, "Context precision")[oszlop]) == m.context_precision
    assert szamertek(sor(tab, "MK-05")[oszlop]) == m.latency_p95_s
    assert szamertek(sor(tab, "MK-06")[oszlop]) == m.koltseg_ft

    ok, ossz, szazalek = hanyad(sor(tab, "MK-03")[oszlop])
    assert (ok, ossz) == (m.helyes_elutasitas, a.GOLDEN_ELUTASITANDO)
    if szazalek is not None:  # ahol a dokumentum százalékot is ír, annak is stimmelnie kell
        assert szazalek == round(100 * ok / ossz, 1)

    teves, ossz, szazalek = hanyad(sor(tab, "Téves elutasítás")[oszlop])
    assert (teves, ossz) == (m.teves_elutasitas, a.GOLDEN_MEGVALASZOLHATO)
    if szazalek is not None:
        assert szazalek == round(100 * teves / ossz, 1)

    szivargas, ossz, _ = hanyad(sor(tab, "MK-04")[oszlop])
    assert (szivargas, ossz) == (m.szivargas, a.JOGOSULTSAGI_ESETEK)


# --- 4.5: a G1-tábla (3. iteráció) és a pivot utáni tábla ----------------------------------


def test_g1_tabla_a_3_iteracio_eredmenye():
    tab = tabla(XYO, "**Március 3., G1.**")
    m = a.ITERACIOK[3]
    assert szamertek(sor(tab, "Faithfulness")[2]) == m.faithfulness
    assert szamertek(sor(tab, "Context recall")[2]) == m.context_recall
    assert hanyad(sor(tab, "Correct refusal")[2])[0] == m.helyes_elutasitas
    assert f"téves elutasítás {m.teves_elutasitas}/24" in sor(tab, "Correct refusal")[2]
    assert hanyad(sor(tab, "Permission leakage")[2])[0] == m.szivargas
    assert szamertek(sor(tab, "Latency")[2]) == m.latency_p95_s


def test_pivot_utani_tabla():
    tab = tabla(XYO, "**Március 19., G1'")
    elotte, utana = a.ITERACIOK[3], a.PIVOT_UTAN
    for nev, mezo in [("Context recall", "context_recall"), ("Faithfulness", "faithfulness")]:
        assert szamertek(sor(tab, nev)[1]) == getattr(elotte, mezo)
        assert szamertek(sor(tab, nev)[2]) == getattr(utana, mezo)
    refusal = sor(tab, "Correct refusal")[2]
    assert hanyad(refusal)[0] == utana.helyes_elutasitas
    assert "2/24" in refusal and utana.teves_elutasitas == 2
    assert szamertek(sor(tab, "Latency")[2]) == utana.latency_p95_s
    assert szamertek(sor(tab, "Költség")[2]) == utana.koltseg_ft
    assert hanyad(sor(tab, "Permission leakage")[2])[0] == utana.szivargas


# --- a szövegben szereplő összegek, darabszámok, idők --------------------------------------


@pytest.mark.parametrize(
    "szoveg",
    [
        a.ft(a.POC_KERET),
        a.ft(a.POC_TARTALEK),
        a.ft(a.BEVEZETESI_KERET),
        f"{a.ezres(a.FUTASI_KERET_EVES)} Ft/év",
        a.ft(a.PIVOT_KOLTSEG),
        a.ezres(a.KERESES_EVENTE),
        a.ido(a.T0_MEDIAN_MP),
        a.ido(a.T1_MEDIAN_MP),
        f"{a.ezres(a.KISERLETI_DOKUMENTUM)} dokumentum",
        f"{a.OCR_PDF_DB} szkennelt PDF",
        f"{a.ARCHIVALT_DOKUMENTUM} elavult dokumentumot",
        f"havonta {a.JEGY_HAVONTA}",
        f"{a.szam(a.KISERLETI_TELJES_KOLTSEG / 1e6, 1)} M Ft",
        f"**{round(a.WAU_T1 * 100)}%**",
    ],
)
def test_szam_szerepel_a_szovegben(szoveg):
    assert szoveg in XYO


def test_letszam_es_kereses_a_szovegben():
    assert f"kb. {a.LETSZAM} fő" in XYO
    assert f"{a.LETSZAM} fő × {a.KERESES_HETENTE} keresés × {a.MUNKAHETEK} hét" in XYO
    assert "| 7 |" in XYO  # a heti keresési alkalmak a baseline-táblában
    assert f"{a.PILOT_FO} munkatárs" in XYO


# --- a golden set (02, 2.2) ----------------------------------------------------------------


def test_golden_set_egyezik_a_meresi_rendszerrel():
    tab = tabla(MERES, "## 2.2.")
    assert int(sor(tab, "Megválaszolható")[1]) == a.GOLDEN_MEGVALASZOLHATO
    assert int(sor(tab, "A tárakban")[1]) == a.GOLDEN_ELUTASITANDO
    assert int(sor(tab, "Nehéz")[1]) == a.GOLDEN_NEHEZ
    assert int(sor(tab, "Összesen")[1]) == a.GOLDEN_OSSZESEN
    assert f"{a.JOGOSULTSAGI_ESETEK} eset" in MERES


def test_golden_set_a_xyo_peldaban_is_ugyanennyi():
    assert f"{a.GOLDEN_MEGVALASZOLHATO} megválaszolható, {a.GOLDEN_ELUTASITANDO} elutasítandó és {a.GOLDEN_NEHEZ} nehéz" in XYO
    assert f"({a.GOLDEN_OSSZESEN} elem)" in XYO
    assert f"{a.JOGOSULTSAGI_ESETEK} esetes" in XYO


# --- a hullámok táblája (4.6) --------------------------------------------------------------


@pytest.mark.parametrize("hullam", a.HULLAMOK, ids=lambda h: h.nev)
def test_hullamok_tablaja(hullam):
    tab = tabla(XYO, "### Bevezetési ág")
    s = sor(tab, hullam.nev)
    assert f"{hullam.fo} fő" in s[1] or f"{hullam.fo} fője" in s[1]
    evvel = hullam is a.HULLAMOK[0]  # az évszám csak az első sor tervezett cellájában áll
    assert s[2] == a.datum(hullam.tervezett, evvel=evvel)
    assert s[3] == a.datum(hullam.tenyleges, evvel=False)


# --- kapudátumok a szövegben ---------------------------------------------------------------


@pytest.mark.parametrize(
    "d",
    [a.G0_MASODIK, a.ZARAS],
    ids=["G0 második", "zárás"],
)
def test_datum_a_szovegben(d):
    assert a.datum(d) in XYO


@pytest.mark.parametrize(
    ("d", "folytatas"),
    [(a.G0_ELSO, "első G0.**"), (a.G1, "G1.**"), (a.G1_MASODIK, "G1'")],
)
def test_kapudatum_a_szoveg_felkover_jelzesben(d, folytatas):
    assert f"**{a.datum(d, evvel=False).capitalize()}, {folytatas}" in XYO


# --- belső következetesség: a számok egymásból levezethetők --------------------------------


def test_keresesek_szama_levezetheto():
    assert a.KERESES_EVENTE == 77_280
    assert a.PILOT_FO + a.KITERJESZTES_FO == a.LETSZAM
    assert sum(h.fo for h in a.HULLAMOK[1:]) == a.KITERJESZTES_FO


def test_cel_feladatido_es_megtakaritas():
    cel_mp = round(a.T0_MEDIAN_MP * (1 - a.CEL_CSOKKENES))
    assert a.ido(cel_mp).replace(" perc ", ":").replace(" mp", "") == "4:33"  # „≤ 4 perc 33 mp”
    assert "4 perc 33 mp" in XYO
    megtakaritas_mp = a.T0_MEDIAN_MP * a.CEL_CSOKKENES
    assert round(megtakaritas_mp) == 117
    ora = a.KERESES_EVENTE * megtakaritas_mp / 3600
    assert round(ora / 50) * 50 == 2_500  # „kb. 2 500 óra évente”
    assert round(ora / 2 / 50) * 50 == 1_250  # 50%-os használatnál „kb. 1 250”


def test_t1_csokkenes_41_szazalek():
    assert round(100 * (1 - a.T1_MEDIAN_MP / a.T0_MEDIAN_MP)) == 41
    assert "−41%" in XYO


def test_koltseg_a_keretben():
    assert int(a.FUTASI_KERET_EVES / a.KERESES_EVENTE) == a.KOLTSEG_KERDESENKENT_HATAR  # „kb. 46 Ft”
    ev = a.ITERACIOK[3].koltseg_ft * a.KERESES_EVENTE
    assert round(ev / 1e6, 1) == 3.2  # „≈ 3,2 M Ft”
    assert ev <= a.FUTASI_KERET_EVES
    for m in a.ITERACIOK[3:] + (a.PIVOT_UTAN,):
        assert m.koltseg_ft <= a.KOLTSEG_KERDESENKENT_HATAR


def test_pivot_a_tartalekbol_es_a_mag_a_keretben():
    assert a.PIVOT_KOLTSEG <= a.POC_TARTALEK
    assert a.KISERLETI_TELJES_KOLTSEG <= a.POC_KERET


def test_a_mag_hetfotol_penteki_hetedik_hetig():
    assert a.KISERLETI_KEZDET.weekday() == 0 and a.KISERLETI_VEG.weekday() == 4
    assert ((a.KISERLETI_VEG - a.KISERLETI_KEZDET).days + 3) // 7 == 7  # „7 hét”
    assert "7 hét" in XYO


def test_a_hullamok_sorrendje_es_a_halasztas():
    for elozo, kovetkezo in zip(a.HULLAMOK, a.HULLAMOK[1:]):
        assert elozo.tenyleges < kovetkezo.tenyleges
    halasztott = [h for h in a.HULLAMOK if h.tenyleges != h.tervezett]
    assert [h.nev for h in halasztott] == ["2. hullám"]
    assert (halasztott[0].tenyleges - halasztott[0].tervezett).days == 14  # „két hét”


def test_g1_sorrend():
    assert a.G0_ELSO < a.G0_MASODIK < a.KISERLETI_KEZDET < a.KISERLETI_VEG < a.G1 < a.G1_MASODIK < a.ZARAS
    assert (a.G1_MASODIK - a.G1).days <= 16  # pivot: legfeljebb két hét + a kapuülés
