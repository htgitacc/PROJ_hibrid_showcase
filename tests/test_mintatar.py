"""A mintatár: a katalógus a README-ből, a szétbontás, a lefokozás és a letölthető csomag."""

import io
import re
import zipfile

import pytest

from hibrid_app import config
from hibrid_app import mintatar as m

KATALOGUS = m.katalogus()
FAJLOK = sorted(p.name for p in config.SABLONOK_DIR.glob("*.md") if p.name != "README.md")


# --- katalógus -----------------------------------------------------------------------------


def test_a_katalogus_a_readme_tablajanak_sorai_sorrendben():
    assert [x.cim for x in KATALOGUS] == [
        "Mérőszámkártya", "Célkártya", "Kapudöntés", "Adatleltár", "AI Act-besorolási lap",
    ]  # fmt: skip
    assert [x.fajl for x in KATALOGUS] == [
        "meroszamkartya.md", "celkartya.md", "kapudontes.md", "adatleltar.md", "ai-act-besorolasi-lap.md",
    ]  # fmt: skip


def test_minden_sablonfajl_a_katalogusban_van_es_forditva():
    """Új minta fájlja README-sor nélkül (vagy fordítva) ne maradhasson."""
    assert sorted(x.fajl for x in KATALOGUS) == FAJLOK


@pytest.mark.parametrize("minta", KATALOGUS, ids=lambda x: x.fajl)
def test_a_katalogus_mezoi_kitoltottek(minta):
    for mezo in (minta.cim, minta.mire, minta.mikor, minta.kapu, minta.ki):
        assert mezo.strip()


@pytest.mark.parametrize("minta", KATALOGUS, ids=lambda x: x.fajl)
def test_szoveg_es_bajtok_a_repobeli_fajl(minta):
    fajl = config.SABLONOK_DIR / minta.fajl
    assert minta.szoveg() == fajl.read_text(encoding="utf-8")
    assert minta.bajtok() == fajl.read_bytes()


@pytest.mark.parametrize("minta", KATALOGUS, ids=lambda x: x.fajl)
def test_minden_minta_harom_reszbol_all(minta):
    """A sablonok/README szerint: használat · a minta · kitöltési útmutató."""
    szoveg = minta.szoveg()
    assert "**Használat.**" in szoveg
    assert szoveg.count(m.UTMUTATO_FEJLEC) == 1
    assert szoveg.index("**Használat.**") < szoveg.index(m.UTMUTATO_FEJLEC)


def test_hibas_readme_sor_hibat_dob(monkeypatch, tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("| [A](a.md) | csak | három | oszlop |\n", encoding="utf-8")
    monkeypatch.setattr(m, "README", readme)
    with pytest.raises(ValueError, match="5 oszlopos"):
        m.katalogus()


# --- szétbontás ----------------------------------------------------------------------------


@pytest.mark.parametrize("minta", KATALOGUS, ids=lambda x: x.fajl)
def test_a_szetbontas_nem_veszit_el_egy_sort_sem(minta):
    szoveg = minta.szoveg()
    minta_resz, utmutato = m.szetbont(szoveg)
    nem_ures = [s for s in szoveg.splitlines() if s.strip()]
    assert [s for s in (minta_resz + utmutato).splitlines() if s.strip()] == nem_ures
    assert utmutato.startswith(m.UTMUTATO_FEJLEC)
    assert m.UTMUTATO_FEJLEC not in minta_resz
    assert "Használat" in minta_resz and len(utmutato.splitlines()) > 5


def test_szetbontas_utmutato_nelkul():
    assert m.szetbont("# Cím\n\nszöveg\n") == ("# Cím\n\nszöveg\n", "")


def test_szetbontas_az_elso_utmutato_fejlecnel():
    ele, utana = m.szetbont("# C\n\nminta\n\n## Kitöltési útmutató\n\nút\n")
    assert ele == "# C\n\nminta\n" and utana == "## Kitöltési útmutató\n\nút\n"


# --- lefokozás, törzs ----------------------------------------------------------------------


def test_lefokozas_ket_szinttel():
    assert m.lefokoz("# A\n## B\n### C\ntext\n") == "### A\n#### B\n##### C\ntext\n"


def test_lefokozas_legfeljebb_hatodik_szintig():
    assert m.lefokoz("##### X\n###### Y\n") == "###### X\n###### Y\n"


def test_lefokozas_nem_nyul_a_kodblokkhoz_es_a_nem_cimsorokhoz():
    szoveg = "## B\n```\n## nem cím\n```\n#hashtag\n#### pontosan\n"
    assert m.lefokoz(szoveg) == "#### B\n```\n## nem cím\n```\n#hashtag\n###### pontosan\n"


def test_torzs_elhagyja_az_elso_cimsort():
    assert m.torzs("# Cím\n\nszöveg\n# Másik\n") == "szöveg\n# Másik\n"
    assert m.torzs("szöveg\n") == "szöveg\n"


# --- a letölthető csomag -------------------------------------------------------------------


def olvas_zip() -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BytesIO(m.csomag()))


