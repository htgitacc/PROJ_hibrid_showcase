"""A dokumentumoldalak és a navigáció: megjelenés, linkek, ábrák, és hogy minden link célja létezik."""

import re

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from hibrid_app import config, dokumentumok, mermaid, navigacio
from hibrid_app import dokumentum_nezet as n
from tests.conftest import ROOT
from tests.test_dokumentumok import osszes_markdown, relativ_linkek

DOKUMENTUMOK = dokumentumok.lista()


def oldal(doc) -> AppTest:
    script = (
        "from hibrid_app import dokumentum_nezet, dokumentumok\n"
        f"doc = next(d for d in dokumentumok.lista() if d.rel == {doc.rel!r})\n"
        "dokumentum_nezet.make_view(doc)()\n"
    )
    at = AppTest.from_string(script, default_timeout=60).run()
    assert not at.exception, at.exception
    return at


def szoveg(at: AppTest) -> str:
    return "\n".join(m.value for m in at.markdown)


# --- bontás --------------------------------------------------------------------------------


def test_reszek_sorrendben():
    s = "# C\n\nelőtte\n\n```mermaid\nflowchart LR\nA --> B\n```\n\nutána\n"
    assert n.reszek(s) == [("md", "# C\n\nelőtte\n\n"), ("mermaid", "flowchart LR\nA --> B\n"), ("md", "\n\nutána\n")]


def test_reszek_abra_nelkul_es_abra_a_szoveg_szelen():
    assert n.reszek("csak szöveg\n") == [("md", "csak szöveg\n")]
    assert n.reszek("```mermaid\nx\n```") == [("mermaid", "x\n")]
    assert n.reszek("") == []


def test_reszek_tobb_abra():
    r = n.reszek("a\n```mermaid\n1\n```\nb\n```mermaid\n2\n```\nc")
    assert [t for t, _ in r] == ["md", "mermaid", "md", "mermaid", "md"]


def test_mas_nyelvu_kodblokkot_nem_vag_ki():
    s = "```python\nx = 1\n```\n"
    assert n.reszek(s) == [("md", s)]


def test_csak_a_modell_dokumentumaban_van_abra():
    abras = {d.rel for d in DOKUMENTUMOK if any(t == "mermaid" for t, _ in n.reszek(d.szoveg()))}
    assert abras == {"koncepcio/00-mukodesi-modell.md"}


# --- az oldalak ----------------------------------------------------------------------------


@pytest.mark.parametrize("doc", DOKUMENTUMOK, ids=lambda d: d.url)
def test_minden_dokumentumoldal_lefut_es_mutatja_a_cimet_es_a_forrasfajlt(doc):
    at = oldal(doc)
    assert f"# {doc.cim}" in szoveg(at)
    assert at.caption[-1].value == f"Forrásfájl: `{doc.rel}`"


@pytest.mark.parametrize("doc", DOKUMENTUMOK, ids=lambda d: d.url)
def test_egyetlen_dokumentumban_sem_marad_nyers_md_link_vagy_fajlnev_tartalek(doc):
    s = szoveg(oldal(doc))
    assert not re.search(r"\]\([^)#][^)]*\.md", s), "nyers .md link maradt"
    assert not re.search(r"\(`[^`]*\.md`\)", s), "fájlnév-tartalék maradt: a link nem oldódott fel"


def test_a_xyo_pelda_linkjei_ugyanabban_a_lapban_nyilnak():
    s = szoveg(oldal(next(d for d in DOKUMENTUMOK if d.url == "04-xyo-pelda")))
    assert '<a href="tudasbazis?szocikk=pl" target="_self">P&amp;L</a>' in s or '<a href="tudasbazis?szocikk=pl" target="_self">P&L</a>' in s
    assert '<a href="01-kapuk-es-kill-criteria" target="_self">' in s
    assert '<a href="02-meresi-rendszer" target="_self">' in s
    assert '<a href="tudasbazis?szocikk=provider-and-deployer" target="_self">' in s
    assert "](tudasbazis" not in s  # nincs markdown-link (az új lapot nyitna)


def test_a_forrasjegyzek_url_jei_szovegkent_megmaradnak():
    s = szoveg(oldal(next(d for d in DOKUMENTUMOK if d.url == "forrasok")))
    assert "https://www.pmi.org/learning/thought-leadership/future-of-project-work" in s


def blokkok(csomopont, kulcs=None):
    """Az AppTest-fa blokkjai (kulcsos konténerek), mélységi sorrendben."""
    for gyerek in getattr(csomopont, "children", {}).values():
        if getattr(gyerek, "key", None) and (kulcs is None or gyerek.key == kulcs):
            yield gyerek
        yield from blokkok(gyerek, kulcs)


def graphviz_a_blokkban(blokk):
    return [e for e in blokk.children.values() if e.type == "graphviz_chart"]


