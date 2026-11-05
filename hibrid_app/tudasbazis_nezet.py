"""A tudásbázis oldala: kereshető, kategóriánként szűrhető, belső linkekkel."""

import streamlit as st

from hibrid_app import dokumentumok
from hibrid_app import tudasbazis as tb

K_KERES = "tb_keres"
K_KATEGORIA = "tb_kategoria"
PARAMETER = "szocikk"  # ?szocikk=<horgony>: a szócikk kiemelve, felül (másik oldalról érkező link)
MINDEN = "Minden kategória"


@st.cache_data
def _betolt(mtime: float) -> list[tb.Szocikk]:
    """A fájl módosítási ideje a gyorsítótár kulcsa: szerkesztés után az oldal újratölt."""
    return tb.betolt()


def _torzs(s: tb.Szocikk, lathato: set[str], url) -> str:
    return "\n\n".join(f"**{nev}:** {tb.linkek_atirasa(t, lathato, url)}" for nev, t in s.mezok)


def _teljes_lista() -> None:
    st.query_params.clear()


def tudasbazis() -> None:
    szocikkek = _betolt(tb.FAJL.stat().st_mtime)
    kategoriak = tb.kategoriak(szocikkek)

    st.title("Tudásbázis")
    st.write(
        "A szakszavak **angolul maradnak**, mert így szerepelnek a szakirodalomban, az eszközökben és az "
        "álláshirdetésekben. Itt az áll, mit jelentenek, hol találkozol velük ebben a modellben, és "
        "mutatóknál **hogyan kell olvasni** őket."
    )

    kert = st.query_params.get(PARAMETER)
    if kert:
        szocikk = next((x for x in szocikkek if x.horgony == kert), None)
        if szocikk is None:
            st.warning(f"Nincs „{kert}” nevű szócikk a tudásbázisban.")
        else:
            with st.container(border=True):
                st.caption("Kiválasztott szócikk")
                st.subheader(szocikk.cim, anchor=False)
                st.markdown(
                    _torzs(szocikk, {x.horgony for x in szocikkek}, lambda h: dokumentumok.feloldas(tb.FAJL_REL, h)),
                    unsafe_allow_html=True,
                )
                st.button("Az összes szócikk", on_click=_teljes_lista, key="tb_osszes")

    c1, c2 = st.columns([3, 2])
    szoveg = c1.text_input("Keresés (címben és szövegben, ékezet nélkül is)", key=K_KERES)
    kategoria = c2.selectbox("Kategória", [MINDEN, *kategoriak], key=K_KATEGORIA)

    talalatok = tb.keres(szocikkek, szoveg, None if kategoria == MINDEN else kategoria)
    st.caption(f"{len(talalatok)} szócikk a {len(szocikkek)}-ből.")
    if not talalatok:
        st.info("Nincs találat. Próbálj rövidebb szót, vagy válaszd a „Minden kategória” lehetőséget.")
        return

    lathato = {s.horgony for s in talalatok}

    def url(hivatkozas: str) -> str | None:
        return dokumentumok.feloldas(tb.FAJL_REL, hivatkozas)

    with st.expander("Ugrás szócikkre"):
        for kat in kategoriak:
            cimek = [s for s in talalatok if s.kategoria == kat]
            if cimek:
                st.markdown(f"**{kat}:** " + " · ".join(f"[{s.cim}](#{s.horgony})" for s in cimek))

    for kat in kategoriak:
        csoport = [s for s in talalatok if s.kategoria == kat]
        if not csoport:
            continue
        st.header(kat, anchor=False)
        for s in csoport:
            st.subheader(s.cim, anchor=s.horgony)
            st.markdown(_torzs(s, lathato, url), unsafe_allow_html=True)  # <a target="_self"> linkek
