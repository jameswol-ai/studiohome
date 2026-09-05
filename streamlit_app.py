"""studiohome | Architecture, Engineering, Construction + MEP design workspace."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from rl_engine import RLCityEngine
from modules.registry import build_categories, build_module_mapping, get_render_function
from modules.routing import validate_quick_action_route


# =====================================================
# PAGE CONFIGURATION
# MUST BE THE FIRST STREAMLIT COMMAND
# =====================================================

st.set_page_config(
    page_title="studiohome | AEC + MEP Design Studio",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# PROJECT STATE
# =====================================================

if "rl_engine" not in st.session_state:
    st.session_state.rl_engine = RLCityEngine()

if "project" not in st.session_state:
    st.session_state.project = {
        "project_name": "studiohome AEC Project",
        "client": "Studiohome Development",
        "intent": "A cutting-edge net-zero carbon 12-storey hybrid mass-timber innovation hub",
        "typology": "Commercial Innovation Hub",
        "site_area": 2500.0,
        "floors": 12,
        "grid_spacing": 8.0,
        "floor_to_floor": 3.5,
        "structural_system": "Mass Timber CLT & Glulam Frame",
        "live_load": 4.0,
        "unit_rate": 1650.0,
        "total_gfa": 30000.0,
        "estimated_cost": 49500000.0,
        "carbon_score": 420.0,
        "energy_rating": "LEED Platinum",
        "energy_target": "Net-Zero Ready",
        "code_basis": "International / IBC",
    }

if "active_tab" not in st.session_state:
    requested_tab = st.query_params.get("tab", "Executive Cockpit")
    st.session_state.active_tab = requested_tab

if "civilization_state" not in st.session_state:
    st.session_state.civilization_state = {
        "stability": 0.91,
        "conflict": 0.12,
        "innovation": 0.88,
        "culture_score": 0.82,
    }


# =====================================================
# REGISTRY
# =====================================================

categories = build_categories()
module_mapping = build_module_mapping()
flat_tab_labels = [tab for tabs in categories.values() for tab in tabs]
category_names = list(categories.keys())

EXECUTIVE_COCKPIT = "Executive Cockpit"

if st.session_state.active_tab not in flat_tab_labels:
    st.session_state.active_tab = EXECUTIVE_COCKPIT


def get_category_for_tab(tab: str) -> str:
    for category, tabs in categories.items():
        if tab in tabs:
            return category
    return category_names[0]


def sync_navigation_state() -> None:
    """Keep category, radio and active_tab internally consistent."""
    active_tab = st.session_state.get("active_tab", EXECUTIVE_COCKPIT)
    if active_tab not in flat_tab_labels:
        active_tab = EXECUTIVE_COCKPIT
        st.session_state.active_tab = active_tab

    category = get_category_for_tab(active_tab)
    if st.session_state.get("module_category") not in category_names:
        st.session_state.module_category = category

    selected_category = st.session_state.module_category
    tabs = categories.get(selected_category, [])
    if not tabs:
        st.session_state.module_category = category
        tabs = categories.get(category, [])

    if st.session_state.get("tab_radio") not in tabs:
        st.session_state.tab_radio = active_tab if active_tab in tabs else tabs[0]


def on_category_change() -> None:
    category = st.session_state.get("module_category")
    tabs = categories.get(category, [])
    if not tabs:
        return
    current = st.session_state.get("active_tab")
    selected = current if current in tabs else tabs[0]
    st.session_state.active_tab = selected
    st.session_state.tab_radio = selected


def on_tab_change() -> None:
    selected = st.session_state.get("tab_radio")
    if selected not in flat_tab_labels:
        return
    st.session_state.active_tab = selected
    st.session_state.module_category = get_category_for_tab(selected)


sync_navigation_state()


# =====================================================
# GLOBAL UI
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgb(13,20,38) 0%, rgb(7,11,20) 85%);
        color: #F1F5F9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    [data-testid="stSidebar"] {
        background: rgba(11,17,32,0.97);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .studio-logo-wrapper {
        display:flex; align-items:center; gap:14px;
        padding:12px 0 20px; margin-bottom:20px;
        border-bottom:1px solid rgba(255,255,255,0.08);
    }
    .studio-logo-icon {
        width:42px; height:42px; min-width:42px;
        background:linear-gradient(135deg,#3B82F6,#1D4ED8);
        border-radius:12px; display:flex; align-items:center; justify-content:center;
        box-shadow:0 6px 20px rgba(59,130,246,0.45);
    }
    .studio-logo-icon svg { width:22px; height:22px; fill:#FFFFFF; }
    .studio-logo-text { font-size:24px; font-weight:800; letter-spacing:-0.8px; color:#FFFFFF; line-height:1; }
    .studio-logo-text span { color:#3B82F6; }
    .glass-card {
        background:rgba(30,41,59,0.40); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px);
        border:1px solid rgba(255,255,255,0.08); border-radius:18px; padding:28px; margin-bottom:24px;
        box-shadow:0 12px 40px rgba(0,0,0,0.45);
    }
    h1,h2,h3 { letter-spacing:-0.6px; color:#F8FAFC !important; font-weight:700 !important; }
    .stButton button {
        background:linear-gradient(135deg,#3B82F6,#2563EB); color:#FFFFFF; border:none; border-radius:10px;
        font-weight:600; padding:.6rem 1.2rem; box-shadow:0 4px 15px rgba(59,130,246,.30);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown(
        """
        <div class="studio-logo-wrapper">
            <div class="studio-logo-icon">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 3 L2 12 h3 v8 h6 v-6 h2 v6 h6 v-8 h3 L12 3 z"/>
                </svg>
            </div>
            <div class="studio-logo-text">studio<span>home</span></div>
        </div>
        <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:1.2px;font-weight:700;margin-bottom:8px;">
            AEC + MEP Design Studio
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_category = st.selectbox(
        "Module Category",
        category_names,
        index=category_names.index(st.session_state.module_category),
        key="module_category",
        on_change=on_category_change,
        label_visibility="collapsed",
    )

    available_tabs = categories.get(selected_category, [])
    if not available_tabs:
        st.error(f"No modules registered for '{selected_category}'.")
        active_tab = EXECUTIVE_COCKPIT
    else:
        if st.session_state.active_tab not in available_tabs:
            st.session_state.active_tab = available_tabs[0]
        if st.session_state.get("tab_radio") not in available_tabs:
            st.session_state.tab_radio = st.session_state.active_tab

        active_tab = st.radio(
            "Select panel",
            available_tabs,
            index=available_tabs.index(st.session_state.active_tab),
            key="tab_radio",
            on_change=on_tab_change,
            label_visibility="collapsed",
        )

    st.session_state.active_tab = active_tab


