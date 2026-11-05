"""A tudásbázis beolvasása és keresése: a valódi fájlon és szintetikus mintákon."""

import re

import pytest

from hibrid_app import tudasbazis as tb
from tests.conftest import olvas

SZOVEG = olvas("kutatas/tudasbazis.md")
SZOCIKKEK = tb.olvas(SZOVEG)

MINTA = """# Cím

## Bevezető
### Nem szócikk, mert a bevezetőben van, de szócikk-alakú
**Mit jelent:** ez mégis beolvasódik.\\

## Egyik
### Alfa
**Mit jelent:** első sor
második sor ugyanabból a mezőből.\\
**Hol fordul elő:** itt, [Béta](#beta) és [dok](05-x.md#y).\\
**Lásd:** [Béta](#beta).

### Mező nélküli cím
### Béta
**Mit jelent:** a másik.

## Üres
*(A kutatással együtt bővül.)*
"""


# --- a szintetikus minta -------------------------------------------------------------------


def test_minta_szerkezete():
    s = tb.olvas(MINTA)
    # a mezők nélküli „### Mező nélküli cím” nem szócikk
    assert [(x.kategoria, x.cim) for x in s] == [
        ("Bevezető", "Nem szócikk, mert a bevezetőben van, de szócikk-alakú"),
        ("Egyik", "Alfa"),
        ("Egyik", "Béta"),
    ]
    assert tb.kategoriak(s) == ["Bevezető", "Egyik"]  # az üres fejezet kimarad


def test_tobb_soros_mezo_es_sorveg_perjel():
    alfa = tb.olvas(MINTA)[1]
    assert alfa.mezo("Mit jelent") == "első sor második sor ugyanabból a mezőből."
    assert not any(t.endswith("\\") for _, t in alfa.mezok)
    assert [n for n, _ in alfa.mezok] == ["Mit jelent", "Hol fordul elő", "Lásd"]


def test_hianyzo_mezo_ures_szoveg():
    assert tb.olvas(MINTA)[2].mezo("Lásd") == ""


@pytest.mark.parametrize(
    ("cim", "vart"),
    [
        ("Correct refusal rate", "correct-refusal-rate"),
        ("P&L", "pl"),
        ("AI Act", "ai-act"),
        ("Context recall", "context-recall"),
        ("RAG", "rag"),
    ],
)
def test_horgony(cim, vart):
    assert tb.horgony(cim) == vart


# --- a valódi fájl -------------------------------------------------------------------------


def test_minden_szocikk_beolvasodik():
    fejlecek = re.findall(r"^### (.+)$", SZOVEG, re.MULTILINE)
    assert [s.cim for s in SZOCIKKEK] == fejlecek
    assert len(SZOCIKKEK) >= 54


def test_negy_kategoria_a_fajl_sorrendjeben():
    assert tb.kategoriak(SZOCIKKEK) == ["Rövidítések", "Folyamatfogalmak", "Mérési módszerek", "Mutatók"]


def test_kotelezo_mezok_minden_szocikknel():
    for s in SZOCIKKEK:
        for nev in ("Mit jelent", "Hol fordul elő", "Lásd"):
            assert s.mezo(nev), f"{s.cim}: hiányzik a „{nev}” mező"


def test_a_mutatoknal_van_hogyan_olvasd():
    """A tudásbázis szabálya: a mutatóknál ez a lényeges mező."""
    mutatok = [s for s in SZOCIKKEK if s.kategoria == "Mutatók"]
    assert mutatok
    for s in mutatok:
        assert s.mezo("Hogyan olvasd"), s.cim


def test_betuendben_vannak_kategorian_belul():
    for kat in tb.kategoriak(SZOCIKKEK):
        cimek = [s.cim for s in SZOCIKKEK if s.kategoria == kat]
        assert cimek == sorted(cimek, key=str.lower), kat


def test_a_horgonyok_egyediek():
    horgonyok = [s.horgony for s in SZOCIKKEK]
    assert len(horgonyok) == len(set(horgonyok))


def test_minden_belso_link_szocikkre_mutat():
    horgonyok = {s.horgony for s in SZOCIKKEK}
    for s in SZOCIKKEK:
        for _, szoveg in s.mezok:
            for cel in re.findall(r"\]\(#([^)]+)\)", szoveg):
                assert cel in horgonyok, f"{s.cim}: #{cel} nem szócikk"


def test_nincs_sorveg_perjel_a_szovegekben():
    assert not [s.cim for s in SZOCIKKEK if any(t.endswith("\\") for _, t in s.mezok)]


