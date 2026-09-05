"""Central registry for studiohome AEC/MEP modules."""

from __future__ import annotations

from modules import (
    ai_brain,
    architecture,
    building_envelope,
    civil_works,
    consciousness,
    cost,
    culture,
    city_learning,
    diplomacy,
    electrical,
    export_suite,
    floorplate,
    full_sim,
    gis_site,
    lca,
    massing,
    mep,
    meta_evo,
    plumbing_fire,
    project_setup,
    rl_city,
    structure,
    war,
    zoning_code,
)


CATEGORIES = {
    "Project & Control": [
        "Executive Cockpit",
        "Project Setup",
        "AI Brain",
    ],
    "Architecture & BIM": [
        "Architecture",
        "Massing",
        "Floorplate",
        "Building Envelope",
        "Zoning Code",
        "Export Suite",
    ],
    "Structural & Civil": [
        "Structure",
        "GIS & Site",
        "Civil Works",
    ],
    "MEP & Building Systems": [
        "MEP",
        "Electrical",
        "Plumbing & Fire",
        "LCA Audit",
    ],
    "Cost, Delivery & Simulation": [
        "Cost",
        "Full Sim",
    ],
    "Urban & Intelligence": [
        "RL City",
        "City Learning",
        "Diplomacy",
        "War",
        "Culture",
        "Consciousness",
        "Meta-Evo",
    ],
}


MODULE_MAPPING = {
    "Executive Cockpit": None,
    "Project Setup": project_setup,
    "AI Brain": ai_brain,
    "Architecture": architecture,
    "Massing": massing,
    "Floorplate": floorplate,
    "Building Envelope": building_envelope,
    "Zoning Code": zoning_code,
    "Export Suite": export_suite,
    "Structure": structure,
    "GIS & Site": gis_site,
    "Civil Works": civil_works,
    "MEP": mep,
    "Electrical": electrical,
    "Plumbing & Fire": plumbing_fire,
    "LCA Audit": lca,
    "Cost": cost,
    "Full Sim": full_sim,
    "RL City": rl_city,
    "City Learning": city_learning,
    "Diplomacy": diplomacy,
    "War": war,
    "Culture": culture,
    "Consciousness": consciousness,
    "Meta-Evo": meta_evo,
}


def build_categories():
    """Return a fresh copy of the navigation categories."""
    return {category: list(tabs) for category, tabs in CATEGORIES.items()}


def build_module_mapping():
    """Return the registered module mapping."""
    return dict(MODULE_MAPPING)


def get_render_function(module):
    """Return a module's callable render function, if available."""
    render = getattr(module, "render", None)
    return render if callable(render) else None
