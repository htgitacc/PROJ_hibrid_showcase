"""A mintatár-oldal: kártyák, letöltőgombok (a hívásaik rögzítésével), beágyazott minta és útmutató."""

import io
import re
import zipfile

from streamlit.testing.v1 import AppTest

from hibrid_app import mintatar as m
from hibrid_app import mintatar_nezet as n
from tests.conftest import ROOT

KATALOGUS = m.katalogus()

# A figyelő rögzíti a st.download_button hívásait (az AppTest a fájlnevet és a tartalmat nem látja).
SCRIPT = """
import streamlit as st
hivasok = []
eredeti = st.download_button
def figyelo(*args, **kwargs):
    hivasok.append((args, kwargs))
    return eredeti(*args, **kwargs)
st.download_button = figyelo
from hibrid_app import mintatar_nezet
mintatar_nezet.mintatar_oldal()
st.session_state["hivasok"] = hivasok
"""


def oldal() -> AppTest:
    at = AppTest.from_string(SCRIPT, default_timeout=60).run()
    assert not at.exception, at.exception
    return at


def hivasok(at: AppTest) -> dict:
    """kulcs → (args, kwargs)"""
    return {kw["key"]: (args, kw) for args, kw in at.session_state["hivasok"]}


def test_kartya_minden_mintahoz_a_katalogus_sorrendjeben():
    at = oldal()
    assert [s.value for s in at.subheader] == [x.cim for x in KATALOGUS]
    szoveg = "\n".join(md.value for md in at.markdown)
    for minta in KATALOGUS:
        for mezo in (minta.mire, minta.mikor, minta.kapu, minta.ki):
            assert mezo in szoveg


def test_a_kartyak_horgonyai_a_fajlnevek():
    """A 6. lépés dokumentumnézete ezekre mutathat: /mintatar#celkartya."""
    at = oldal()
    assert [s.proto.anchor for s in at.subheader] == [
        "meroszamkartya", "celkartya", "kapudontes", "adatleltar", "ai-act-besorolasi-lap",
    ]  # fmt: skip


def test_hat_letoltogomb_egy_zip_es_ot_minta():
    at = oldal()
    gombok = at.get("download_button")
    assert len(gombok) == 1 + len(KATALOGUS)
    assert gombok[0].proto.label == f"Mind az {len(KATALOGUS)} minta (zip)"
    assert [g.proto.label for g in gombok[1:]] == ["Letöltés (.md)"] * len(KATALOGUS)
    vart_kulcsok = [
        "letolt_zip", "letolt_meroszamkartya.md", "letolt_celkartya.md", "letolt_kapudontes.md",
        "letolt_adatleltar.md", "letolt_ai-act-besorolasi-lap.md",
    ]  # fmt: skip
    for gomb, kulcs in zip(gombok, vart_kulcsok, strict=True):
        assert gomb.proto.id.endswith(kulcs)
    assert n.K_ZIP == "letolt_zip"


def test_az_md_letoltes_fajlnev_tipus_es_tartalom():
    h = hivasok(oldal())
    for minta in KATALOGUS:
        _, kw = h[n.kulcs(minta)]
        assert kw["file_name"] == minta.fajl
        assert kw["mime"] == "text/markdown"
        assert kw["data"] == (ROOT / "koncepcio/sablonok" / minta.fajl).read_bytes()  # bájtra a repóbeli


def test_a_zip_letoltes_fajlnev_tipus_es_tartalom():
    _, kw = hivasok(oldal())[n.K_ZIP]
    assert kw["file_name"] == "hibrid-pm-sablonok.zip" and kw["mime"] == "application/zip"
    assert callable(kw["data"])  # csak kattintáskor épül
    z = zipfile.ZipFile(io.BytesIO(kw["data"]()))
    for minta in KATALOGUS:
        assert z.read(f"sablonok/{minta.fajl}") == minta.bajtok()


def test_ket_tab_es_egy_lenyilo_mintankent():
    at = oldal()
    assert len(at.tabs) == 2 * len(KATALOGUS)
    assert [t.label for t in at.tabs] == ["A minta", "Kitöltési útmutató"] * len(KATALOGUS)
    cimek = [e.label for e in at.expander]
    assert cimek[0] == "Hogyan használd jól"
    assert cimek[1:] == ["Megnézem: a minta és a kitöltési útmutató"] * len(KATALOGUS)


def test_a_hasznalati_szabalyok_a_readme_bol_jonnek():
    at = oldal()
    szabalyok = m.hasznalati_szabalyok()
    assert "Ne töltsd ki mindet egyszerre" in szabalyok
    assert "\n".join(md.value for md in at.expander[0].markdown).strip() == szabalyok.strip()


def beagyazott(at: AppTest, minta_index: int, ful: int) -> str:
    return "\n".join(md.value for md in at.tabs[2 * minta_index + ful].markdown)


def test_a_minta_ful_tartalmazza_a_mintat_cim_nelkul():
    at = oldal()
    ful = beagyazott(at, 0, 0)  # Mérőszámkártya
    assert "**Kártya azonosító:** [MK-nn]" in ful
    assert "Mérőszámkártya — [MK-nn]" not in ful  # a címet a kártya mutatja
    assert "Kitöltési útmutató" not in ful  # az a másik fül


def test_az_utmutato_ful_tartalmazza_az_utmutatot_fejlec_nelkul():
    at = oldal()
    for i, minta in enumerate(KATALOGUS):
        ful = beagyazott(at, i, 1)
        _, utmutato = m.szetbont(minta.szoveg())
        elso_tartalmi_sor = next(s for s in utmutato.splitlines()[1:] if s.strip())
        assert elso_tartalmi_sor.split("](")[0].split("[")[0] in ful, minta.cim
        assert not ful.lstrip().startswith("#")  # a fül címe a fejléc
        assert len(ful) > 500


def test_a_beagyazott_cimsorok_lefokozottak():
    """A kártya saját címe (h3) alatt nincs h1–h3 címsor a beágyazott szövegben."""
    at = oldal()
    for i in range(len(KATALOGUS)):
        for ful in (0, 1):
            assert not re.search(r"^#{1,3} ", beagyazott(at, i, ful), re.MULTILINE), (i, ful)
    assert re.search(r"^#### 1\. Bemenetek", beagyazott(at, 2, 0), re.MULTILINE)  # Kapudöntés


def test_relativ_dokumentum_linkek_a_felulet_oldalaira_mutatnak():
    at = oldal()
    szoveg = "\n".join(beagyazott(at, i, ful) for i in range(len(KATALOGUS)) for ful in (0, 1))
    assert not re.search(r"\]\([^)#][^)]*\.md", szoveg)  # nincs nyers .md link
    assert ".md`" not in szoveg  # és nincs fájlnév-tartalék sem: minden link feloldható
    assert '<a href="04-xyo-pelda" target="_self">' in szoveg  # ../04-xyo-pelda.md
    assert '<a href="02-meresi-rendszer" target="_self">' in szoveg
    assert '<a href="tudasbazis?szocikk=' in szoveg  # ../../kutatas/tudasbazis.md#…


def test_a_teljes_alkalmazas_lefut():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception, at.exception


def test_minden_minta_kartyajan_ott_a_kitoltott_pelda_linkje_ugyanabban_a_lapban():
    szoveg = "\n".join(md.value for md in oldal().markdown)
    assert szoveg.count("**Kitöltött példa:**") == len(KATALOGUS)
    for href in ("02-meresi-rendszer", "celkartyak", "kapudontesek", "adatleltar", "ai-act-besorolasi-lap"):
        assert f'<a href="{href}" target="_self">' in szoveg
