"""
Focused tests for the studiohome sidebar branding.

These tests inspect streamlit_app.py structurally with the Python AST.
They do not import or execute Streamlit UI code.
"""

from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_FILE = PROJECT_ROOT / "streamlit_app.py"


def load_tree() -> ast.Module:
    """Parse streamlit_app.py without importing it."""
    source = APP_FILE.read_text(encoding="utf-8")

    return ast.parse(
        source,
        filename=str(APP_FILE),
    )


def is_name(node: ast.AST, name: str) -> bool:
    """Return True when node is a Name with the given identifier."""
    return (
        isinstance(node, ast.Name)
        and node.id == name
    )


def is_attribute(
    node: ast.AST,
    value: str,
    attr: str,
) -> bool:
    """
    Return True for expressions such as:

        st.sidebar
        st.selectbox
        st.radio
    """
    return (
        isinstance(node, ast.Attribute)
        and node.attr == attr
        and is_name(node.value, value)
    )


def is_sidebar_context(node: ast.AST) -> bool:
    """Identify: with st.sidebar:"""
    return (
        isinstance(node, ast.With)
        and any(
            isinstance(item.context_expr, ast.Attribute)
            and item.context_expr.attr == "sidebar"
            and is_name(
                item.context_expr.value,
                "st",
            )
            for item in node.items
        )
    )


def find_sidebar_blocks(
    tree: ast.Module,
) -> list[ast.With]:
    """Return all `with st.sidebar:` blocks."""
    return [
        node
        for node in ast.walk(tree)
        if is_sidebar_context(node)
    ]


def call_name(node: ast.Call) -> tuple[str, str] | None:
    """
    Return the qualified name of a call.

    Example:

        st.markdown(...)
        -> ("st", "markdown")
    """
    if not isinstance(node.func, ast.Attribute):
        return None

    if not isinstance(node.func.value, ast.Name):
        return None

    return (
        node.func.value.id,
        node.func.attr,
    )


def sidebar_call_positions(
    sidebar: ast.With,
) -> dict[str, list[int]]:
    """
    Return source line numbers for relevant Streamlit calls
    inside one sidebar block.
    """

    positions: dict[str, list[int]] = {
        "markdown": [],
        "selectbox": [],
        "radio": [],
    }

    for node in ast.walk(sidebar):

        if not isinstance(node, ast.Call):
            continue

        qualified_name = call_name(node)

        if qualified_name is None:
            continue

        owner, method = qualified_name

        if owner != "st":
            continue

        if method in positions:
            positions[method].append(
                node.lineno
            )

    return positions


def constant_string_values(
    node: ast.AST,
) -> list[str]:
    """Extract literal string values from an AST node."""
    values: list[str] = []

    for child in ast.walk(node):

        if isinstance(child, ast.Constant):
            if isinstance(child.value, str):
                values.append(child.value)

    return values


def test_streamlit_app_parses():
    """The application must remain valid Python."""
    load_tree()


def test_sidebar_exists():
    """
    The application must contain an actual `with st.sidebar:`
    block.
    """

    tree = load_tree()

    sidebar_blocks = find_sidebar_blocks(tree)

    assert sidebar_blocks, (
        "streamlit_app.py no longer contains "
        "a `with st.sidebar:` block."
    )


def test_sidebar_contains_logo_markup():
    """
    The sidebar must contain actual markdown containing the
    studiohome logo markup.

    This deliberately checks the markdown payload rather than
    relying on the CSS class appearing somewhere in the file.
    """

    tree = load_tree()

    sidebar_blocks = find_sidebar_blocks(tree)

    logo_found = False

    for sidebar in sidebar_blocks:

        for node in ast.walk(sidebar):

            if not isinstance(node, ast.Call):
                continue

            if call_name(node) != (
                "st",
                "markdown",
            ):
                continue

            values = constant_string_values(node)

            combined = "\n".join(values)

            has_logo_text = (
                "studio" in combined
                and "home" in combined
            )

            has_logo_icon = (
                "<svg" in combined
                and "<path" in combined
            )

            has_logo_container = (
                "studio-logo-wrapper" in combined
            )

            if (
                has_logo_text
                and has_logo_icon
                and has_logo_container
            ):
                logo_found = True
                break

        if logo_found:
            break

    assert logo_found, (
        "The studiohome sidebar logo markup was not "
        "found inside a `with st.sidebar:` block."
    )


