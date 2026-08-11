import streamlit as st
from rl_engine import RLCityEngine

# Import individual modular panels
from modules import (
    ai_brain, architecture, structure, mep, gis_site, cost, massing,
    export_suite, full_sim, rl_city, city_learning, diplomacy, war,
    culture, consciousness, meta_evo
)

# =====================================================
# SESSION STATE CONFIG
# =====================================================
if "rl_engine" not in st.session_state:
    st.session_state.rl_engine = RLCityEngine()
if "active_tab" not in st.session_state:
    params = st.query_params
    st.session_state.active_tab = params.get("tab", "AI Brain")
if "civilization_state" not in st.session_state:
    st.session_state.civilization_state = {
        "stability": 0.85,
        "conflict": 0.20,
        "innovation": 0.78,
        "culture_score": 0.65
    }

st.set_page_config(page_title="studiohome", page_icon="🏠", layout="wide")

# =====================================================
# GLASSMORPHISM & UI POLISH CSS STYLING
# =====================================================
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(10, 15, 30) 90%);
        color: #F8FAFC;
    }
    .studio-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 16px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 16px;
    }
    .studio-logo-icon {
        width: 38px;
        height: 38px;
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    .studio-logo-icon svg {
        width: 20px;
        height: 20px;
        fill: #FFFFFF;
    }
    .studio-logo-text {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .studio-logo-text span {
        color: #3B82F6;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    h1, h2, h3 {
        letter-spacing: -0.5px;
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stButton button {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Render Custom Logo in Sidebar
with st.sidebar:
    st.markdown("""
        <div class="studio-logo-wrapper">
            <div class="studio-logo-icon">
                <svg viewBox="0 0 24 24"><path d="M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3z"/></svg>
            </div>
            <div class="studio-logo-text">studio<span>home</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin-bottom: 8px;'>Navigation Suite</p>", unsafe_allow_html=True)

# Category Mapping Dictionary
categories = {
    "Design & Engineering": [
        "AI Brain", "Architecture", "Structure", "MEP",
        "GIS & Site", "Cost", "Massing", "Export Suite", "Full Sim"
    ],
    "Urban & Civilization": [
        "RL City", "City Learning", "Diplomacy", "War",
        "Culture", "Consciousness", "Meta-Evo"
    ]
}

flat_tab_labels = [tab for tabs in categories.values() for tab in tabs]

if st.session_state.active_tab not in flat_tab_labels:
    st.session_state.active_tab = flat_tab_labels[0]

with st.sidebar:
    selected_category = st.selectbox(
        "Module Category", 
        list(categories.keys()),
        label_visibility="collapsed"
    )
    
    active_tab = st.radio(
        "Select panel",
        categories[selected_category],
        index=categories[selected_category].index(st.session_state.active_tab) if st.session_state.active_tab in categories[selected_category] else 0,
        key="tab_radio",
        label_visibility="collapsed"
    )
st.session_state.active_tab = active_tab

# =========================================================
# MODULE ROUTER MAPPING
# =========================================================
module_mapping = {
    "AI Brain": ai_brain,
    "Architecture": architecture,
    "Structure": structure,
    "MEP": mep,
    "GIS & Site": gis_site,
    "Cost": cost,
    "Massing": massing,
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

# Execute active panel render method
if active_tab in module_mapping:
    module_mapping[active_tab].render()

# ---- FOOTER ----
st.sidebar.markdown("---")
st.sidebar.caption(f"Active: **{st.session_state.active_tab}**")