# --- keresés -------------------------------------------------------------------------------


def cimek(talalatok):
    return [s.cim for s in talalatok]


def test_ures_kereses_mindent_visszaad_fajlbeli_sorrendben():
    assert cimek(tb.keres(SZOCIKKEK)) == cimek(SZOCIKKEK)


def test_kategoria_szuro():
    mutatok = tb.keres(SZOCIKKEK, kategoria="Mutatók")
    assert mutatok and {s.kategoria for s in mutatok} == {"Mutatók"}
    assert "Faithfulness" in cimek(mutatok)


def test_kereses_ekezet_es_kisbetu_fuggetlen():
    assert "Faithfulness" in cimek(tb.keres(SZOCIKKEK, "FAITHFULNESS"))
    ekezetes = tb.keres(SZOCIKKEK, "mérés")
    assert len(ekezetes) > 5  # a szó több szócikk szövegében is szerepel
    assert tb.keres(SZOCIKKEK, "meres") == ekezetes == tb.keres(SZOCIKKEK, "MÉRÉS")


def test_minden_szo_kell():
    egy = tb.keres(SZOCIKKEK, "leakage")
    ketto = tb.keres(SZOCIKKEK, "leakage jogosultság")
    assert egy and set(cimek(ketto)) <= set(cimek(egy))
    assert tb.keres(SZOCIKKEK, "leakage zzzzzzzz") == []


def test_kereses_a_mezok_szovegeben_is():
    """A „kill criterion” szó a Stage gate szócikk szövegében szerepel, a címében nem."""
    talalat = {s.cim: s for s in tb.keres(SZOCIKKEK, "kill criteria")}
    assert "Stage gate" in talalat
    assert "kill" not in talalat["Stage gate"].cim.lower()


def test_kategoria_es_szoveg_egyutt():
    mind = tb.keres(SZOCIKKEK, "kapu")
    csak_mutato = tb.keres(SZOCIKKEK, "kapu", "Mutatók")
    assert csak_mutato and set(cimek(csak_mutato)) < set(cimek(mind))
    assert {s.kategoria for s in csak_mutato} == {"Mutatók"}


# --- hivatkozások átírása ------------------------------------------------------------------


def test_lathato_belso_link_marad():
    assert tb.linkek_atirasa("lásd [DPIA](#dpia)", {"dpia"}) == "lásd [DPIA](#dpia)"


def test_rejtett_szocikkre_mutato_link_sima_szoveg():
    assert tb.linkek_atirasa("lásd [DPIA](#dpia)", set()) == "lásd DPIA"


def test_dokumentum_link_url_nelkul_fajlnevvel():
    assert tb.linkek_atirasa("[04](04-szabalyozas.md)", set()) == "04 (`04-szabalyozas.md`)"
    assert tb.linkek_atirasa("[x](04-szabalyozas.md#f)", set()) == "x (`04-szabalyozas.md`)"


def test_dokumentum_link_url_szolgaltatassal_ugyanabban_a_lapban():
    """A másik oldalra mutató link <a target="_self"> (a markdown-link új lapot nyitna)."""
    url = lambda hivatkozas: "dok/" + hivatkozas.removesuffix(".md")
    assert tb.linkek_atirasa("[04](04-szabalyozas.md)", set(), url) == '<a href="dok/04-szabalyozas" target="_self">04</a>'


def test_az_url_html_escape_elt():
    url = lambda hivatkozas: 'a"b<c'
    assert 'href="a&quot;b&lt;c"' in tb.linkek_atirasa("[x](y.md)", set(), url)


def test_lathato_none_minden_horgony_linket_megtart():
    assert tb.linkek_atirasa("[A](#a) [B](#b)", None) == "[A](#a) [B](#b)"
    assert tb.linkek_atirasa("[A](#a) [B](#b)", {"a"}) == "[A](#a) B"


def test_kulso_link_valtozatlan_marad():
    szoveg = "[PMI](https://www.pmi.org/x) és [levél](mailto:a@b.hu) és [HTTP](HTTP://E.ORG)"
    assert tb.linkek_atirasa(szoveg, set()) == szoveg
    assert tb.linkek_atirasa(szoveg, None, lambda h: "nem-hivodhat") == szoveg


def test_tobb_link_egy_szovegben():
    szoveg = "[A](#a), [B](#b) és [C](c.md)"
    assert tb.linkek_atirasa(szoveg, {"a"}) == "[A](#a), B és C (`c.md`)"
