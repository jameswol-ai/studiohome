"""
studiohome module registry.

Centralizes module discovery, navigation categories,
and module routing.
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


# =====================================================
# REGISTERED MODULES
# =====================================================

MODULE_DEFINITIONS: tuple[ModuleDefinition, ...] = (
    # -------------------------------------------------
    # Design & Engineering
    # -------------------------------------------------

    ModuleDefinition(
        "AI Brain",
        "modules.ai_brain",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "Architecture",
        "modules.architecture",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "Structure",
        "modules.structure",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "MEP",
        "modules.mep",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "GIS & Site",
        "modules.gis_site",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "Cost",
        "modules.cost",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "Massing",
        "modules.massing",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "Zoning Code",
        "modules.zoning_code",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "Export Suite",
        "modules.export_suite",
        "Design & Engineering",
    ),

    ModuleDefinition(
        "Full Sim",
        "modules.full_sim",
        "Design & Engineering",
    ),

    # -------------------------------------------------
    # Urban & Civilization
    # -------------------------------------------------

    ModuleDefinition(
        "RL City",
        "modules.rl_city",
        "Urban & Civilization",
    ),

    ModuleDefinition(
        "City Learning",
        "modules.city_learning",
        "Urban & Civilization",
    ),

    ModuleDefinition(
        "Diplomacy",
        "modules.diplomacy",
        "Urban & Civilization",
    ),

    ModuleDefinition(
        "War",
        "modules.war",
        "Urban & Civilization",
    ),

    ModuleDefinition(
        "Culture",
        "modules.culture",
        "Urban & Civilization",
    ),

    ModuleDefinition(
        "Consciousness",
        "modules.consciousness",
        "Urban & Civilization",
    ),

    ModuleDefinition(
        "Meta-Evo",
        "modules.meta_evo",
        "Urban & Civilization",
    ),
)


# =====================================================
# CATEGORY ORDER
# =====================================================

CATEGORY_ORDER: tuple[str, ...] = (
    "Overview & Control",
    "Design & Engineering",
    "Urban & Civilization",
)


# =====================================================
# LOAD MODULES
# =====================================================

def load_modules() -> dict[str, ModuleType]:
    """
    Import all registered modules.

    Import errors intentionally propagate so broken
    modules are detected during application startup.
    """

    modules: dict[str, ModuleType] = {}

    for definition in MODULE_DEFINITIONS:
        modules[definition.name] = import_module(
            definition.import_path
        )

    return modules


# =====================================================
# BUILD NAVIGATION
# =====================================================

def build_categories() -> dict[str, list[str]]:
    """Build sidebar navigation categories."""

    categories: dict[str, list[str]] = {
        category: []
        for category in CATEGORY_ORDER
    }

    categories["Overview & Control"].append(
        "Executive Cockpit"
    )

    for definition in MODULE_DEFINITIONS:

        categories.setdefault(
            definition.category,
            [],
        ).append(
            definition.name
        )

    return categories


# =====================================================
# BUILD MODULE ROUTER
# =====================================================

def build_module_mapping() -> dict[str, ModuleType | None]:
    """Build the application module router."""

    modules = load_modules()

    return {
        "Executive Cockpit": None,
        **modules,
    }


# =====================================================
# RENDER FUNCTION RESOLUTION
# =====================================================

def get_render_function(
    module: ModuleType,
) -> Callable[[], object] | None:
    """
    Return a callable render() function.

    Returns None if the module does not expose
    a callable render() attribute.
    """

    render = getattr(
        module,
        "render",
        None,
    )

    if callable(render):
        return render

    return None


# =====================================================
# REGISTRY VALIDATION
# =====================================================

def validate_registry() -> list[str]:
    """
    Validate module imports and render() contracts.

    Returns a list of human-readable errors.
    """

    errors: list[str] = []

    seen_names: set[str] = set()

    for definition in MODULE_DEFINITIONS:

        if definition.name in seen_names:

            errors.append(
                f"Duplicate module name: "
                f"{definition.name}"
            )

        seen_names.add(definition.name)

        try:

            module = import_module(
                definition.import_path
            )

        except Exception as exc:

            errors.append(
                f"{definition.name}: "
                f"import failed: {exc}"
            )

            continue

        render = getattr(
            module,
            "render",
            None,
        )

        if not callable(render):

            errors.append(
                f"{definition.name}: "
                "render() is missing or not callable"
            )

    return errors