def test_a_csomag_ervenyes_es_teljes():
    z = olvas_zip()
    assert z.testzip() is None
    assert sorted(z.namelist()) == sorted(
        ["OLVASSEL.txt", "sablonok/README.md", *(f"sablonok/{f}" for f in FAJLOK)]
    )


@pytest.mark.parametrize("fajl", [*FAJLOK, "README.md"])
def test_a_csomag_fajljai_bajtra_egyeznek_a_repobelivel(fajl):
    assert olvas_zip().read(f"sablonok/{fajl}") == (config.SABLONOK_DIR / fajl).read_bytes()


def test_az_olvassel_felsorol_minden_mintat():
    szoveg = olvas_zip().read("OLVASSEL.txt").decode("utf-8")
    for minta in KATALOGUS:
        assert minta.fajl in szoveg and minta.cim in szoveg
    assert re.search(r"Készült: \d{4}-\d{2}-\d{2}", szoveg)


def test_a_csomag_csak_a_megadott_mintakat_tartalmazza():
    z = zipfile.ZipFile(io.BytesIO(m.csomag(KATALOGUS[:2])))
    assert sorted(n for n in z.namelist() if n.startswith("sablonok/") and n != "sablonok/README.md") == [
        "sablonok/celkartya.md", "sablonok/meroszamkartya.md",
    ]  # fmt: skip


def test_ha_ketszer_szerepel_a_fejlec_az_elsonel_vag():
    szoveg = "# C\n\nminta\n\n## Kitöltési útmutató\n\nelső\n\n## Kitöltési útmutató\n\nmásodik\n"
    ele, utana = m.szetbont(szoveg)
    assert ele == "# C\n\nminta\n"
    assert utana.count(m.UTMUTATO_FEJLEC) == 2  # a második az útmutató része marad


# --- a README szakaszai --------------------------------------------------------------------


def test_szakasz_a_kovetkezo_fejlecig():
    szoveg = "# C\n\n## A\n\nelső\n\n## B (x)\n\nmásodik\nsor\n\n## C\n\nharmadik\n"
    assert m.szakasz(szoveg, "A") == "első\n"
    assert m.szakasz(szoveg, "B (x)") == "második\nsor\n"  # a zárójel nem regex-metakarakter
    assert m.szakasz(szoveg, "C") == "harmadik\n"  # az utolsó szakasz a fájl végéig tart


def test_szakasz_hianyzo_fejlecnel_ures():
    assert m.szakasz("## A\n\nszöveg\n", "B") == ""


def test_szakasz_nem_keveri_a_hasonlo_fejleceket():
    assert m.szakasz("## Hogyan használd\n\nx\n\n## Hogyan használd jól\n\ny\n", "Hogyan használd jól") == "y\n"


def test_a_readme_hasznalati_szabalyai():
    szabalyok = m.hasznalati_szabalyok()
    assert szabalyok.startswith("- **Ne töltsd ki mindet egyszerre.**")
    assert "## " not in szabalyok
    assert szabalyok.count("\n- **") == 2  # három szabály