def test_a_modell_abraja_kirajzolodik():
    doc = next(d for d in DOKUMENTUMOK if d.url == "00-mukodesi-modell")
    at = oldal(doc)
    forras = next(t for tip, t in n.reszek(doc.szoveg()) if tip == "mermaid")
    abrak = at.get("graphviz_chart")
    assert len(abrak) == 1
    assert abrak[0].proto.spec == mermaid.dot(forras) and "rankdir=LR;" in abrak[0].proto.spec
    assert "```mermaid" not in szoveg(at)  # nem marad nyers kódblokk


def test_az_abra_a_cssben_hivatkozott_konteneren_belul_van():
    """A CSS-osztály (st-key-<kulcs>) és a konténer kulcsa egyezik: különben keskeny képernyőn nem görgethető."""
    doc = next(d for d in DOKUMENTUMOK if d.url == "00-mukodesi-modell")
    at = oldal(doc)
    css = next(m.value for m in at.markdown if m.value.startswith("<style>"))
    abra = next(blokkok(at.main, "abra-0"))
    assert [g.proto.spec for g in graphviz_a_blokkban(abra)] == [at.get("graphviz_chart")[0].proto.spec]
    assert config.KESKENY_PX == 700 and n.ABRA_SZELESSEG_PX == 1000
    assert "@media (max-width: 700px) { .st-key-abra-0 { overflow-x: auto; } " in css
    assert '.st-key-abra-0 [data-testid="stGraphVizChart"], .st-key-abra-0 [data-testid="stGraphVizChart"] svg { min-width: 1000px; } }' in css
    assert "@media (min-width: 701px) { .st-key-abra-tipp-0 { display: none; } }" in css
    assert next(m for m in at.markdown if m.value == css).proto.allow_html


def test_a_gorgetesi_tipp_csak_keskeny_kepernyon_latszik():
    at = oldal(next(d for d in DOKUMENTUMOK if d.url == "00-mukodesi-modell"))
    tipp = next(blokkok(at.main, "abra-tipp-0"))
    assert [c.value for c in tipp.children.values()] == ["Az ábra vízszintesen görgethető."]


def test_egy_dokumentum_tobb_abraja_kulon_sorszamot_kap():
    """A valódi dokumentumban egy ábra van; a nézet több ábrát is helyesen számoz."""
    script = (
        "from unittest import mock\n"
        "from hibrid_app import dokumentum_nezet, dokumentumok\n"
        "szoveg = '# C\\n\\n```mermaid\\nflowchart LR\\nA --> B\\n```\\n\\nközte\\n\\n```mermaid\\nflowchart LR\\nC --> D\\n```\\n'\n"
        "doc = dokumentumok.lista()[0]\n"
        "with mock.patch.object(dokumentumok.Dokumentum, 'szoveg', return_value=szoveg):\n"
        "    dokumentum_nezet.make_view(doc)()\n"
    )
    at = AppTest.from_string(script, default_timeout=60).run()
    assert not at.exception, at.exception
    assert [b.key for b in blokkok(at.main)] == ["abra-0", "abra-tipp-0", "abra-1", "abra-tipp-1"]
    assert len(at.get("graphviz_chart")) == 2
    css = "".join(m.value for m in at.markdown if m.value.startswith("<style>"))
    assert ".st-key-abra-0 " in css and ".st-key-abra-1 " in css  # mindkét ábrának saját CSS-e van


def test_tobb_abra_kulon_kulcsot_kap():
    script = (
        "from hibrid_app import dokumentum_nezet\n"
        "dokumentum_nezet.abra('flowchart LR\\nA --> B', 0)\n"
        "dokumentum_nezet.abra('flowchart LR\\nC --> D', 1)\n"
    )
    at = AppTest.from_string(script, default_timeout=60).run()
    assert not at.exception
    assert [b.key for b in blokkok(at.main)] == ["abra-0", "abra-tipp-0", "abra-1", "abra-tipp-1"]


def test_az_abra_a_tartalom_szelessegere_skalazodik_es_van_alt_szovege():
    """A szélesség és az alt szöveg nincs az elem protójában, ezért a hívást figyeljük."""
    script = (
        "import streamlit as st\n"
        "hivasok = []\n"
        "eredeti = st.graphviz_chart\n"
        "def figyelo(*args, **kwargs):\n"
        "    hivasok.append((args, kwargs))\n"
        "    return eredeti(*args, **kwargs)\n"
        "st.graphviz_chart = figyelo\n"
        "from hibrid_app import dokumentum_nezet\n"
        "dokumentum_nezet.abra('flowchart LR\\nA --> B')\n"
        "st.session_state['hivasok'] = hivasok\n"
    )
    at = AppTest.from_string(script, default_timeout=60).run()
    assert not at.exception
    (_, kwargs), = at.session_state["hivasok"]
    assert kwargs["width"] == "stretch"
    assert kwargs["alt"] == n.ALT and "ábrája" in kwargs["alt"]


def test_abra_nelkuli_oldalon_nincs_graphviz():
    assert len(oldal(next(d for d in DOKUMENTUMOK if d.url == "04-xyo-pelda")).get("graphviz_chart")) == 0


