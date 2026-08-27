from modules import (
    ai_brain, architecture, structure, mep, gis_site, cost, massing,
    floorplate, lca, zoning_code, export_suite, full_sim, rl_city, 
    city_learning, diplomacy, war, culture, consciousness, meta_evo
)

def build_categories():
    return {
        "Overview & Control": [
            "Executive Cockpit"
        ],
        "Design & Engineering": [
            "AI Brain", "Architecture", "Structure", "MEP",
            "GIS & Site", "Cost", "Massing", "Floorplate", 
            "LCA Audit", "Zoning Code", "Export Suite", "Full Sim"
        ],
        "Urban & Civilization": [
            "RL City", "City Learning", "Diplomacy", "War",
            "Culture", "Consciousness", "Meta-Evo"
        ]
    }

def build_module_mapping():
    return {
        "Executive Cockpit": None,
        "AI Brain": ai_brain,
        "Architecture": architecture,
        "Structure": structure,
        "MEP": mep,
        "GIS & Site": gis_site,
        "Cost": cost,
        "Massing": massing,
        "Floorplate": floorplate,
        "LCA Audit": lca,
        "Zoning Code": zoning_code,
        "Export Suite": export_suite,
        "Full Sim": full_sim,
        "RL City": rl_city,
        "City Learning": city_learning,
        "Diplomacy": diplomacy,
        "War": war,
        "Culture": culture,
        "Consciousness": consciousness,
        "Meta-Evo": meta_evo
    }

def get_render_function(module):
    return getattr(module, "render", None)