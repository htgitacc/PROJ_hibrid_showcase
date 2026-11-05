"""Hibrid PM — Streamlit belépőpont.

Indítás:  .venv/bin/streamlit run app.py   (a portot a parancssorban add meg, nincs rögzítve)
"""

import streamlit as st

from hibrid_app import arculat, config, navigacio

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=":material/hub:",
    layout="wide",
    initial_sidebar_state="auto",
)

arculat.oldal_css()
navigation = st.navigation(navigacio.oldalak(), expanded=True)
navigation.run()
