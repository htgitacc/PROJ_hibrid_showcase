"""Egy dokumentum oldala: a markdown, működő belső linkekkel és kirajzolt Mermaid-ábrákkal."""

import re
from collections.abc import Callable

import streamlit as st

from hibrid_app import config, dokumentumok, mermaid, tudasbazis

_ABRA = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)


def reszek(szoveg: str) -> list[tuple[str, str]]:
    """A szöveg sorrendben: ("md", markdown) és ("mermaid", forráskód) részekre bontva."""
    kimenet, hol = [], 0
    for m in _ABRA.finditer(szoveg):
        if m.start() > hol:
            kimenet.append(("md", szoveg[hol : m.start()]))
        kimenet.append(("mermaid", m.group(1)))
        hol = m.end()
    if hol < len(szoveg):
        kimenet.append(("md", szoveg[hol:]))
    return kimenet


ABRA_SZELESSEG_PX = 1000  # a természetes méret (az ábra ennyi pixelen olvasható)
ALT = "A dokumentum ábrája; a szöveges tartalma a dokumentumban is szerepel."


def abra(forras: str, sorszam: int = 0) -> None:
    """Kirajzolja a Mermaid-ábrát; ha az átalakító nem érti, a forráskódot mutatja.

    Széles képernyőn az ábra a tartalom szélességére skálázódik. Keskeny képernyőn a skálázás
    olvashatatlanul kicsire venné a szöveget, ezért ott természetes méretben jelenik meg, és
    vízszintesen görgethető (CSS-lekérdezés, nincs hozzá JavaScript).
    """
    try:
        dot = mermaid.dot(forras)
    except ValueError:
        st.code(forras, language="text")
        st.caption("Ezt az ábrát a felület nem tudja kirajzolni, ezért a forráskódja látszik (GitHubon kirajzolódik).")
        return
    osztaly = f".st-key-abra-{sorszam}"
    st.markdown(
        "<style>"
        f"@media (max-width: {config.KESKENY_PX}px) {{ {osztaly} {{ overflow-x: auto; }} "
        f'{osztaly} [data-testid="stGraphVizChart"], {osztaly} [data-testid="stGraphVizChart"] svg '
        f"{{ min-width: {ABRA_SZELESSEG_PX}px; }} }}"
        f"@media (min-width: {config.KESKENY_PX + 1}px) {{ .st-key-abra-tipp-{sorszam} {{ display: none; }} }}"
        "</style>",
        unsafe_allow_html=True,
    )
    with st.container(key=f"abra-{sorszam}"):
        st.graphviz_chart(dot, width="stretch", alt=ALT)
    with st.container(key=f"abra-tipp-{sorszam}"):
        st.caption("Az ábra vízszintesen görgethető.")


def make_view(doc: dokumentumok.Dokumentum) -> Callable[[], None]:
    """A dokumentum nézetfüggvénye (az `st.Page` hívja)."""

    def view() -> None:
        def url(hivatkozas: str) -> str | None:
            return dokumentumok.feloldas(doc.rel, hivatkozas)

        abrak = 0
        for tipus, tartalom in reszek(doc.szoveg()):
            if tipus == "mermaid":
                abra(tartalom, abrak)
                abrak += 1
            else:
                st.markdown(tudasbazis.linkek_atirasa(tartalom, None, url), unsafe_allow_html=True)
        st.caption(f"Forrásfájl: `{doc.rel}`")

    view.__name__ = f"dokumentum_{doc.url.replace('-', '_')}"
    return view
