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
        "stability": 0.88,
        "conflict": 0.15,
        "innovation": 0.82,
        "culture_score": 0.74
    }

st.set_page_config(page_title="studiohome | Generative Architecture & Civil Engine", page_icon="🏛️", layout="wide")

# =====================================================
# GLASSMORPHISM & ELITE UI POLISH CSS STYLING
# =====================================================
st.markdown("""
    <style>
    /* App Wide Background & Font Enhancement */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgb(13, 20, 38) 0%, rgb(7, 11, 20) 85%);
        color: #F1F5F9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Sleek Custom Logo in Sidebar */
    .studio-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    .studio-logo-icon {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45);
    }
    .studio-logo-icon svg {
        width: 22px;
        height: 22px;
        fill: #FFFFFF;
    }
    .studio-logo-text {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #FFFFFF;
    }
    .studio-logo-text span {
        color: #3B82F6;
    }

    /* Advanced Glassmorphism Containers */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
    }
    
    /* Typography Polish */
    h1, h2, h3 {
        letter-spacing: -0.6px;
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar Styling Polish */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 17, 32, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    /* Sleek Modern Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: all 0.25s ease-in-out;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
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
st.sidebar.caption(f"Active Module: **{st.session_state.active_tab}**")
