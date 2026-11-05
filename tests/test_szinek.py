"""A színek: a két testvérarculat közepe, a config.toml egyezése, kontraszt, az ábra színei."""

import tomllib

import pytest

from hibrid_app import mermaid, szinek
from tests.conftest import ROOT, olvas

TEMA = tomllib.loads(olvas(".streamlit/config.toml"))["theme"]


def kontraszt(a: str, b: str) -> float:
    """WCAG 2.1 kontrasztarány."""

    def fenyero(szin: str) -> float:
        def csatorna(v: int) -> float:
            v /= 255
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

        r, g, b_ = map(csatorna, szinek.rgb(szin))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b_

    vilagos, sotet = sorted((fenyero(a), fenyero(b)), reverse=True)
    return (vilagos + 0.05) / (sotet + 0.05)


# --- a segédfüggvények ---------------------------------------------------------------------


def test_rgb_hexa_oda_vissza():
    assert szinek.rgb("#a14a2c") == (161, 74, 44)
    assert szinek.hexa(161, 74, 44) == "#a14a2c"
    assert szinek.hexa(*szinek.rgb("#0a0b0c")) == "#0a0b0c"  # a vezető nulla megmarad


@pytest.mark.parametrize(
    ("a", "b", "vart"),
    [("#000000", "#ffffff", "#808080"), ("#102030", "#102030", "#102030"), ("#00000a", "#000014", "#00000f")],
)
def test_kozep(a, b, vart):
    assert szinek.kozep(a, b) == vart
    assert szinek.kozep(b, a) == vart  # felcserélhető


def test_elhalvanyit():
    assert szinek.elhalvanyit("#000000", 0) == "#000000"
    assert szinek.elhalvanyit("#000000", 1) == "#ffffff"
    assert szinek.elhalvanyit("#000000", 0.25) == "#404040"  # 63,75 → 64
    assert szinek.elhalvanyit("#606243", 0.5) == "#b0b0a1"  # (96+255)/2 = 175,5 → 176 · (98+255)/2 = 176,5 → 176 · 161


# --- a paletta -----------------------------------------------------------------------------


def test_a_paletta_a_ket_arculat_csatornankenti_kozepe():
    for nev in szinek.PM:
        assert szinek.PALETTA[nev] == szinek.kozep(szinek.PM[nev], szinek.SM[nev]), nev


def test_a_rogzitett_ertekek():
    """A döntés (docs/adr/0003) számai: ha a paletta változik, ez jelzi."""
    assert szinek.PALETTA == {
        "kiemeles": "#606243", "szoveg": "#242722", "hatter": "#f0f1eb", "hatter2": "#e4e5dc",
        "keret": "#d1d4c8", "oldalsav": "#e7e8de", "info_szoveg": "#265862", "info_hatter": "#ddeae6",
    }  # fmt: skip


def test_a_kiemeles_a_ket_forras_kiemelese_kozott_van():
    for csatorna in range(3):
        a, b, k = (szinek.rgb(x)[csatorna] for x in (szinek.PM["kiemeles"], szinek.SM["kiemeles"], szinek.KIEMELES))
        assert min(a, b) <= k <= max(a, b)


# --- a config.toml egyezik a konstansokkal ------------------------------------------------


@pytest.mark.parametrize(
    ("kulcs", "ertek"),
    [
        ("primaryColor", szinek.KIEMELES), ("linkColor", szinek.KIEMELES), ("textColor", szinek.SZOVEG),
        ("backgroundColor", szinek.HATTER), ("secondaryBackgroundColor", szinek.HATTER2),
        ("borderColor", szinek.KERET), ("blueTextColor", szinek.INFO_SZOVEG),
        ("blueBackgroundColor", szinek.INFO_HATTER), ("redTextColor", szinek.PIROS_SZOVEG),
        ("redBackgroundColor", szinek.PIROS_HATTER), ("orangeTextColor", szinek.NARANCS_SZOVEG),
        ("orangeBackgroundColor", szinek.NARANCS_HATTER),
    ],
)  # fmt: skip
def test_a_tema_a_konstansokat_hasznalja(kulcs, ertek):
    assert TEMA[kulcs] == ertek


def test_az_oldalsav_szine_es_az_egyetlen_vilagos_tema():
    assert TEMA["sidebar"]["backgroundColor"] == szinek.OLDALSAV
    assert TEMA["base"] == "light"
    assert "dark" not in TEMA and "light" not in TEMA  # nincs külön [theme.light] / [theme.dark]