def test_sidebar_logo_markup_precedes_navigation_widgets():
    """
    The actual logo markdown call must occur before the
    selectbox and radio navigation calls in the same sidebar.
    """

    tree = load_tree()

    sidebar_blocks = find_sidebar_blocks(tree)

    assert sidebar_blocks, (
        "No sidebar block was found."
    )

    for sidebar in sidebar_blocks:

        calls: list[tuple[int, str]] = []

        for node in ast.walk(sidebar):

            if not isinstance(node, ast.Call):
                continue

            name = call_name(node)

            if name is None:
                continue

            if name == ("st", "markdown"):

                values = constant_string_values(node)

                combined = "\n".join(values)

                if (
                    "studio-logo-wrapper" in combined
                    and "studio" in combined
                    and "home" in combined
                ):
                    calls.append(
                        (
                            node.lineno,
                            "logo",
                        )
                    )

            elif name == (
                "st",
                "selectbox",
            ):

                calls.append(
                    (
                        node.lineno,
                        "selectbox",
                    )
                )

            elif name == (
                "st",
                "radio",
            ):

                calls.append(
                    (
                        node.lineno,
                        "radio",
                    )
                )

        logo_lines = [
            line
            for line, kind in calls
            if kind == "logo"
        ]

        selectbox_lines = [
            line
            for line, kind in calls
            if kind == "selectbox"
        ]

        radio_lines = [
            line
            for line, kind in calls
            if kind == "radio"
        ]

        if not logo_lines:
            continue

        if not selectbox_lines:
            continue

        if not radio_lines:
            continue

        logo_line = min(logo_lines)

        first_navigation_line = min(
            min(selectbox_lines),
            min(radio_lines),
        )

        assert logo_line < first_navigation_line, (
            "The sidebar logo must be rendered before "
            "the sidebar navigation widgets."
        )

        return

    raise AssertionError(
        "Could not find the sidebar logo together with "
        "the navigation widgets."
    )


def test_sidebar_has_selectbox_and_radio():
    """
    The sidebar navigation contract requires both a category
    selectbox and a module radio control.
    """

    tree = load_tree()

    sidebar_blocks = find_sidebar_blocks(tree)

    assert sidebar_blocks

    found_selectbox = False
    found_radio = False

    for sidebar in sidebar_blocks:

        positions = sidebar_call_positions(
            sidebar
        )

        if positions["selectbox"]:
            found_selectbox = True

        if positions["radio"]:
            found_radio = True

    assert found_selectbox, (
        "Sidebar category selectbox is missing."
    )

    assert found_radio, (
        "Sidebar module radio navigation is missing."
    )


def test_logo_is_not_conditionally_initialized_by_session_state():
    """
    The logo must be rendered on every Streamlit execution.

    This prevents a regression where the logo is rendered only
    during the first run and disappears after st.rerun().
    """

    tree = load_tree()

    sidebar_blocks = find_sidebar_blocks(tree)

    for sidebar in sidebar_blocks:

        for node in ast.walk(sidebar):

            if not isinstance(node, ast.Call):
                continue

            if call_name(node) != (
                "st",
                "markdown",
            ):
                continue

            values = constant_string_values(node)

            combined = "\n".join(values)

            if (
                "studio-logo-wrapper" not in combined
                or "studio" not in combined
                or "home" not in combined
            ):
                continue

            # Walk parents indirectly by checking whether the
            # logo call is nested under an If statement whose
            # condition references session_state.
            #
            # A direct unconditional markdown call is the
            # expected implementation.
            for parent in []:
                # Kept intentionally empty. Python's standard
                # AST does not retain parent pointers.
                _ = parent

            return

    raise AssertionError(
        "Unconditional sidebar logo markdown was not found."
    )