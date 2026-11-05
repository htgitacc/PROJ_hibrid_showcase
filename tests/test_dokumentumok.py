"""A dokumentumregiszter és a hivatkozás-feloldás; őr teszt a valódi dokumentumok minden linkjére."""

import re
from urllib.parse import unquote

import pytest

from hibrid_app import config, mintatar, tudasbazis
from hibrid_app import dokumentumok as d
from tests.conftest import ROOT

DOKUMENTUMOK = d.lista()
LINK = re.compile(r"\[([^\]]+)\]\(([^)]*)\)")


# --- regiszter -----------------------------------------------------------------------------


def test_a_regiszter_sorrendje_es_szekcioi():
    assert [x.rel for x in DOKUMENTUMOK] == [
        "kutatas/00-osszefoglalo.md", "kutatas/01-hibrid-a-piacon.md",
        "kutatas/02-miert-buknak-el-az-ai-projektek.md", "kutatas/03-ai-projektmodszertanok.md",
        "kutatas/04-szabalyozas.md", "kutatas/05-meres-es-ertekeles.md", "kutatas/forrasok.md",
        "koncepcio/README.md", "koncepcio/00-mukodesi-modell.md", "koncepcio/01-kapuk-es-kill-criteria.md",
        "koncepcio/02-meresi-rendszer.md", "koncepcio/03-szerepek.md", "koncepcio/04-xyo-pelda.md",
        "koncepcio/xyo-mintak/adatleltar.md", "koncepcio/xyo-mintak/ai-act-besorolasi-lap.md",
        "koncepcio/xyo-mintak/celkartyak.md", "koncepcio/xyo-mintak/kapudontesek.md",
    ]  # fmt: skip
    assert [x.szekcio for x in DOKUMENTUMOK] == [d.KUTATAS] * 7 + [d.KONCEPCIO] * 6 + [d.XYO_MINTAK] * 4


def test_a_tudasbazis_es_a_sablonok_nincsenek_a_regiszterben():
    rel = {x.rel for x in DOKUMENTUMOK}
    assert d.TUDASBAZIS_FAJL not in rel
    assert not any(r.startswith("koncepcio/sablonok/") for r in rel)


def test_minden_kitoltott_minta_a_regiszterben_van_es_minden_mintahoz_tartozik_egy():
    """Az `xyo-mintak/` fájljai és a `KITOLTOTT` megfeleltetés egymást őrzi, mindkét irányban."""
    rel = {x.rel for x in DOKUMENTUMOK}
    hivatkozott = {r for t in mintatar.KITOLTOTT.values() for r in t}
    assert hivatkozott <= rel
    assert {r for r in rel if r.startswith(d.XYO_MINTAK_MAPPA + "/")} <= hivatkozott
    assert set(mintatar.KITOLTOTT) == {m.fajl for m in mintatar.katalogus()}


def test_az_utak_egyediek_es_nem_utkoznek_a_tobbi_oldallal():
    utak = [x.url for x in DOKUMENTUMOK]
    assert len(utak) == len(set(utak))
    assert not set(utak) & d.FOGLALT_UTAK
    assert all(re.fullmatch(r"[a-z0-9-]+", u) for u in utak)  # nincs vezető /, nincs speciális karakter


def test_a_koncepcio_readme_utja_koncepcio():
    assert next(x.url for x in DOKUMENTUMOK if x.rel == "koncepcio/README.md") == "koncepcio"
    assert next(x.url for x in DOKUMENTUMOK if x.rel == "kutatas/04-szabalyozas.md") == "04-szabalyozas"


@pytest.mark.parametrize("dok", DOKUMENTUMOK, ids=lambda x: x.url)
def test_a_cim_a_fajl_elso_cimsora(dok):
    elso = dok.szoveg().splitlines()[0]
    assert elso.startswith("# ") and dok.cim == elso[2:].strip()


def test_cim_tartalek_ha_nincs_cimsor():
    assert d._cim("nincs cím\nsemmi", "tartalék") == "tartalék"
    assert d._cim("szöveg\n# Cím itt\n## más", "x") == "Cím itt"


# --- feloldás ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("forras", "href", "vart"),
    [
        # a tudásbázis, bárhonnan
        ("kutatas/02-miert-buknak-el-az-ai-projektek.md", "tudasbazis.md#dpia", "tudasbazis?szocikk=dpia"),
        ("koncepcio/04-xyo-pelda.md", "../kutatas/tudasbazis.md#kill-criteria", "tudasbazis?szocikk=kill-criteria"),
        ("koncepcio/sablonok/celkartya.md", "../../kutatas/tudasbazis.md#baseline", "tudasbazis?szocikk=baseline"),
        ("koncepcio/04-xyo-pelda.md", "../kutatas/tudasbazis.md", "tudasbazis"),
        # dokumentumok
        ("kutatas/00-osszefoglalo.md", "01-hibrid-a-piacon.md", "01-hibrid-a-piacon"),
        ("koncepcio/00-mukodesi-modell.md", "../kutatas/02-miert-buknak-el-az-ai-projektek.md",
         "02-miert-buknak-el-az-ai-projektek"),
        ("koncepcio/sablonok/celkartya.md", "../04-xyo-pelda.md", "04-xyo-pelda"),
        ("kutatas/00-osszefoglalo.md", "../koncepcio/README.md", "koncepcio"),
        ("kutatas/00-osszefoglalo.md", "01-hibrid-a-piacon.md#12-jobb-e", "01-hibrid-a-piacon#12-jobb-e"),
        ("koncepcio/01-kapuk-es-kill-criteria.md", "02-meresi-rendszer.md", "02-meresi-rendszer"),
        # sablonok → mintatár
        ("koncepcio/README.md", "sablonok/", "mintatar"),
        ("koncepcio/README.md", "sablonok/README.md", "mintatar"),
        ("koncepcio/README.md", "sablonok/meroszamkartya.md", "mintatar#meroszamkartya"),
        ("koncepcio/sablonok/README.md", "ai-act-besorolasi-lap.md", "mintatar#ai-act-besorolasi-lap"),
        ("koncepcio/sablonok/kapudontes.md", "adatleltar.md", "mintatar#adatleltar"),
    ],
)
def test_feloldas(forras, href, vart):
    assert d.feloldas(forras, href) == vart


