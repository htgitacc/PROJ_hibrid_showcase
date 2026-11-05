"""Füstteszt: a teljes alkalmazás és minden nézet kivétel nélkül lefut."""

import pytest
from streamlit.testing.v1 import AppTest

from tests.conftest import ROOT

PAGES = ["overview"]


@pytest.mark.parametrize("page", PAGES)
def test_page_renders(page):
    at = AppTest.from_string(f"from hibrid_app import views\nviews.{page}()\n", default_timeout=60).run()
    assert not at.exception, at.exception
    assert at.title[0].value  # a nézet tényleg tartalmat rajzolt


def test_full_app_renders():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not at.exception, at.exception
    assert at.title[0].value == "Hibrid PM — AI-projekt"
