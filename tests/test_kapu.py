"""A G1-döntés: sávhatárok, a 01 táblájával való egyezés, döntési szabályok, a Xyo-példa esetei."""

import dataclasses
import re

import pytest

from hibrid_app import adatok as a
from hibrid_app import kapu as k
from tests.conftest import olvas, sor, tabla

KAPUK = olvas("koncepcio/01-kapuk-es-kill-criteria.md")
XYO = olvas("koncepcio/04-xyo-pelda.md")

KERET = a.FUTASI_KERET_EVES
# Minden mutató zöld; a tesztek ebből rontanak egyet-egyet.
ZOLD_MERES = a.Meres(0.95, 0.90, None, 8, 0, 0, 5.0, 30)
ZOLD_KOLTSEG = 3_000_000


def dontes(m=ZOLD_MERES, koltseg=ZOLD_KOLTSEG, **kwargs):
    return k.g1_dontes(m, eves_koltseg=koltseg, **kwargs)


def rosszabb(**mezok):
    return dataclasses.replace(ZOLD_MERES, **mezok)


# --- sávhatárok: minden küszöb mindkét oldalról --------------------------------------------


@pytest.mark.parametrize(
    ("fuggveny", "ertek", "vart"),
    [
        (k.sav_leakage, 0, k.ZOLD),
        (k.sav_leakage, 1, k.PIROS),
        (k.sav_faithfulness, 0.90, k.ZOLD),
        (k.sav_faithfulness, 0.89, k.SARGA),
        (k.sav_faithfulness, 0.80, k.SARGA),
        (k.sav_faithfulness, 0.79, k.PIROS),
        (k.sav_recall, 0.85, k.ZOLD),
        (k.sav_recall, 0.84, k.SARGA),
        (k.sav_recall, 0.70, k.SARGA),
        (k.sav_recall, 0.69, k.PIROS),
        (k.sav_latency, 8.0, k.ZOLD),
        (k.sav_latency, 8.1, k.SARGA),
        (k.sav_latency, 15.0, k.SARGA),
        (k.sav_latency, 15.1, k.PIROS),
    ],
)
def test_savhatarok(fuggveny, ertek, vart):
    assert fuggveny(ertek) == vart


@pytest.mark.parametrize(
    ("helyes", "vart"),
    [(8, k.ZOLD), (7, k.SARGA), (6, k.PIROS)],  # 100% · 87,5% · 75% a 8 elemen
)
def test_refusal_sav_a_kis_mintan(helyes, vart):
    assert k.sav_refusal(helyes, 0) == vart


@pytest.mark.parametrize(
    ("helyes", "ossz", "vart"),
    [(18, 20, k.ZOLD), (17, 20, k.SARGA), (16, 20, k.SARGA), (15, 20, k.PIROS)],
)
def test_refusal_hatarertek_a_20_elemes_csoporton(helyes, ossz, vart):
    """A termékágban a csoport 20 elemre bővül: 90% és 80% pontosan elérhető."""
    assert k.sav_refusal(helyes, 0, elutasitando=ossz) == vart


@pytest.mark.parametrize(
    ("teves", "megvalaszolhato", "vart"),
    [(2, 24, k.ZOLD), (3, 24, k.SARGA), (2, 20, k.ZOLD), (3, 20, k.SARGA)],  # 8,3 · 12,5 · 10 · 15%
)
def test_teves_elutasitas_zoldet_sargara_ront(teves, megvalaszolhato, vart):
    assert k.sav_refusal(8, teves, megvalaszolhato=megvalaszolhato) == vart


def test_teves_elutasitas_a_pirosat_nem_javitja():
    assert k.sav_refusal(5, 5) == k.PIROS


