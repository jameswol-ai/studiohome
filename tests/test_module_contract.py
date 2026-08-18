"""
Contract tests for all registered studiohome modules.

These tests deliberately do not import streamlit_app.py.
"""

from importlib import import_module

import pytest

from modules.registry import MODULE_DEFINITIONS


@pytest.mark.parametrize(
    "definition",
    MODULE_DEFINITIONS,
    ids=lambda definition: definition.name,
)
def test_registered_module_imports_and_exposes_render(definition):
    """Every registered module must import and expose render()."""

    try:
        module = import_module(definition.import_path)
    except Exception as exc:
        pytest.fail(
            f"{definition.name} failed to import "
            f"from {definition.import_path}: {exc}"
        )

    render = getattr(module, "render", None)

    assert callable(render), (
        f"{definition.name} "
        f"({definition.import_path}) must expose "
        "a callable render() function"
    )