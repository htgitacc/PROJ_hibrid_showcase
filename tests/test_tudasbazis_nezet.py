"""A tudásbázis-oldal: megjelenés, keresés, szűrés, belső linkek (AppTest)."""

import re

from streamlit.testing.v1 import AppTest

from hibrid_app import tudasbazis as tb
from hibrid_app import tudasbazis_nezet as n

SZOCIKKEK = tb.betolt()
SCRIPT = "from hibrid_app import tudasbazis_nezet\ntudasbazis_nezet.tudasbazis()\n"


def oldal() -> AppTest:
    at = AppTest.from_string(SCRIPT, default_timeout=60).run()
    assert not at.exception, at.exception
    return at


def cimek(at: AppTest) -> list[str]:
    return [s.value for s in at.subheader]


def horgonyok(at: AppTest) -> list[str]:
    return [s.proto.anchor for s in at.subheader]


def belso_linkek(szoveg: str) -> set[str]:
    return set(re.findall(r"\]\(#([^)]+)\)", szoveg))


def szocikk_szovegek(at: AppTest) -> str:
    """A szócikkek törzse (a „Ugrás” index nélkül): a `Mit jelent` mezővel kezdődő markdown-elemek."""
    return "\n".join(m.value for m in at.markdown if m.value.startswith("**Mit jelent:**"))


def test_minden_szocikk_megjelenik_kategoriankent():
    at = oldal()
    assert cimek(at) == [s.cim for s in SZOCIKKEK]
    assert [h.value for h in at.header] == tb.kategoriak(SZOCIKKEK)
    assert at.caption[0].value == f"{len(SZOCIKKEK)} szócikk a {len(SZOCIKKEK)}-ből."


def test_a_horgonyok_egyeznek_a_beolvasoval():
    at = oldal()
    assert horgonyok(at) == [s.horgony for s in SZOCIKKEK]


def test_a_szocikk_mezoi_megjelennek():
    at = oldal()
    ai_act = next(m.value for m in at.markdown if "az EU mesterséges intelligenciáról" in m.value)
    for mezo in ("**Mit jelent:**", "**Hol fordul elő:**", "**Tipikus félreolvasás:**", "**Lásd:**"):
        assert mezo in ai_act


def test_kereses_szukit_es_a_darabszam_frissul():
    at = oldal()
    at.text_input(key=n.K_KERES).set_value("leakage").run()
    vart = [s.cim for s in tb.keres(SZOCIKKEK, "leakage")]
    assert cimek(at) == vart and "Permission leakage" in vart
    assert at.caption[0].value == f"{len(vart)} szócikk a {len(SZOCIKKEK)}-ből."


def test_kereses_ekezet_nelkul_is_talal():
    at = oldal()
    at.text_input(key=n.K_KERES).set_value("meres").run()
    assert cimek(at) == [s.cim for s in tb.keres(SZOCIKKEK, "mérés")]
    assert len(cimek(at)) > 5


def test_kategoria_szuro():
    at = oldal()
    at.selectbox(key=n.K_KATEGORIA).select("Mutatók").run()
    assert [h.value for h in at.header] == ["Mutatók"]
    assert cimek(at) == [s.cim for s in SZOCIKKEK if s.kategoria == "Mutatók"]


def test_a_kategoria_lista_a_fajl_sorrendjeben_van():
    at = oldal()
    assert list(at.selectbox(key=n.K_KATEGORIA).options) == [n.MINDEN, *tb.kategoriak(SZOCIKKEK)]


def test_nincs_talalat():
    at = oldal()
    at.text_input(key=n.K_KERES).set_value("zzzzzzzz").run()
    assert not at.exception
    assert cimek(at) == [] and len(at.header) == 0
    assert "Nincs találat" in at.info[0].value
    assert at.caption[0].value.startswith("0 szócikk")


def test_teljes_listaban_minden_belso_link_celpontja_letezik():
    at = oldal()
    celok = belso_linkek(szocikk_szovegek(at))
    assert len(celok) > 20  # a tudásbázis erősen hivatkozik önmagára
    assert celok <= set(horgonyok(at))