def test_a_tema_minden_szine_ismert_ertek():
    """Ha a config.toml új színt kap, az kerüljön a szinek.py-ba is."""
    ismert = {v for k, v in vars(szinek).items() if k.isupper() and isinstance(v, str) and v.startswith("#")}
    hex_ertekek = {v for k, v in TEMA.items() if isinstance(v, str) and v.startswith("#")}
    hex_ertekek.add(TEMA["sidebar"]["backgroundColor"])
    assert hex_ertekek <= ismert


# --- kontraszt (WCAG 2.1) ------------------------------------------------------------------


@pytest.mark.parametrize("felulet", [szinek.HATTER, szinek.HATTER2, szinek.OLDALSAV])
def test_a_kiemeles_olvashato_minden_feluleten(felulet):
    assert kontraszt(szinek.KIEMELES, felulet) >= 4.5


@pytest.mark.parametrize("felulet", [szinek.HATTER, szinek.HATTER2, szinek.OLDALSAV, szinek.INFO_HATTER])
def test_a_szoveg_legalabb_7_az_egyhez_minden_feluleten(felulet):
    assert kontraszt(szinek.SZOVEG, felulet) >= 7


def test_info_doboz_es_feher_szoveg_a_kiemelesen():
    assert kontraszt(szinek.INFO_SZOVEG, szinek.INFO_HATTER) >= 4.5
    assert kontraszt("#ffffff", szinek.KIEMELES) >= 4.5
    assert kontraszt(szinek.PIROS_SZOVEG, szinek.PIROS_HATTER) >= 4.5
    assert kontraszt(szinek.NARANCS_SZOVEG, szinek.NARANCS_HATTER) >= 4.5


def test_a_kontraszt_segedfuggveny_ismert_ertekekkel():
    assert kontraszt("#000000", "#ffffff") == pytest.approx(21.0)
    assert kontraszt("#777777", "#777777") == pytest.approx(1.0)


# --- az ábra színei a palettából -----------------------------------------------------------


def test_az_abra_a_paletta_szineit_hasznalja():
    d = mermaid.dot("flowchart LR\nA --> B\nG{{\"x\"}}\nsubgraph S\nC\nend\n")
    for szin in (szinek.ABRA_CSOMOPONT, szinek.KIEMELES, szinek.SZOVEG, szinek.ABRA_EL, szinek.ABRA_KIEMELT):
        assert f'"{szin}"' in d, szin


def test_a_kapuk_hatszoge_halvany_kiemelo_hatteret_kap():
    d = mermaid.dot('flowchart LR\nG{{"x"}}\n')
    assert f'shape=hexagon, fillcolor="{szinek.ABRA_KIEMELT}"' in d
    assert kontraszt(szinek.SZOVEG, szinek.ABRA_KIEMELT) >= 7  # a felirat olvasható


def test_nem_maradt_a_pm_all_terrakotta_a_kodban():
    """A pm_all kiemelése csak a szinek.py forrásadatai között szerepelhet."""
    regi = szinek.PM["kiemeles"]
    for fajl in [*(ROOT / "hibrid_app").glob("*.py"), ROOT / "app.py", ROOT / ".streamlit/config.toml"]:
        if fajl.name == "szinek.py":
            continue
        assert regi not in fajl.read_text(encoding="utf-8"), fajl.name


def test_az_elek_sotetek_es_lathatok():
    """Vékony vonalon a kontraszt számít: az él színe a szöveg és a kiemelés közepe, nem halvány szürke."""
    assert szinek.ABRA_EL == "#424432" and szinek.ABRA_EL not in (szinek.SZOVEG, szinek.KIEMELES)
    d = mermaid.dot("flowchart LR\nA --> B\n")
    assert f'edge [color="{szinek.ABRA_EL}", fontcolor="{szinek.SZOVEG}", fontsize=10, penwidth=1.2]' in d
    assert "fontsize=11, penwidth=1.2]" in d  # a csomópontok kerete is vastagabb
    assert kontraszt(szinek.ABRA_EL, szinek.HATTER) >= 7


def test_a_kapuk_hatterenek_meg_kell_kulonboznie_a_csomopontokeetol():
    assert szinek.ABRA_KIEMELT == "#bfc0b4" and szinek.ABRA_KIEMELT != szinek.ABRA_CSOMOPONT
    assert kontraszt(szinek.ABRA_KIEMELT, szinek.HATTER) >= 1.5  # látszik a háttéren is


def test_a_furtcimke_es_keret_kiemelo_szinu_a_feliratok_szoveg_szinuek():
    d = mermaid.dot('flowchart LR\nsubgraph S["cím"]\nA["x"]\nend\n')
    assert f'color="{szinek.KIEMELES}"; fontcolor="{szinek.KIEMELES}"; fontsize=12' in d  # fürt
    assert f'color="{szinek.KIEMELES}", fontcolor="{szinek.SZOVEG}", fontsize=11' in d  # csomópont
