"""A mintatár oldala: az üres minták letölthetően, megtekinthetően, kitöltési útmutatóval."""

import streamlit as st

from hibrid_app import dokumentumok, mintatar, tudasbazis

K_ZIP = "letolt_zip"


def kulcs(minta: mintatar.Minta) -> str:
    return f"letolt_{minta.fajl}"


def _megjelenit(szoveg: str, forras: str) -> str:
    """A minta markdownja lefokozott címsorokkal, a relatív linkek a felület oldalaira mutatnak
    (`forras`: a minta repó-relatív útja, ehhez képest oldódnak fel)."""
    return tudasbazis.linkek_atirasa(
        mintatar.lefokoz(szoveg), None, lambda hivatkozas: dokumentumok.feloldas(forras, hivatkozas)
    )


def _kitoltott_sor(minta: mintatar.Minta) -> str:
    """„Kitöltött példa” sor: az oldalon belüli (ugyanabban a lapban nyíló) link a példa oldalára."""
    linkek = []
    for rel in minta.kitoltott:
        dok = next((d for d in dokumentumok.lista() if d.rel == rel), None)
        if dok:
            linkek.append(f'<a href="{dok.url}" target="_self">{dok.cim}</a>')
    return "**Kitöltött példa:** " + ", ".join(linkek) if linkek else ""


def mintatar_oldal() -> None:
    mintak = mintatar.katalogus()

    st.title("Mintatár")
    st.write(
        "Minden újrahasznosítható dokumentumhoz egy **üres minta** tartozik kitöltési útmutatóval. A "
        "kitöltött változatot a Xyo-példa mutatja. Egy minta három részből áll: használat, a minta "
        "maga, és mezőnként a kitöltési útmutató (mit írj bele · példa · tipikus hiba)."
    )
    st.download_button(
        f"Mind az {len(mintak)} minta (zip)",
        data=mintatar.csomag,  # csak kattintáskor épül
        file_name="hibrid-pm-sablonok.zip",
        mime="application/zip",
        icon=":material/folder_zip:",
        key=K_ZIP,
    )
    with st.expander("Hogyan használd jól"):
        st.markdown(mintatar.hasznalati_szabalyok())

    for minta in mintak:
        with st.container(border=True):
            st.subheader(minta.cim, anchor=minta.fajl.removesuffix(".md"))
            st.markdown(
                f"**Mire való:** {minta.mire}\n\n**Mikor:** {minta.mikor}\n\n"
                f"**Melyik kapuhoz:** {minta.kapu}\n\n**Ki tölti ki:** {minta.ki}"
            )
            if pelda := _kitoltott_sor(minta):
                st.markdown(pelda, unsafe_allow_html=True)
            st.download_button(
                "Letöltés (.md)",
                data=minta.bajtok(),
                file_name=minta.fajl,
                mime="text/markdown",
                icon=":material/download:",
                key=kulcs(minta),
            )
            with st.expander("Megnézem: a minta és a kitöltési útmutató"):
                forras = f"koncepcio/sablonok/{minta.fajl}"
                minta_resz, utmutato = mintatar.szetbont(minta.szoveg())
                ful_minta, ful_utmutato = st.tabs(["A minta", "Kitöltési útmutató"])
                with ful_minta:
                    st.markdown(_megjelenit(mintatar.torzs(minta_resz), forras), unsafe_allow_html=True)
                with ful_utmutato:
                    st.markdown(
                        _megjelenit(utmutato.removeprefix(mintatar.UTMUTATO_FEJLEC).lstrip("\n"), forras),
                        unsafe_allow_html=True,
                    )
