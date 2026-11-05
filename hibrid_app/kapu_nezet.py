"""A G1-kapu oldala: a döntés a mutatókból, csúszkákkal a „mi lett volna, ha” kipróbáláshoz.

A döntés logikája a `kapu.py`-ban van; ez a modul csak bemenetet gyűjt és megjelenít.
"""

from dataclasses import dataclass

import streamlit as st

from hibrid_app import adatok, kapu

SAV_SZIN = {kapu.ZOLD: "green", kapu.SARGA: "orange", kapu.PIROS: "red"}


@dataclass(frozen=True)
class Elotoltes:
    """Egy kiinduló állapot: a Xyo egy mérése és a mellé tartozó emberi ítéletek."""

    nev: str
    meres: adatok.Meres
    pivot_volt: bool = False
    hiba_helye_azonositott: bool = False


ELOTOLTESEK = (
    Elotoltes("Xyo — 3. iteráció (a G1, március 3.)", adatok.ITERACIOK[3], hiba_helye_azonositott=True),
    Elotoltes("Xyo — pivot után (G1', március 19.)", adatok.PIVOT_UTAN, pivot_volt=True),
    Elotoltes("Xyo — 0. iteráció (baseline)", adatok.ITERACIOK[0]),
    Elotoltes("Xyo — 1. iteráció (darabolás)", adatok.ITERACIOK[1]),
    Elotoltes("Xyo — 2. iteráció („csak a forrásból”)", adatok.ITERACIOK[2]),
)
NEVEK = [e.nev for e in ELOTOLTESEK]

# A widgetek kulcsai (a tesztek is ezeket használják).
K_ELOTOLTES = "g1_elotoltes"
K_LEAKAGE = "g1_leakage"
K_FAITHFULNESS = "g1_faithfulness"
K_RECALL = "g1_recall"
K_HELYES = "g1_helyes_elutasitas"
K_TEVES = "g1_teves_elutasitas"
K_LATENCY = "g1_latency"
K_KOLTSEG = "g1_koltseg_kerdesenkent"
K_PIVOT_VOLT = "g1_pivot_volt"
K_HIBAHELY = "g1_hiba_helye"
K_OLCSOBB = "g1_olcsobb_valtozat"
K_ADATMINOSEG = "g1_adatminoseg"


def betolt() -> None:
    """A kiválasztott előtöltés értékeit a csúszkákba írja (a selectbox on_change hívja)."""
    e = ELOTOLTESEK[NEVEK.index(st.session_state[K_ELOTOLTES])]
    m = e.meres
    st.session_state.update(
        {
            K_LEAKAGE: m.szivargas,
            K_FAITHFULNESS: m.faithfulness,
            K_RECALL: m.context_recall,
            K_HELYES: m.helyes_elutasitas,
            K_TEVES: m.teves_elutasitas,
            K_LATENCY: m.latency_p95_s,
            K_KOLTSEG: m.koltseg_ft,
            K_PIVOT_VOLT: e.pivot_volt,
            K_HIBAHELY: e.hiba_helye_azonositott,
            K_OLCSOBB: False,
            K_ADATMINOSEG: False,
        }
    )


def _szazalek(x: float) -> str:
    """„100%”, de „8,3%”: a tizedes csak akkor kell, ha van."""
    return f"{round(x)}%" if x == round(x) else f"{adatok.szam(x, 1)}%"


def _jelzo(sav: str) -> str:
    return f":{SAV_SZIN[sav]}[**{sav}**]"


def _tabla(m: adatok.Meres, eves_koltseg: int, savok: dict[str, str]) -> str:
    """A mutatók, értékük és sávjuk markdown-táblában."""
    helyes_szazalek = 100 * m.helyes_elutasitas / adatok.GOLDEN_ELUTASITANDO
    teves_szazalek = 100 * m.teves_elutasitas / adatok.GOLDEN_MEGVALASZOLHATO
    keret_szazalek = 100 * eves_koltseg / adatok.FUTASI_KERET_EVES
    ertekek = {
        "leakage": f"{m.szivargas}/{adatok.JOGOSULTSAGI_ESETEK} eset",
        "faithfulness": adatok.szam(m.faithfulness),
        "recall": adatok.szam(m.context_recall),
        "refusal": (
            f"{m.helyes_elutasitas}/{adatok.GOLDEN_ELUTASITANDO} ({_szazalek(helyes_szazalek)}); "
            f"téves elutasítás {m.teves_elutasitas}/{adatok.GOLDEN_MEGVALASZOLHATO} "
            f"({_szazalek(teves_szazalek)})"
        ),
        "latency": f"{adatok.szam(m.latency_p95_s, 1)} s",
        "koltseg": (
            f"{m.koltseg_ft} Ft/kérdés → {adatok.szam(eves_koltseg / 1e6, 2)} M Ft/év "
            f"(a keret {adatok.szam(keret_szazalek, 0)}%-a)"
        ),
    }
    sorok = ["| Mutató | Szerep a kapun | Mért érték | Sáv |", "|---|---|---|---|"]
    for mutato in kapu.MUTATOK:
        sorok.append(
            f"| {mutato.nev} | {mutato.szerep} | {ertekek[mutato.kulcs]} | {_jelzo(savok[mutato.kulcs])} |"
        )
    return "\n".join(sorok)


