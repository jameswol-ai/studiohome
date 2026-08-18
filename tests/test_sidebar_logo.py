"""
Focused sidebar branding contract tests.

These tests do not require a live Streamlit server.
They inspect streamlit_app.py directly so importing the
application does not execute Streamlit startup code.
"""

from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_FILE = PROJECT_ROOT / "streamlit_app.py"


def read_app_source() -> str:
    """Return the complete streamlit_app.py source."""
    return APP_FILE.read_text(encoding="utf-8")


def test_sidebar_logo_markup_exists():
    """
    The studiohome sidebar logo must exist in the application.
    """

    source = read_app_source()

    assert "studio-logo-wrapper" in source
    assert "studio-logo-icon" in source
    assert "studio-logo-text" in source
    assert "studio<span>home</span>" in source

    # Verify the architectural SVG icon is still present.
    assert "<svg" in source
    assert "viewBox=\"0 0 24 24\"" in source
    assert "<path" in source


def test_sidebar_logo_is_rendered_before_navigation_widgets():
    """
    The sidebar branding must be rendered before the
    selectbox/radio navigation widgets.
    """

    source = read_app_source()

    logo_position = source.index(
        "studio-logo-wrapper"
    )

    selectbox_position = source.index(
        "st.selectbox("
    )

    radio_position = source.index(
        "st.radio("
    )

    assert logo_position < selectbox_position
    assert logo_position < radio_position


def test_sidebar_logo_is_inside_sidebar_context():
    """
    The logo must be rendered inside a st.sidebar context,
    not in the main application body.
    """

    source = read_app_source()

    sidebar_position = source.index(
        "with st.sidebar:"
    )

    logo_position = source.index(
        "studio-logo-wrapper"
    )

    assert sidebar_position < logo_position


def test_sidebar_logo_markup_occurs_on_normal_execution_path():
    """
    The logo must not be hidden behind an active-tab condition
    or a navigation callback.

    This protects it from disappearing after st.rerun().
    """

    source = read_app_source()

    logo_position = source.index(
        "studio-logo-wrapper"
    )

    first_navigation_position = min(
        position
        for position in (
            source.find("st.selectbox("),
            source.find("st.radio("),
        )
        if position != -1
    )

    prefix = source[:logo_position]

    # The logo should be established before navigation state
    # determines the active module.
    assert "if active_tab" not in prefix
    assert "if st.session_state.active_tab" not in prefix

    assert logo_position < first_navigation_position


def test_sidebar_logo_markup_survives_rerun_contract():
    """
    A Streamlit rerun executes streamlit_app.py from the top.

    Therefore the branding markup must not depend on a one-time
    initialization flag such as:

        if "logo_rendered" not in st.session_state:

    This test ensures the logo remains unconditional.
    """

    source = read_app_source()

    logo_position = source.index(
        "studio-logo-wrapper"
    )

    # Look at the code immediately preceding the logo.
    preceding_source = source[:logo_position]

    # The logo must not be protected by a session-state
    # initialization condition.
    assert "logo_rendered" not in preceding_source

    # It must be rendered from a sidebar block.
    sidebar_position = preceding_source.rfind(
        "with st.sidebar:"
    )

    assert sidebar_position != -1


def test_sidebar_navigation_widgets_exist_after_logo():
    """
    Both navigation widgets must remain after the logo.
    """

    source = read_app_source()

    logo_position = source.index(
        "studio-logo-wrapper"
    )

    selectbox_position = source.index(
        "st.selectbox("
    )

    radio_position = source.index(
        "st.radio("
    )

    assert selectbox_position > logo_position
    assert radio_position > selectbox_position


def test_streamlit_app_parses_successfully():
    """
    Basic syntax guard for streamlit_app.py.
    """

    source = read_app_source()

    ast.parse(
        source,
        filename=str(APP_FILE),
    )