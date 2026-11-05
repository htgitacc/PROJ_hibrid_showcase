"""Az Áttekintés oldal: tartalom, és hogy minden linkje létező oldalra mutat."""

import re

from streamlit.testing.v1 import AppTest

from hibrid_app import config, navigacio, views


def oldal() -> AppTest:
    at = AppTest.from_string("from hibrid_app import views\nviews.overview()\n", default_timeout=60).run()
    assert not at.exception, at.exception
    return at


def tartalom(at: AppTest) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_a_cim_es_a_bevezeto():
    at = oldal()
    assert at.title[0].value == config.APP_TITLE
    assert at.subheader[0].value == "Mit találsz itt?"


def test_minden_szekcio_felsorolva_a_navigacio_szekcioi_szerint():
    szoveg = tartalom(oldal())
    for szekcio in ("Kutatás", "Koncepció", "G1 — PoC-kapu", "Tudásbázis", "Mintatár"):
        assert f"**{szekcio}**:" in szoveg


def test_nincs_epul_felirat():
    assert "épül" not in tartalom(oldal())
    assert len(oldal().info) == 0


def test_minden_link_letezo_oldalra_mutat_ugyanabban_a_lapban():
    szoveg = tartalom(oldal())
    linkek = re.findall(r'<a href="([^"]+)" target="_self">', szoveg)
    assert len(linkek) == len(views.LINKEK) == 6
    utak = {o.url for o in navigacio.leirasok() if o.url}
    assert set(linkek) <= utak
    assert "](" not in szoveg  # nincs markdown-link (új lapot nyitna)


def test_a_html_linkek_engedelyezett_html_ben_vannak():
    at = oldal()
    assert all(m.proto.allow_html for m in at.markdown if '<a href="' in m.value)


def test_a_sablon_minden_helyorzoje_kitoltott():
    assert "{" not in tartalom(oldal())


def test_a_link_segedfuggveny():
    assert views.link("x", "y") == '<a href="y" target="_self">x</a>'