def g1_kapu() -> None:
    """A G1-oldal: előtöltés, eredmény (felül), csúszkák (alul)."""
    st.title("G1 — a PoC-kapu")
    st.write(
        "A kapu a kísérleti szakasz végén dönt: **go**, **pivot** (egyszer) vagy **no-go**. A döntést a mérőszámok "
        "adják a `koncepcio/01` szabályai szerint, nem a demó benyomása. Tölts be egy Xyo-állapotot, "
        "majd mozgasd a csúszkákat: mikor fordul át a döntés?"
    )
    st.caption("A küszöbök és a számok a Xyo-példa feltevései, nem iparági szabványok.")

    if K_ELOTOLTES not in st.session_state:
        st.session_state[K_ELOTOLTES] = NEVEK[0]
        betolt()
    st.selectbox("Kiinduló állapot", NEVEK, key=K_ELOTOLTES, on_change=betolt)

    eredmeny = st.container()  # felül jelenik meg, de a csúszkák értékei után töltjük ki

    st.subheader("Mutatók (csúszkák)")
    c1, c2 = st.columns(2)
    with c1:
        st.number_input(
            f"Permission leakage (szivárgó eset a {adatok.JOGOSULTSAGI_ESETEK}-ből)",
            min_value=0, max_value=adatok.JOGOSULTSAGI_ESETEK, step=1, key=K_LEAKAGE,
        )  # fmt: skip
        st.slider("Faithfulness", 0.0, 1.0, step=0.01, key=K_FAITHFULNESS)
        st.slider("Context recall", 0.0, 1.0, step=0.01, key=K_RECALL)
        st.slider(
            f"Helyes elutasítás (a {adatok.GOLDEN_ELUTASITANDO} elutasítandóból)",
            0, adatok.GOLDEN_ELUTASITANDO, key=K_HELYES,
        )  # fmt: skip
    with c2:
        st.slider(
            f"Téves elutasítás (a {adatok.GOLDEN_MEGVALASZOLHATO} megválaszolhatóból)",
            0, adatok.GOLDEN_MEGVALASZOLHATO, key=K_TEVES,
        )  # fmt: skip
        st.slider("Latency p95 (másodperc)", 0.0, 20.0, step=0.1, key=K_LATENCY)
        st.slider("Költség kérdésenként (Ft)", 0, 80, key=K_KOLTSEG)
        st.caption(
            f"Éves költség = kérdésenként × {adatok.ezres(adatok.KERESES_EVENTE)} kérdés/év; "
            f"a futási keret {adatok.ft(adatok.FUTASI_KERET_EVES)}/év."
        )

    st.subheader("Emberi ítéletek (a mérés mellé)")
    d1, d2 = st.columns(2)
    with d1:
        st.checkbox("A pivot már megvolt", key=K_PIVOT_VOLT)
        st.checkbox("A hiba helye azonosított (van konkrét hipotézis)", key=K_HIBAHELY)
    with d2:
        st.checkbox("Van olcsóbb változat, amely a kritikus mutatókat tartja", key=K_OLCSOBB)
        st.checkbox("A recall tartós hibájának oka az adat minősége", key=K_ADATMINOSEG)

    m = adatok.Meres(
        faithfulness=round(st.session_state[K_FAITHFULNESS], 2),
        context_recall=round(st.session_state[K_RECALL], 2),
        context_precision=None,
        helyes_elutasitas=st.session_state[K_HELYES],
        teves_elutasitas=st.session_state[K_TEVES],
        szivargas=st.session_state[K_LEAKAGE],
        latency_p95_s=round(st.session_state[K_LATENCY], 1),
        koltseg_ft=st.session_state[K_KOLTSEG],
    )
    eves = kapu.eves_koltseg(m)
    dontes = kapu.g1_dontes(
        m,
        eves_koltseg=eves,
        pivot_volt=st.session_state[K_PIVOT_VOLT],
        hiba_helye_azonositott=st.session_state[K_HIBAHELY],
        van_olcsobb_valtozat=st.session_state[K_OLCSOBB],
        adatminoseg_a_recall_oka=st.session_state[K_ADATMINOSEG],
    )

    with eredmeny:
        kiemeles = {kapu.GO: st.success, kapu.PIVOT: st.warning, kapu.NO_GO: st.error}[dontes.kimenet]
        kiemeles(f"**Döntés: {dontes.kimenet.upper()}**\n\n" + "\n".join(f"- {s}" for s in dontes.indoklas))
        st.markdown(_tabla(m, eves, dontes.savok))
        st.caption(
            "Az answer relevancy szándékosan nincs a táblában: csak diagnosztika, döntést nem alapozunk rá."
        )