def test_nem_tamogatott_abra_kodblokkra_esik_vissza():
    script = "from hibrid_app import dokumentum_nezet\ndokumentum_nezet.abra('sequenceDiagram\\nA->>B: hi')\n"
    at = AppTest.from_string(script, default_timeout=60).run()
    assert not at.exception
    assert len(at.get("graphviz_chart")) == 0
    assert not any(m.value.startswith("<style>") for m in at.markdown)  # nincs CSS sem
    assert "A->>B: hi" in at.code[0].value
    assert "nem tudja kirajzolni" in at.caption[0].value


def test_a_regiszter_es_a_nezetfuggveny_neve():
    nev = n.make_view(DOKUMENTUMOK[0]).__name__
    assert nev == "dokumentum_00_osszefoglalo"


# --- navigáció -----------------------------------------------------------------------------

LEIRASOK = navigacio.leirasok()


def test_a_navigacio_szekciói_es_sorrendje():
    szekciok = list(dict.fromkeys(o.szekcio for o in LEIRASOK))
    assert szekciok == ["Kezdés", "Kutatás", "Koncepció", "Xyo-minták", "Eszközök"]
    assert [sum(o.szekcio == sz for o in LEIRASOK) for sz in szekciok] == [1, 7, 6, 4, 3]


def test_a_dokumentumoldalak_a_regiszterbol_jonnek():
    for szekcio in ("Kutatás", "Koncepció", "Xyo-minták"):
        assert [(o.url, o.cim) for o in LEIRASOK if o.szekcio == szekcio] == [
            (d.url, d.cim) for d in DOKUMENTUMOK if d.szekcio == szekcio
        ]
    assert [o.cim for o in LEIRASOK if o.szekcio == "Kutatás"][1] == "1. A hibrid megközelítés a piacon"


def test_az_utak_egyediek_es_pontosan_egy_az_alapertelmezett():
    utak = [o.url for o in LEIRASOK if o.url is not None]
    assert len(utak) == len(set(utak))
    assert [o.cim for o in LEIRASOK if o.url is None] == ["Áttekintés"]
    assert {"g1-kapu", "tudasbazis", "mintatar"} <= set(utak)


def test_az_st_page_objektumok_felepulnek_a_leirasokbol():
    oldalak = navigacio.oldalak()
    assert list(oldalak) == ["Kezdés", "Kutatás", "Koncepció", "Xyo-minták", "Eszközök"]
    assert sum(len(v) for v in oldalak.values()) == len(LEIRASOK)
    assert all(isinstance(p, st.Page) for v in oldalak.values() for p in v)


def test_minden_feloldott_link_celja_letezo_oldal():
    """A végpontok közti integritás: amit a feloldás ad, az a navigációban tényleg oldal."""
    utak = {o.url for o in LEIRASOK if o.url is not None}
    szamlalo = 0
    for p in osszes_markdown():
        forras = p.relative_to(ROOT).as_posix()
        for _, cel in relativ_linkek(p):
            url = dokumentumok.feloldas(forras, cel)
            assert re.split(r"[#?]", url)[0] in utak, f"{forras}: {cel} → {url}"
            szamlalo += 1
    assert szamlalo > 150


def test_a_teljes_alkalmazas_lefut_az_uj_navigacioval():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception, at.exception


def test_az_alapertelmezett_oldal_jelolese():
    """Az `st.Page` futtatókörnyezet nélkül csak privát attribútumon árulja el (a Streamlit amúgy az
    elsőt venné alapértelmezettnek, ezért ez viselkedésben nem látszik)."""
    oldalak = [p for v in navigacio.oldalak().values() for p in v]
    assert [p._default for p in oldalak] == [True] + [False] * (len(oldalak) - 1)  # csak az Áttekintés


# --- a HTML-linkek csak engedélyezett HTML-lel működnek -------------------------------------


def html_linkes_elemek(at: AppTest):
    return [m for m in at.markdown if '<a href="' in m.value]


def test_a_dokumentumoldal_html_linkjei_engedelyezett_html_ben_vannak():
    elemek = html_linkes_elemek(oldal(next(d for d in DOKUMENTUMOK if d.url == "04-xyo-pelda")))
    assert elemek
    assert all(m.proto.allow_html for m in elemek)  # különben nyers szövegként látszanának


def test_a_tudasbazis_html_linkjei_engedelyezett_html_ben_vannak():
    at = AppTest.from_string(
        "from hibrid_app import tudasbazis_nezet\ntudasbazis_nezet.tudasbazis()\n", default_timeout=60
    ).run()
    elemek = html_linkes_elemek(at)
    assert elemek and all(m.proto.allow_html for m in elemek)


def test_a_mintatar_html_linkjei_engedelyezett_html_ben_vannak():
    at = AppTest.from_string(
        "from hibrid_app import mintatar_nezet\nmintatar_nezet.mintatar_oldal()\n", default_timeout=60
    ).run()
    elemek = html_linkes_elemek(at)
    assert elemek and all(m.proto.allow_html for m in elemek)