# =====================================================
# QUICK ACTIONS
# =====================================================

def route_cockpit_action(action: str) -> None:
    valid, destination, error = validate_quick_action_route(
        action=action,
        module_mapping=module_mapping,
        flat_tab_labels=flat_tab_labels,
    )
    if not valid:
        st.error(f"🚨 Quick-action routing error: {error}")
        return
    if destination is None:
        st.error(f"🚨 Quick-action '{action}' returned no destination.")
        return
    if destination not in flat_tab_labels:
        st.error(f"🚨 '{destination}' is not registered in navigation.")
        return
    if destination not in module_mapping:
        st.error(f"🚨 '{destination}' is missing from module_mapping.")
        return
    if module_mapping[destination] is None:
        st.error(f"🚨 '{destination}' has no module implementation.")
        return

    st.session_state.active_tab = destination
    st.session_state.module_category = get_category_for_tab(destination)
    st.session_state.tab_radio = destination
    st.rerun()


# =====================================================
# EXECUTIVE COCKPIT
# =====================================================

def render_executive_cockpit() -> None:
    project = st.session_state.project
    st.markdown("# 🏛️ studiohome | AEC + MEP Executive Cockpit")
    st.caption("Integrated Architecture, Engineering, Construction, Mechanical, Electrical and Plumbing design coordination workspace.")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Project", project.get("project_name", "AEC Project"))
    c2.metric("GFA", f"{project.get('total_gfa', 0):,.0f} m²")
    c3.metric("CAPEX", f"${project.get('estimated_cost', 0):,.0f}")
    c4.metric("Storeys", f"{project.get('floors', 0)}")
    c5.metric("Design Status", "Coordinated", "Live")

    st.markdown("### 🧩 Multidisciplinary Design Readiness")
    df = pd.DataFrame({
        "Discipline": ["Architecture", "Structure", "Civil", "Mechanical", "Electrical", "Plumbing / Fire", "BIM / Export", "Cost"],
        "Readiness (%)": [94, 96, 89, 91, 90, 88, 92, 93],
    })
    fig = px.bar(df, x="Discipline", y="Readiness (%)", color="Readiness (%)", range_y=[75,100], template="plotly_dark", height=340)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30,b=10,l=10,r=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ⚡ Design Coordination Shortcuts")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("🧭 Project Setup", use_container_width=True, key="cockpit_project"):
            route_cockpit_action("project_setup")
    with b2:
        if st.button("🏗️ Architecture", use_container_width=True, key="cockpit_arch"):
            route_cockpit_action("architecture_design")
    with b3:
        if st.button("⚡ MEP + Electrical", use_container_width=True, key="cockpit_mep"):
            route_cockpit_action("mep_design")
    with b4:
        if st.button("🚿 Plumbing + Fire", use_container_width=True, key="cockpit_plumbing"):
            route_cockpit_action("plumbing_fire")

    st.markdown("### 🏢 AEC Delivery Stack")
    st.info("Brief → Site → Architecture → Massing → Envelope → Structure → Civil → Mechanical → Electrical → Plumbing & Fire → Cost → Simulation → BIM / Documentation")
    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# ACTIVE MODULE ROUTER
# =====================================================

if active_tab == EXECUTIVE_COCKPIT:
    render_executive_cockpit()
elif active_tab in module_mapping:
    module = module_mapping[active_tab]
    if module is None:
        st.error(f"Module '{active_tab}' is registered but has no implementation.")
    else:
        render = get_render_function(module)
        if render is None:
            st.error(f"Module '{active_tab}' does not expose a callable render() function.")
        else:
            try:
                render()
            except Exception as exc:
                st.error(f"Unable to render '{active_tab}'.")
                with st.expander("Technical details", expanded=False):
                    st.exception(exc)
else:
    st.error(f"Unknown module: '{active_tab}'")


# =====================================================
# FOOTER
# =====================================================

st.sidebar.markdown("---")
st.sidebar.caption(f"Active Module: **{st.session_state.active_tab}**")
