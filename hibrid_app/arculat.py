"""Az egész alkalmazásra érvényes, szűk képernyős kiegészítő CSS.

A markdown-táblázatok (a dokumentumokban sok az oszlop) szűk képernyőn az egész oldalt oldalra
tolnák; ezért saját vízszintes görgetést kapnak. A médialekérdezésen kívül egyetlen szabály van: a
legalább `SZELES_TABLA_OSZLOP` oszlopos táblák (pl. az adatleltár 9 oszlopa) asztali szélességen is
szélesebbek lehetnek az oldalnál. Minden más táblázat asztali nézete nem változik.
"""

import streamlit as st

from hibrid_app import config

SZELES_TABLA_OSZLOP = 7

SZUK_KEPERNYO_CSS = f"""<style>
[data-testid="stMarkdownContainer"] table:has(th:nth-child({SZELES_TABLA_OSZLOP})) {{
  display: block; max-width: 100%; overflow-x: auto;
}}
@media (max-width: {config.KESKENY_PX}px) {{
  [data-testid="stMarkdownContainer"] table {{ display: block; max-width: 100%; overflow-x: auto; }}
}}
</style>"""


def oldal_css() -> None:
    """Az `app.py` hívja minden futásnál, a navigáció előtt."""
    st.html(SZUK_KEPERNYO_CSS)