@pytest.mark.parametrize(
    ("koltseg", "vart"),
    [
        (KERET, k.ZOLD),  # pontosan a keret: „a keretben”
        (KERET + 1, k.SARGA),
        (KERET * 6 // 5, k.SARGA),  # pontosan 120%
        (KERET * 6 // 5 + 1, k.PIROS),
    ],
)
def test_koltseg_sav(koltseg, vart):
    assert k.sav_koltseg(koltseg) == vart


# --- a küszöbök egyeznek a 01 táblájával ---------------------------------------------------

TABLA = tabla(KAPUK, "| Mutató | Szerepe a kapun")


@pytest.mark.parametrize("kulcs", [m.kulcs for m in k.MUTATOK])
def test_szerep_egyezik_a_dokumentummal(kulcs):
    elotag = {
        "leakage": "[Permission leakage]", "faithfulness": "[Faithfulness]", "recall": "[Context recall]",
        "refusal": "[Correct refusal rate]", "latency": "[Latency]", "koltseg": "Becsült éves",
    }[kulcs]  # fmt: skip
    assert sor(TABLA, elotag)[1] == k.SZEREP[kulcs]


def test_a_diagnosztikai_mutato_nem_kapukritérium():
    assert sor(TABLA, "[Answer relevancy]")[1] == k.DIAGNOSZTIKA
    assert "answer relevancy" not in {m.kulcs for m in k.MUTATOK}


def test_faithfulness_es_recall_kuszobei():
    for elotag, zold, sarga in [
        ("[Faithfulness]", k.FAITHFULNESS_ZOLD, k.FAITHFULNESS_SARGA),
        ("[Context recall]", k.RECALL_ZOLD, k.RECALL_SARGA),
    ]:
        s = sor(TABLA, elotag)
        assert s[2] == f"≥ {a.szam(zold)}"
        assert s[3] == f"{a.szam(sarga)}–{a.szam(zold - 0.01)}"
        assert s[4] == f"< {a.szam(sarga)}"


def test_refusal_kuszobei():
    s = sor(TABLA, "[Correct refusal rate]")
    zold, sarga = round(k.REFUSAL_ZOLD * 100), round(k.REFUSAL_SARGA * 100)
    assert (s[2], s[3], s[4]) == (f"≥ {zold}%", f"{sarga}–{zold - 1}%", f"< {sarga}%")


def test_teves_elutasitas_kuszobe_az_mk03_ban():
    assert f"a téves elutasítás legfeljebb {round(k.TEVES_ELUTASITAS_MAX * 100)}%" in olvas(
        "koncepcio/02-meresi-rendszer.md"
    )


def test_latency_es_koltseg_kuszobei():
    s = sor(TABLA, "[Latency]")
    assert (s[2], s[3], s[4]) == (
        f"≤ {k.LATENCY_ZOLD_S} s", f"{k.LATENCY_ZOLD_S}–{k.LATENCY_SARGA_S} s", f"> {k.LATENCY_SARGA_S} s"
    )
    s = sor(TABLA, "Becsült éves")
    assert (s[2], s[3], s[4]) == (
        "a keretben",
        f"a keret {k.KOLTSEG_ZOLD_SZAZALEK}–{k.KOLTSEG_SARGA_SZAZALEK}%-a",
        f"> {k.KOLTSEG_SARGA_SZAZALEK}%",
    )


def test_a_dokumentum_ot_kill_criteriat_sorol_fel():
    resz = KAPUK.split("**Kill criteria**")[1].split("**Mit jelent a no-go?**")[0]
    szamok = re.findall(r"^(\d)\. ", resz, re.MULTILINE)
    assert szamok == [str(n) for n in k.KILL_CRITERIA]


# --- döntési szabályok ---------------------------------------------------------------------


def test_minden_zold_go():
    d = dontes()
    assert d.kimenet == k.GO and d.kill == ()
    assert set(d.savok.values()) == {k.ZOLD}


def test_go_sarga_tamogatoval_is():
    assert dontes(rosszabb(latency_p95_s=9.0), koltseg=KERET + 1).kimenet == k.GO


@pytest.mark.parametrize(
    ("mezo", "ertek", "kill"),
    [
        ("faithfulness", 0.79, 2),
        ("context_recall", 0.69, 2),
        ("helyes_elutasitas", 6, 2),
        ("szivargas", 1, 1),
    ],
)
def test_kill_criterion_no_go_barmi_mellett(mezo, ertek, kill):
    """Kill criterion: no-go, még azonosított hibahellyel és olcsóbb változattal is."""
    d = dontes(rosszabb(**{mezo: ertek}), hiba_helye_azonositott=True, van_olcsobb_valtozat=True)
    assert d.kimenet == k.NO_GO and kill in d.kill


def test_kill_4_koltseg_olcsobb_valtozat_nelkul():
    d = dontes(koltseg=KERET * 6 // 5 + 1)
    assert d.kimenet == k.NO_GO and d.kill == (4,)


def test_piros_koltseg_olcsobb_valtozattal_nem_kill_hanem_pivot():
    d = dontes(koltseg=KERET * 6 // 5 + 1, van_olcsobb_valtozat=True, hiba_helye_azonositott=True)
    assert d.kimenet == k.PIVOT and d.kill == ()


def test_piros_koltseg_olcsobb_valtozattal_hibahely_nelkul_no_go():
    d = dontes(koltseg=KERET * 6 // 5 + 1, van_olcsobb_valtozat=True)
    assert d.kimenet == k.NO_GO and d.kill == ()


def test_piros_latency_nem_go_es_pivot_hibahellyel():
    m = rosszabb(latency_p95_s=16.0)
    assert dontes(m).kimenet == k.NO_GO
    assert dontes(m, hiba_helye_azonositott=True).kimenet == k.PIVOT


def test_kill_5_adatminoseg():
    m = rosszabb(context_recall=0.80)
    assert dontes(m, hiba_helye_azonositott=True).kimenet == k.PIVOT
    d = dontes(m, hiba_helye_azonositott=True, adatminoseg_a_recall_oka=True)
    assert d.kimenet == k.NO_GO and d.kill == (5,)


def test_kill_5_zold_recallnal_nem_ervenyes():
    assert dontes(adatminoseg_a_recall_oka=True).kimenet == k.GO


def test_pivot_egy_sarga_kritikus_mutatoval_es_hibahellyel():
    d = dontes(rosszabb(context_recall=0.84), hiba_helye_azonositott=True)
    assert d.kimenet == k.PIVOT and d.kill == ()
    assert d.savok["recall"] == k.SARGA


def test_egy_sarga_kritikus_hibahely_nelkul_no_go():
    d = dontes(rosszabb(context_recall=0.84))
    assert d.kimenet == k.NO_GO and d.kill == ()
    assert "nem azonosított" in d.indoklas[0]


def test_ket_sarga_kritikus_no_go_meg_hibahellyel_is():
    """01: „pl. két kritikus mutató sárga” = no-go (minden más eset)."""
    m = rosszabb(context_recall=0.84, faithfulness=0.85)
    d = dontes(m, hiba_helye_azonositott=True)
    assert d.kimenet == k.NO_GO and d.kill == ()


def test_pivot_csak_egyszer():
    m = rosszabb(context_recall=0.84)
    assert dontes(m, hiba_helye_azonositott=True).kimenet == k.PIVOT
    d = dontes(m, hiba_helye_azonositott=True, pivot_volt=True)
    assert d.kimenet == k.NO_GO and d.kill == (3,)  # kill criterion 3


def test_pivot_utan_zold_kritikussal_es_piros_tamogatoval_nincs_masodik_pivot():
    d = dontes(rosszabb(latency_p95_s=16.0), hiba_helye_azonositott=True, pivot_volt=True)
    assert d.kimenet == k.NO_GO and d.kill == ()
    assert "pivot már megvolt" in d.indoklas[0]


def test_pivot_utan_minden_zold_go():
    assert dontes(pivot_volt=True).kimenet == k.GO


def test_a_hibahely_zold_eredmenyen_nem_szamit():
    assert dontes(hiba_helye_azonositott=True).kimenet == k.GO


def test_tobb_kill_egyszerre_mind_megjelenik():
    d = dontes(rosszabb(szivargas=2, faithfulness=0.5))
    assert d.kill == (1, 2)
    assert len(d.indoklas) == 2


# --- a Xyo-példa esetei --------------------------------------------------------------------

IT = a.ITERACIOK


def xyo_dontes(m, **kwargs):
    return k.g1_dontes(m, eves_koltseg=k.eves_koltseg(m), **kwargs)


def test_0_es_1_iteracio_piros_kritikus_miatt_no_go():
    assert xyo_dontes(IT[0]).kill == (2,)  # recall 0,66 és refusal 5/8
    assert xyo_dontes(IT[1]).kill == (2,)  # refusal 5/8 (a recall 0,81 sárga)


def test_2_iteracio_ket_sarga_kritikus_no_go_kill_nelkul():
    d = xyo_dontes(IT[2], hiba_helye_azonositott=True)
    assert d.kimenet == k.NO_GO and d.kill == ()
    assert d.savok["faithfulness"] == k.ZOLD
    assert d.savok["recall"] == d.savok["refusal"] == k.SARGA  # a refusal: téves elutasítás 3/24


def test_3_iteracio_pivot_a_g1_en():
    """04, 4.5: a kizáró zöld, egy kritikus (recall 0,84) sárga, a hely azonosított → pivot."""
    d = xyo_dontes(IT[3], hiba_helye_azonositott=True)
    assert d.kimenet == k.PIVOT and d.kill == ()
    assert d.savok["recall"] == k.SARGA
    assert [s for s in d.savok.values() if s != k.ZOLD] == [k.SARGA]


def test_3_iteracio_hibahely_nelkul_no_go():
    assert xyo_dontes(IT[3]).kimenet == k.NO_GO


def test_pivot_utan_go_a_g1_vesszo_n():
    """04, 4.5: a pivot után a recall 0,88 → G1': go."""
    d = xyo_dontes(a.PIVOT_UTAN, pivot_volt=True)
    assert d.kimenet == k.GO


def test_ha_a_pivot_utan_a_recall_nem_zold_no_go():
    """04, 4.5: „ha a pivot után a recall nem zöld, a döntés no-go” (kill criterion 3)."""
    d = xyo_dontes(dataclasses.replace(a.PIVOT_UTAN, context_recall=0.84), pivot_volt=True, hiba_helye_azonositott=True)
    assert d.kimenet == k.NO_GO and d.kill == (3,)


@pytest.mark.parametrize(
    ("horgony", "meres", "sav_oszlop"),
    [("**Március 3., G1.**", IT[3], 3), ("**Március 19., G1'", a.PIVOT_UTAN, 3)],
    ids=["G1", "G1 vesszo"],
)
def test_a_dokumentum_sav_oszlopa_egyezik(horgony, meres, sav_oszlop):
    """A 04 „Sáv” oszlopát a kód a nyers számokból újraszámolja."""
    savok = k.savok(meres, k.eves_koltseg(meres))
    tab = tabla(XYO, horgony)
    nevek = {"Permission leakage": "leakage", "Faithfulness": "faithfulness", "Context recall": "recall",
             "Correct refusal": "refusal", "Latency": "latency", "Éves futási": "koltseg", "Költség": "koltseg"}  # fmt: skip
    ellenorzott = 0
    for elotag, kulcs in nevek.items():
        talalat = [s for s in tab if s[0].startswith(elotag)]
        if talalat:
            assert talalat[0][sav_oszlop] == savok[kulcs], elotag
            ellenorzott += 1
    assert ellenorzott >= 5
