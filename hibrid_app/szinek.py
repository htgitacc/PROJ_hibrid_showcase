"""A felület színei egy helyen.

A harmadik modell színvilága a két testvérprojekt **számtani közepe**, csatornánként (R, G, B):
a `PROJ_pm_all` meleg, terrakotta kiemelésű arculata és a `PROJ_sm_all` zöldes, jáde kiemelésű
arculata közé esik, olajzöld-khaki kiemeléssel. Döntés: `docs/adr/0003`. A jelentést hordozó
színek (piros, narancs) nem a két arculat közepe, hanem a pm_all jelentésszínei.

A `.streamlit/config.toml` értékei ezekkel egyeznek (`tests/test_szinek.py` őrzi).
"""

# A két forrásarculat értékei (a közép ezekből számolódik; a projektek témájából átvett értékek).
PM = {
    "kiemeles": "#a14a2c", "szoveg": "#2a2420", "hatter": "#f3eee7", "hatter2": "#e9e1d6",
    "keret": "#d9cfc2", "oldalsav": "#ebe3d8", "info_szoveg": "#2f5560", "info_hatter": "#e1e8e4",
}  # fmt: skip
SM = {
    "kiemeles": "#1f7a5a", "szoveg": "#1f2a24", "hatter": "#eef4ef", "hatter2": "#dfe9e2",
    "keret": "#c9d8cd", "oldalsav": "#e3ece5", "info_szoveg": "#1d5c63", "info_hatter": "#d9ebe9",
}  # fmt: skip


def rgb(szin: str) -> tuple[int, int, int]:
    szin = szin.lstrip("#")
    return int(szin[0:2], 16), int(szin[2:4], 16), int(szin[4:6], 16)


def hexa(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def kozep(a: str, b: str) -> str:
    """A két szín csatornánkénti számtani közepe (kerekítve)."""
    return hexa(*(round((x + y) / 2) for x, y in zip(rgb(a), rgb(b), strict=True)))


def elhalvanyit(szin: str, arany: float) -> str:
    """A szín `arany` részben fehérrel keverve (0 = az eredeti, 1 = fehér)."""
    return hexa(*(round(x + (255 - x) * arany) for x in rgb(szin)))


PALETTA = {nev: kozep(PM[nev], SM[nev]) for nev in PM}

KIEMELES = PALETTA["kiemeles"]
SZOVEG = PALETTA["szoveg"]
HATTER = PALETTA["hatter"]
HATTER2 = PALETTA["hatter2"]
KERET = PALETTA["keret"]
OLDALSAV = PALETTA["oldalsav"]
INFO_SZOVEG = PALETTA["info_szoveg"]
INFO_HATTER = PALETTA["info_hatter"]

# Jelentést hordozó színek (a pm_all-ból; nem a két arculat közepe)
PIROS_SZOVEG, PIROS_HATTER = "#9b2c22", "#f3dcd3"
NARANCS_SZOVEG, NARANCS_HATTER = "#8a4b0f", "#f3e3cc"

# Az ábrák színei a palettából
ABRA_CSOMOPONT = HATTER2
ABRA_KIEMELT = elhalvanyit(KIEMELES, 0.6)  # a kapuk (hatszögek) háttere: határozottan sötétebb a csomópontoknál
ABRA_EL = kozep(SZOVEG, KIEMELES)  # az élek sötétek: vékony vonalon a kontraszt számít
