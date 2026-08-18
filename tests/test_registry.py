"""
Tests for the studiohome module registry.
"""

from types import ModuleType

from modules.registry import (
    build_categories,
    build_module_mapping,
    get_render_function,
)


def test_build_categories_contains_expected_categories():
    categories = build_categories()

    assert list(categories) == [
        "Overview & Control",
        "Design & Engineering",
        "Urban & Civilization",
    ]


def test_build_categories_contains_executive_cockpit():
    categories = build_categories()

    assert "Executive Cockpit" in categories[
        "Overview & Control"
    ]


def test_build_categories_contains_design_modules():
    categories = build_categories()

    expected = {
        "AI Brain",
        "Architecture",
        "Structure",
        "MEP",
        "GIS & Site",
        "Cost",
        "Massing",
        "Zoning Code",
        "Export Suite",
        "Full Sim",
    }

    assert expected.issubset(
        set(categories["Design & Engineering"])
    )


def test_build_categories_contains_civilization_modules():
    categories = build_categories()

    expected = {
        "RL City",
        "City Learning",
        "Diplomacy",
        "War",
        "Culture",
        "Consciousness",
        "Meta-Evo",
    }

    assert expected.issubset(
        set(categories["Urban & Civilization"])
    )


def test_build_module_mapping_contains_executive_cockpit():
    mapping = build_module_mapping()

    assert "Executive Cockpit" in mapping
    assert mapping["Executive Cockpit"] is None


def test_build_module_mapping_contains_registered_modules():
    mapping = build_module_mapping()

    expected = {
        "AI Brain",
        "Architecture",
        "Structure",
        "MEP",
        "GIS & Site",
        "Cost",
        "Massing",
        "Zoning Code",
        "Export Suite",
        "Full Sim",
        "RL City",
        "City Learning",
        "Diplomacy",
        "War",
        "Culture",
        "Consciousness",
        "Meta-Evo",
    }

    assert expected.issubset(set(mapping))


def test_build_module_mapping_values_are_modules():
    mapping = build_module_mapping()

    for name, module in mapping.items():
        if name == "Executive Cockpit":
            continue

        assert isinstance(module, ModuleType)


def test_get_render_function_returns_callable():
    class FakeModule:
        @staticmethod
        def render():
            return None

    render = get_render_function(FakeModule)

    assert callable(render)


def test_get_render_function_returns_none_when_missing():
    class FakeModule:
        pass

    assert get_render_function(FakeModule) is None


def test_get_render_function_returns_none_for_non_callable():
    class FakeModule:
        render = "not callable"

    assert get_render_function(FakeModule) is None