@pytest.mark.parametrize(
    ("forras", "href"),
    [
        ("kutatas/00-osszefoglalo.md", "https://example.org/x"),
        ("kutatas/00-osszefoglalo.md", "mailto:valaki@example.org"),
        ("kutatas/00-osszefoglalo.md", "#szakasz"),  # dokumentumon belüli
        ("kutatas/00-osszefoglalo.md", ""),
        ("kutatas/00-osszefoglalo.md", "nincs-ilyen.md"),
        ("kutatas/00-osszefoglalo.md", "../docs/adr/0001-harmadik-modell-hibrid-rag-xyo.md"),  # nem a felületen él
        ("koncepcio/README.md", "sablonok/nincs-ilyen.md"),
        ("kutatas/00-osszefoglalo.md", "../../../etc/passwd"),  # a repón kívülre mutató útvonal
        ("kutatas/00-osszefoglalo.md", "tudasbazis.md.exe"),
        # külső URL-nek látszó cél nem oldódhat fel, akkor sem, ha az útvonal-normalizálás a repóba vinné
        ("README.md", "http:/../kutatas/tudasbazis.md"),
        # üres link és #horgony a sablonok mappájából nem oldódhat fel a mappa saját útvonalára
        ("koncepcio/sablonok/README.md", ""),
        ("koncepcio/sablonok/README.md", "#x"),
    ],
)
def test_nem_feloldhato(forras, href):
    assert d.feloldas(forras, href) is None


def test_a_tudasbazis_szocikk_parametere_url_kodolt():
    assert d.feloldas("kutatas/00-osszefoglalo.md", "tudasbazis.md#kis szó&x") == "tudasbazis?szocikk=kis%20sz%C3%B3%26x"


def test_az_url_relativ_nincs_vezeto_perjel():
    for forras, href in [("kutatas/00-osszefoglalo.md", "tudasbazis.md#x"), ("koncepcio/README.md", "sablonok/")]:
        assert not d.feloldas(forras, href).startswith("/")


# --- őr: a valódi dokumentumok minden relatív linkje működik -------------------------------


def osszes_markdown():
    return sorted(
        [*config.KUTATAS_DIR.glob("*.md"), *config.KONCEPCIO_DIR.glob("*.md"), *config.SABLONOK_DIR.glob("*.md")]
    )


def relativ_linkek(p):
    for nev, cel in LINK.findall(p.read_text(encoding="utf-8")):
        if not (cel.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", cel)):
            yield nev, cel


def test_a_dokumentumok_minden_relativ_linkje_feloldhato():
    """„Működő belső linkek”: ha egy új link nem a felületre vagy létező célra mutat, a teszt jelzi."""
    hibak = []
    for p in osszes_markdown():
        forras = p.relative_to(ROOT).as_posix()
        for nev, cel in relativ_linkek(p):
            if d.feloldas(forras, cel) is None:
                hibak.append(f"{forras}: [{nev}]({cel})")
    assert not hibak, "\n".join(hibak)


def test_a_linkek_szama_nem_nulla():
    """Az őr teszt ne legyen üres: a dokumentumok valóban sok linket tartalmaznak."""
    db = sum(1 for p in osszes_markdown() for _ in relativ_linkek(p))
    assert db > 100


def test_minden_tudasbazis_horgony_letezik():
    horgonyok = {s.horgony for s in tudasbazis.betolt()}
    szamlalo = 0
    for p in osszes_markdown():
        forras = p.relative_to(ROOT).as_posix()
        for _, cel in relativ_linkek(p):
            url = d.feloldas(forras, cel)
            if url and url.startswith("tudasbazis?szocikk="):
                szamlalo += 1
                assert unquote(url.split("=", 1)[1]) in horgonyok, f"{forras}: {cel}"
    assert szamlalo > 80


def test_minden_mintatar_horgony_letezik():
    stemek = {m.fajl.removesuffix(".md") for m in mintatar.katalogus()}
    for p in osszes_markdown():
        forras = p.relative_to(ROOT).as_posix()
        for _, cel in relativ_linkek(p):
            url = d.feloldas(forras, cel)
            if url and url.startswith("mintatar#"):
                assert url.split("#")[1] in stemek, f"{forras}: {cel}"
