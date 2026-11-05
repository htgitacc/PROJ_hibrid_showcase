"""A szűk képernyős CSS: csak médialekérdezésen belül szabály, és az oldalra kerül."""

from streamlit.testing.v1 import AppTest

from hibrid_app import arculat, config
from tests.conftest import ROOT


def test_a_szabaly_a_markdown_tablakra_vonatkozik_es_gorgetest_ad():
    css = arculat.SZUK_KEPERNYO_CSS
    torzs = css.split(f"@media (max-width: {config.KESKENY_PX}px) {{", 1)[1]
    assert '[data-testid="stMarkdownContainer"] table' in torzs
    assert "display: block" in torzs and "overflow-x: auto" in torzs and "max-width: 100%" in torzs


def test_a_toresi_pont_700_px():
    assert config.KESKENY_PX == 700
    assert "@media (max-width: 700px)" in arculat.SZUK_KEPERNYO_CSS


def kivul_a_medialekerdezesen(css: str) -> str:
    """A CSS a @media-blokk (kapcsos zárójel-párosítással megkeresett) kivágása után."""
    kezdet = css.index("@media")
    mely, vege = 0, None
    for i in range(css.index("{", kezdet), len(css)):
        mely += {"{": 1, "}": -1}.get(css[i], 0)
        if mely == 0:
            vege = i + 1
            break
    assert vege is not None, "a @media-blokk nincs lezárva"
    return css[:kezdet] + css[vege:]


def test_a_medialekerdezesen_kivul_csak_a_szeles_tablak_szabalya_van():
    """Ami a lekérdezésen kívül van, az az asztali nézetet is érinti: ezért csak a ≥ 7 oszlopos
    táblákra szól (a többi táblázat asztali nézete nem változik)."""
    kivul = kivul_a_medialekerdezesen(arculat.SZUK_KEPERNYO_CSS)
    assert kivul.count("{") == 1 and kivul.count("}") == 1
    assert "table:has(th:nth-child(7))" in kivul and arculat.SZELES_TABLA_OSZLOP == 7
    assert "overflow-x: auto" in kivul and "max-width: 100%" in kivul


def test_a_kivul_kereso_segedfuggveny_megfogja_a_kivul_levo_szabalyt():
    rossz = "<style>@media (max-width: 1px) {\n}\ntable { x: y; }\n</style>"
    assert "{" in kivul_a_medialekerdezesen(rossz)


def test_a_css_az_alkalmazas_oldalan_van():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception, at.exception
    assert any(arculat.SZUK_KEPERNYO_CSS in str(getattr(e.proto, "body", "")) for e in at.get("html"))
