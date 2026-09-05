"""studiohome | Architecture, Engineering, Construction + MEP design workspace."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from rl_engine import RLCityEngine
from modules.registry import build_categories, build_module_mapping, get_render_function
from modules.routing import validate_quick_action_route


st.set_page_config(
    page_title="studiohome | AEC + MEP Design Studio",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


if "rl_engine" not in st.session_state:
    st.session_state.rl_engine = RLCityEngine()

if "project" not in st.session_state:
    st.session_state.project = {
        "project_name": "studiohome AEC Project",
        "client": "Studiohome Development",
        "intent": "A cutting-edge net-zero carbon 12-storey hybrid mass-timber innovation hub",
        "typology": "Commercial Innovation Hub",
        "design_family": "Commercial",
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
        "design_status": "Concept Ready",
    }

if "active_tab" not in st.session_state:
    st.session_state.active_tab = st.query_params.get("tab", "Executive Cockpit")

if "civilization_state" not in st.session_state:
    st.session_state.civilization_state = {
        "stability": 0.91,
        "conflict": 0.12,
        "innovation": 0.88,
        "culture_score": 0.82,
    }


categories = build_categories()
module_mapping = build_module_mapping()
flat_tab_labels = [tab for tabs in categories.values() for tab in tabs]
category_names = list(categories)
EXECUTIVE_COCKPIT = "Executive Cockpit"

if st.session_state.active_tab not in flat_tab_labels:
    st.session_state.active_tab = EXECUTIVE_COCKPIT


def get_category_for_tab(tab: str) -> str:
    for category, tabs in categories.items():
        if tab in tabs:
            return category
    return category_names[0]


def sync_navigation_state() -> None:
    active = st.session_state.get("active_tab", EXECUTIVE_COCKPIT)
    if active not in flat_tab_labels:
        active = EXECUTIVE_COCKPIT
        st.session_state.active_tab = active

    category = get_category_for_tab(active)
    if st.session_state.get("module_category") not in category_names:
        st.session_state.module_category = category

    tabs = categories.get(st.session_state.module_category, [])
    if not tabs:
        st.session_state.module_category = category
        tabs = categories[category]

    if st.session_state.get("tab_radio") not in tabs:
        st.session_state.tab_radio = active if active in tabs else tabs[0]


def on_category_change() -> None:
    category = st.session_state.get("module_category")
    tabs = categories.get(category, [])
    if tabs:
        selected = st.session_state.get("active_tab")
        if selected not in tabs:
            selected = tabs[0]
        st.session_state.active_tab = selected
        st.session_state.tab_radio = selected


def on_tab_change() -> None:
    selected = st.session_state.get("tab_radio")
    if selected in flat_tab_labels:
        st.session_state.active_tab = selected
        st.session_state.module_category = get_category_for_tab(selected)
        st.query_params["tab"] = selected


sync_navigation_state()


st.markdown(
    """
    <style>
    :root {
        --studio-black: #000000;
        --studio-red: #D40000;
        --studio-white: #FFFFFF;
        --studio-gray: #F4F4F4;
        --studio-border: #D8D8D8;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stHeader"] {
        background: var(--studio-white) !important;
        color: var(--studio-black) !important;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div {
        background: var(--studio-white) !important;
        border-right: 2px solid var(--studio-black);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .studio-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 18px;
        margin-bottom: 18px;
        border-bottom: 2px solid var(--studio-black);
    }

    .studio-logo-icon {
        width: 40px;
        height: 40px;
        min-width: 40px;
        background: var(--studio-red);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .studio-logo-icon svg {
        width: 22px;
        height: 22px;
        fill: var(--studio-black);
    }

    .studio-logo-text {
        font-size: 23px;
        font-weight: 850;
        letter-spacing: -0.8px;
        color: var(--studio-black) !important;
        line-height: 1;
    }

    .studio-logo-text span { color: var(--studio-black) !important; }

    .hero {
        background: var(--studio-black);
        color: var(--studio-white);
        border-radius: 14px;
        padding: 30px 34px;
        margin-bottom: 22px;
        border-left: 8px solid var(--studio-red);
    }

    .hero h1, .hero p, .hero span { color: var(--studio-white) !important; }
    .hero h1 { margin: 0 0 7px 0; font-size: 34px; letter-spacing: -1.2px; }
    .hero p { margin: 0; opacity: .86; }

    .section-card {
        background: var(--studio-white);
        border: 1px solid var(--studio-border);
        border-top: 4px solid var(--studio-black);
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 18px;
        font-weight: 800;
        color: var(--studio-black);
        margin-bottom: 14px;
    }

    h1, h2, h3, h4, h5, h6, p, label,
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: var(--studio-black) !important;
    }

    [data-testid="stCaptionContainer"] { color: #333333 !important; }

    .stButton button {
        background: var(--studio-black) !important;
        color: var(--studio-white) !important;
        border: 2px solid var(--studio-black) !important;
        border-radius: 8px !important;
        font-weight: 750 !important;
        min-height: 42px;
    }

    .stButton button:hover {
        background: var(--studio-red) !important;
        color: var(--studio-white) !important;
        border-color: var(--studio-red) !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div {
        background: var(--studio-white) !important;
        border: 1px solid var(--studio-black) !important;
        color: var(--studio-black) !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="input"] *,
    [data-baseweb="textarea"] * {
        color: var(--studio-black) !important;
    }

    [data-testid="stAlert"] {
        background: var(--studio-white) !important;
        color: var(--studio-black) !important;
        border: 1px solid var(--studio-black) !important;
    }

    [data-testid="stExpander"] {
        background: var(--studio-white) !important;
        border: 1px solid var(--studio-border) !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--studio-black);
    }

    [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: var(--studio-black) !important;
        border-bottom-color: var(--studio-red) !important;
    }

    [data-testid="stProgressBar"] > div > div {
        background: var(--studio-red) !important;
    }

    .status-pill {
        display: inline-block;
        padding: 5px 10px;
        border: 1px solid var(--studio-black);
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .6px;
        color: var(--studio-black);
        background: var(--studio-white);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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
        <div style="font-size:11px;color:#000000;text-transform:uppercase;letter-spacing:1.2px;font-weight:800;margin-bottom:8px;">
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
    st.markdown("---")
    st.caption(f"Active Module: **{st.session_state.active_tab}**")


def route_cockpit_action(action: str) -> None:
    valid, destination, error = validate_quick_action_route(
        action, module_mapping, flat_tab_labels
    )
    if not valid:
        st.error(f"Quick-action routing error: {error}")
        return
    st.session_state.active_tab = destination
    st.session_state.module_category = get_category_for_tab(destination)
    st.session_state.tab_radio = destination
    st.query_params["tab"] = destination
    st.rerun()


def render_executive_cockpit() -> None:
    project = st.session_state.project
    family = project.get("design_family", "Commercial")
    status = project.get("design_status", "Concept Ready")

    st.markdown(
        f"""
        <div class="hero">
            <h1>studiohome AEC + MEP Design Studio</h1>
            <p>Integrated project control for architecture, engineering, construction, building systems, cost, simulation and documentation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top = st.columns([2.5, 1, 1, 1])
    with top[0]:
        st.markdown(f"### {project.get('project_name', 'AEC Project')}")
        st.caption(project.get("intent", "Integrated AEC design project"))
    with top[1]:
        st.metric("Design Family", family)
    with top[2]:
        st.metric("Status", status)
    with top[3]:
        st.metric("Code Basis", project.get("code_basis", "Not set"))

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Project Snapshot</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Site", f"{project.get('site_area', 0):,.0f} m²")
    c2.metric("GFA", f"{project.get('total_gfa', 0):,.0f} m²")
    c3.metric("CAPEX", f"${project.get('estimated_cost', 0):,.0f}")
    c4.metric("Storeys", str(project.get("floors", 0)))
    c5.metric("Grid", f"{project.get('grid_spacing', 0):.1f} m")
    c6.metric("Energy", project.get("energy_rating", "Not set"))
    st.markdown('</div>', unsafe_allow_html=True)

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Multidisciplinary Design Readiness</div>', unsafe_allow_html=True)
        readiness = pd.DataFrame(
            {
                "Discipline": [
                    "Architecture", "Structure", "Civil", "Mechanical",
                    "Electrical", "Plumbing / Fire", "BIM / Export", "Cost",
                ],
                "Readiness (%)": [94, 96, 89, 91, 90, 88, 92, 93],
            }
        )
        fig = px.bar(
            readiness,
            x="Discipline",
            y="Readiness (%)",
            range_y=[0, 100],
            template="plotly_white",
            height=350,
        )
        fig.update_traces(marker_color="#D40000")
        fig.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#000000"),
            margin=dict(t=20, b=10, l=10, r=10),
            showlegend=False,
        )
        fig.update_xaxes(showgrid=False, tickfont=dict(color="#000000"))
        fig.update_yaxes(gridcolor="#E5E5E5", tickfont=dict(color="#000000"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Design Families</div>', unsafe_allow_html=True)
        st.caption("Open a dedicated generator for each building family.")
        family_buttons = [
            ("Residential", "residential_design"),
            ("Commercial", "commercial_design"),
            ("Industrial", "industrial_design"),
        ]
        for label, key in family_buttons:
            if st.button(label, use_container_width=True, key=key):
                st.session_state.active_tab = f"{label} Design"
                st.session_state.module_category = "Design Generator"
                st.session_state.tab_radio = f"{label} Design"
                st.session_state.project["design_family"] = label
                st.query_params["tab"] = f"{label} Design"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Design Coordination Shortcuts</div>', unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    shortcuts = [
        (b1, "Project Setup", "project_setup", "cockpit_project"),
        (b2, "Architecture", "architecture_design", "cockpit_arch"),
        (b3, "MEP + Electrical", "mep_design", "cockpit_mep"),
        (b4, "Drawing Studio", "drawing_studio", "cockpit_drawing"),
    ]
    for column, label, action, key in shortcuts:
        with column:
            if st.button(label, use_container_width=True, key=key):
                route_cockpit_action(action)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AEC Delivery Pipeline</div>', unsafe_allow_html=True)
    pipeline = [
        "Brief", "Site", "Architecture", "Floorplates", "Drawing Studio",
        "Massing", "Envelope", "Structure", "Civil", "Mechanical",
        "Electrical", "Plumbing & Fire", "Cost", "Simulation", "BIM / Documentation",
    ]
    st.progress(0.67)
    st.caption(" → ".join(pipeline))
    st.markdown('</div>', unsafe_allow_html=True)


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
