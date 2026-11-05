"""Az oldalak és az oldalsáv felépítése (az `app.py` hívja, a tesztek is innen olvasnak)."""

from collections.abc import Callable
from dataclasses import dataclass

import streamlit as st

from hibrid_app import (
    dokumentum_nezet,
    dokumentumok,
    kapu_nezet,
    mintatar_nezet,
    tudasbazis_nezet,
    views,
)

KEZDES = "Kezdés"
ESZKOZOK = "Eszközök"


@dataclass(frozen=True)
class Oldal:
    """Egy oldal leírása; az `st.Page`-et csak az `oldalak()` építi belőle (az nem olvasható
    futtatókörnyezet nélkül, a leírás igen)."""

    szekcio: str
    cim: str
    url: str | None  # None: az alapértelmezett oldal, a gyökér-URL-en
    nezet: Callable[[], None]
    ikon: str


def leirasok() -> list[Oldal]:
    """Az oldalak sorrendben: kezdés, kutatás, koncepció, eszközök."""
    oldalak = [Oldal(KEZDES, "Áttekintés", None, views.overview, ":material/home:")]
    oldalak += [
        Oldal(d.szekcio, d.cim, d.url, dokumentum_nezet.make_view(d), ":material/article:")
        for d in dokumentumok.lista()
    ]
    oldalak += [
        Oldal(ESZKOZOK, "G1 — PoC-kapu", "g1-kapu", kapu_nezet.g1_kapu, ":material/rule:"),
        Oldal(ESZKOZOK, "Tudásbázis", "tudasbazis", tudasbazis_nezet.tudasbazis, ":material/menu_book:"),
        Oldal(ESZKOZOK, "Mintatár", "mintatar", mintatar_nezet.mintatar_oldal, ":material/download:"),
    ]
    return oldalak


def oldalak() -> dict[str, list[st.Page]]:
    """Szekciónként az `st.Page`-ek (a szekciók a `leirasok()` sorrendjében)."""
    szekciok: dict[str, list[st.Page]] = {}
    for o in leirasok():
        oldal = st.Page(o.nezet, title=o.cim, icon=o.ikon, url_path=o.url, default=o.url is None)
        szekciok.setdefault(o.szekcio, []).append(oldal)
    return szekciok
