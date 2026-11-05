"""Az oldalak nézetfüggvényei. Minden nézet önállóan futtatható (a tesztek így hívják)."""

import streamlit as st

from hibrid_app import config


def link(szoveg: str, url: str) -> str:
    """Másik oldalra mutató link ugyanabban a lapban (a sima markdown-link új lapot nyitna)."""
    return f'<a href="{url}" target="_self">{szoveg}</a>'


# (szekció, leírás sablon): a {…} helyére az oldal linkje kerül. Az útvonalak a navigációból
# valók; a `tests/test_views.py` őrzi, hogy mind létező oldalra mutat.
TARTALOM = (
    (
        "Kutatás",
        (
            "hat dokumentum és a forrásjegyzék: mennyire elterjedt a hibrid, miért buknak el az AI-projektek, "
            "milyen módszertanok vannak, mit szabályoz az AI Act, hogyan mérjük egy RAG-asszisztenst. "
            "Minden szám mellett forrás áll. Kezdd az {osszefoglalo}."
        ),
    ),
    (
        "Koncepció",
        (
            "a működési modell, a kapuk és leállítási feltételek, a mérési rendszer, a szerepek, és a Xyo "
            "Tudásasszisztens végigvezetve a modellen. Kezdd a {modell} vagy a {pelda}."
        ),
    ),
    (
        "G1 — PoC-kapu",
        (
            "kipróbálható: a Xyo mérései és csúszkák, a kapu döntése (go, pivot, no-go). Itt látszik, "
            "mikor fordul át a döntés. {kapu}."
        ),
    ),
    (
        "Tudásbázis",
        (
            "a szakszavak angolul, magyarázattal: mit jelent, hol fordul elő, hogyan kell olvasni. "
            "Kereshető. {tudasbazis}."
        ),
    ),
    (
        "Mintatár",
        (
            "üres, letölthető minták kitöltési útmutatóval: mérőszámkártya, célkártya, kapudöntés, "
            "adatleltár, AI Act-besorolási lap. {mintatar}."
        ),
    ),
)

LINKEK = {
    "osszefoglalo": ("összefoglalóval", "00-osszefoglalo"),
    "modell": ("működési modellel", "00-mukodesi-modell"),
    "pelda": ("Xyo-példával", "04-xyo-pelda"),
    "kapu": ("Megnyitom a kaput", "g1-kapu"),
    "tudasbazis": ("Megnyitom a tudásbázist", "tudasbazis"),
    "mintatar": ("Megnyitom a mintatárat", "mintatar"),
}


def overview() -> None:
    """Nyitóoldal: mi ez, és mit hol találsz."""
    st.title(config.APP_TITLE)
    st.write(
        "Hibrid projektmenedzsment-modell egy AI-projekten: prediktív keret, "
        "mérőszám-kapukkal vezérelt kísérleti szakasz, és a PoC-kapu utáni kettéválás "
        "(prediktív bevezetés + agilis termékfolyamat). A mintaprojekt a Xyo Tudásasszisztens."
    )
    st.subheader("Mit találsz itt?")
    linkek = {kulcs: link(szoveg, url) for kulcs, (szoveg, url) in LINKEK.items()}
    st.markdown(
        "\n".join(f"- **{szekcio}**: {leiras.format(**linkek)}" for szekcio, leiras in TARTALOM),
        unsafe_allow_html=True,
    )
    st.caption("A számok és a küszöbök a Xyo-példa feltevései, nem iparági szabványok.")