def test_szurt_listaban_nincs_halott_belso_link():
    """A rejtett szócikkre mutató link sima szöveg lesz, a látszóra mutató megmarad."""
    at = oldal()
    at.text_input(key=n.K_KERES).set_value("kapu").run()
    lathato = set(horgonyok(at))
    assert 0 < len(lathato) < len(SZOCIKKEK)
    szoveg = szocikk_szovegek(at)
    assert belso_linkek(szoveg) <= lathato
    assert belso_linkek(szoveg)  # a látszó szócikkek közti linkek megmaradnak
    # a teljes listában több link van, mint a szűrtben: a rejtettek szöveggé váltak
    assert len(belso_linkek(szocikk_szovegek(oldal()))) > len(belso_linkek(szoveg))


def test_dokumentum_link_a_felulet_oldalara_mutat_ugyanabban_a_lapban():
    at = oldal()
    ai_act = next(m.value for m in at.markdown if "az EU mesterséges intelligenciáról" in m.value)
    assert '<a href="04-szabalyozas" target="_self">04</a>' in ai_act
    assert "](04-szabalyozas.md" not in ai_act and ".md`" not in ai_act  # nincs halott link, nincs fájlnév-szöveg
    osszes = szocikk_szovegek(at)
    assert not re.search(r"\]\([^)#][^)]*\.md", osszes)  # sehol sem maradt nyers .md link


def test_az_ugras_index_a_lathato_szocikkekre_mutat():
    at = oldal()
    at.text_input(key=n.K_KERES).set_value("leakage").run()
    index = "\n".join(m.value for m in at.expander[0].markdown)
    assert belso_linkek(index) == set(horgonyok(at))
    assert "[Permission leakage](#permission-leakage)" in index
    assert "**Mutatók:**" in index and "**Rövidítések:**" not in index  # üres kategória kimarad


def test_a_teljes_alkalmazas_lefut():
    from tests.conftest import ROOT

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception, at.exception


# --- ?szocikk=… : másik oldalról érkező link, a szócikk kiemelve felül -----------------------


def kiemelt(szocikk: str) -> AppTest:
    at = AppTest.from_string(SCRIPT, default_timeout=60)
    at.query_params["szocikk"] = szocikk
    at.run()
    assert not at.exception, at.exception
    return at


def test_a_kert_szocikk_kiemelve_felul():
    at = kiemelt("dpia")
    assert at.caption[0].value == "Kiválasztott szócikk"
    assert at.subheader[0].value == "DPIA"
    assert at.subheader[0].proto.anchor == ""  # a kártya címének nincs horgonya: nem ütközik a lista DPIA-jával
    torzsek = [m.value for m in at.markdown if m.value.startswith("**Mit jelent:**") and "Data Protection Impact" in m.value]
    assert len(torzsek) == 2  # egyszer a kártyán, egyszer a teljes listában


def test_a_teljes_lista_a_kartya_mellett_is_megvan():
    at = kiemelt("dpia")
    assert [s.value for s in at.subheader][1:] == [s.cim for s in SZOCIKKEK]  # kártya + 54 szócikk
    assert [s.proto.anchor for s in at.subheader][1:] == [s.horgony for s in SZOCIKKEK]


def test_a_kartya_linkjei_a_listara_es_a_felulet_oldalaira_mutatnak():
    at = kiemelt("ai-act")
    kartya = next(m.value for m in at.markdown if "az EU mesterséges intelligenciáról" in m.value)
    assert "[DPIA](#dpia)" in kartya  # a listabeli szócikkre (az oldalon belül, kattintásra pontos)
    assert '<a href="04-szabalyozas" target="_self">04</a>' in kartya
    assert all(m.proto.allow_html for m in at.markdown if '<a href="' in m.value)


def test_ismeretlen_szocikk_figyelmeztetes_es_a_lista_marad():
    at = kiemelt("nincs-ilyen")
    assert "nincs-ilyen" in at.warning[0].value
    assert [s.value for s in at.subheader] == [s.cim for s in SZOCIKKEK]  # nincs kártya
    assert len(at.caption) == 1 and "szócikk a" in at.caption[0].value


def test_az_osszes_szocikk_gomb_torli_a_parametert():
    at = kiemelt("dpia")
    at.button(key="tb_osszes").click().run()
    assert not at.exception
    assert "szocikk" not in at.query_params
    assert [s.value for s in at.subheader] == [s.cim for s in SZOCIKKEK]  # a kártya eltűnt


def test_param_nelkul_nincs_kartya_es_nincs_gomb():
    at = oldal()
    assert len(at.button) == 0
    assert not any(c.value == "Kiválasztott szócikk" for c in at.caption)
