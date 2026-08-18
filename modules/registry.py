"""
studiohome module registry.

Centralizes module discovery, navigation categories,
and module routing so streamlit_app.py remains focused
on application orchestration and UI.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Callable


@dataclass(frozen=True)
class ModuleDefinition:
    """Definition of a studiohome application module."""

    name: str
    import_path: str
    category: str


MODULE_DEFINITIONS: tuple[ModuleDefinition, ...] = (
    # Design & Engineering
    ModuleDefinition("AI Brain", "modules.ai_brain", "Design & Engineering"),
    ModuleDefinition("Architecture", "modules.architecture", "Design & Engineering"),
    ModuleDefinition("Structure", "modules.structure", "Design & Engineering"),
    ModuleDefinition("MEP", "modules.mep", "Design & Engineering"),
    ModuleDefinition("GIS & Site", "modules.gis_site", "Design & Engineering"),
    ModuleDefinition("Cost", "modules.cost", "Design & Engineering"),
    ModuleDefinition("Massing", "modules.massing", "Design & Engineering"),
    ModuleDefinition("Zoning Code", "modules.zoning_code", "Design & Engineering"),
    ModuleDefinition("Export Suite", "modules.export_suite", "Design & Engineering"),
    ModuleDefinition("Full Sim", "modules.full_sim", "Design & Engineering"),

    # Urban & Civilization
    ModuleDefinition("RL City", "modules.rl_city", "Urban & Civilization"),
    ModuleDefinition("City Learning", "modules.city_learning", "Urban & Civilization"),
    ModuleDefinition("Diplomacy", "modules.diplomacy", "Urban & Civilization"),
    ModuleDefinition("War", "modules.war", "Urban & Civilization"),
    ModuleDefinition("Culture", "modules.culture", "Urban & Civilization"),
    ModuleDefinition("Consciousness", "modules.consciousness", "Urban & Civilization"),
    ModuleDefinition("Meta-Evo", "modules.meta_evo", "Urban & Civilization"),
)


CATEGORY_ORDER: tuple[str, ...] = (
    "Overview & Control",
    "Design & Engineering",
    "Urban & Civilization",
)


def load_modules() -> dict[str, ModuleType]:
    """
    Import all registered modules.

    Import errors are allowed to propagate so deployment/startup
    validation can detect broken module imports immediately.
    """
    return {
        definition.name: import_module(definition.import_path)
        for definition in MODULE_DEFINITIONS
    }


def build_categories() -> dict[str, list[str]]:
    """Build navigation categories from the module registry."""

    categories = {
        category: []
        for category in CATEGORY_ORDER
    }

    categories["Overview & Control"].append(
        "Executive Cockpit"
    )

    for definition in MODULE_DEFINITIONS:
        categories.setdefault(definition.category, []).append(
            definition.name
        )

    return categories


def build_module_mapping() -> dict[str, ModuleType | None]:
    """Build the router mapping used by the application."""

    modules = load_modules()

    return {
        "Executive Cockpit": None,
        **modules,
    }


def get_render_function(
    module: ModuleType,
) -> Callable[[], object] | None:
    """
    Return a module's callable render() function.

    Returns None when render() does not exist or is not callable.
    """

    render = getattr(module, "render", None)

    return render if callable(render) else None