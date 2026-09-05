"""studiohome | Architecture, Engineering, Construction + MEP design workspace."""
from __future__ import annotations

import re

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


# Central UI sanitation: imported modules may still contain legacy emoji labels.
# Strip them at the Streamlit boundary so the deployed application remains emoji-free.
_EMOJI_RE = re.compile(
    "["
    "\\U0001F1E6-\\U0001F1FF"
    "\\U0001F300-\\U0001F5FF"
    "\\U0001F600-\\U0001F64F"
    "\\U0001F680-\\U0001F6FF"
    "\\U0001F700-\\U0001F77F"
    "\\U0001F780-\\U0001F7FF"
    "\\U0001F800-\\U0001F8FF"
    "\\U0001F900-\\U0001F9FF"
    "\\U0001FA00-\\U0001FAFF"
    "\\U00002700-\\U000027BF"
    "\\U00002600-\\U000026FF"
    "\\U00002300-\\U000023FF"
    "]+",
    flags=re.UNICODE,
)


def _strip_emojis(value):
    """Remove emoji and common pictographic symbols from UI text."""
    if isinstance(value, str):
        return _EMOJI_RE.sub("", value).strip()
    return value


def _wrap_streamlit_text_method(method):
    """Wrap a Streamlit text-facing method without changing its API."""
    def wrapper(*args, **kwargs):
        cleaned_args = tuple(_strip_emojis(arg) for arg in args)
        for key in ("label", "caption", "text", "body", "value", "help"):
            if key in kwargs:
                kwargs[key] = _strip_emojis(kwargs[key])
        return method(*cleaned_args, **kwargs)

    wrapper.__name__ = getattr(method, "__name__", "wrapped_streamlit_method")
    return wrapper


# Apply once per process. This protects the entire module registry, not only this file.
if not getattr(st, "_studiohome_emoji_filter_installed", False):
    for _method_name in (
        "markdown",
        "write",
        "text",
        "caption",
        "title",
        "header",
        "subheader",
        "button",
        "checkbox",
        "radio",
        "selectbox",
        "multiselect",
        "text_input",
        "text_area",
        "number_input",
        "slider",
        "select_slider",
        "date_input",
        "time_input",
        "metric",
        "success",
        "info",
        "warning",
        "error",
        "exception",
        "progress",
    ):
        if hasattr(st, _method_name):
            setattr(st, _method_name, _wrap_streamlit_text_method(getattr(st, _method_name)))
    st._studiohome_emoji_filter_installed = True


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


def navigate_to(tab: str) -> None:
    if tab not in flat_tab_labels:
        return
    st.session_state.active_tab = tab
    st.session_state.module_category = get_category_for_tab(tab)
    st.session_state.tab_radio = tab
    st.query_params["tab"] = tab
    st.rerun()


def route_cockpit_action(action: str) -> None:
    valid, destination, error = validate_quick_action_route(
        action, module_mapping, flat_tab_labels
    )
    if not valid:
        st.error(f"Quick-action routing error: {error}")
        return
    navigate_to(destination)


st.markdown(
    """
    <style>
    :root {
        --studio-black: #111111;
        --studio-red: #D40000;
        --studio-white: #FFFFFF;
        --studio-gray: #F4F4F4;
        --studio-border: #DDDDDD;
        --studio-muted: #666666;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: var(--studio-white) !important;
        color: var(--studio-black) !important;
    }

    [data-testid="stHeader"] {
        background: var(--studio-white) !important;
        border-bottom: 1px solid var(--studio-border);
    }

    [data-testid="stSidebar"] {
        background: var(--studio-white) !important;
        border-right: 1px solid var(--studio-border);
    }

    [data-testid="stSidebar"] > div {
        background: var(--studio-white) !important;
    }

    .block-container {
        max-width: 1540px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, h5, h6, p, label,
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"], [data-testid="stCaptionContainer"] {
        color: var(--studio-black) !important;
        text-shadow: none !important;
    }

    h1, h2, h3, h4, h5, h6 {
        letter-spacing: -0.45px;
        text-shadow: none !important;
    }

    .studio-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 2px 0 15px;
        margin-bottom: 12px;
        border-bottom: 1px solid var(--studio-border);
    }

    .studio-logo-icon {
        width: 38px;
        height: 38px;
        min-width: 38px;
        background: var(--studio-red);
        border-radius: 3px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .studio-logo-icon svg {
        width: 21px;
        height: 21px;
        fill: var(--studio-black);
    }

    .studio-logo-text {
        font-size: 23px;
        font-weight: 850;
        letter-spacing: -0.8px;
        line-height: 1;
        color: var(--studio-black) !important;
        text-shadow: none !important;
    }

    .studio-logo-text span { color: var(--studio-black) !important; }

    .sidebar-section-label {
        margin: 18px 0 7px;
        font-size: 10px;
        font-weight: 800;
        color: var(--studio-muted) !important;
        text-transform: uppercase;
        letter-spacing: 1.4px;
    }

    .nav-category {
        margin-top: 13px;
        margin-bottom: 5px;
        padding: 5px 0;
        font-size: 10px;
        font-weight: 850;
        color: var(--studio-muted) !important;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        border-bottom: 1px solid #EEEEEE;
    }

    .nav-active-marker {
        border-left: 3px solid var(--studio-red);
        padding-left: 8px;
        margin: 2px 0;
    }

    .nav-active-marker div {
        font-size: 12px;
        font-weight: 800;
        color: var(--studio-black);
    }

    .stButton > button {
        min-height: 38px;
        padding: 6px 12px;
        background: var(--studio-white) !important;
        color: var(--studio-black) !important;
        border: 1px solid transparent !important;
        border-radius: 3px !important;
        box-shadow: none !important;
        font-weight: 650 !important;
        text-align: left !important;
        transition: background .12s ease, color .12s ease, border-color .12s ease;
    }

    .stButton > button:hover {
        background: var(--studio-gray) !important;
        color: var(--studio-red) !important;
        border-color: #E8E8E8 !important;
        box-shadow: none !important;
    }

    .main .stButton > button {
        background: var(--studio-black) !important;
        color: var(--studio-white) !important;
        border-color: var(--studio-black) !important;
        text-align: center !important;
    }

    .main .stButton > button:hover {
        background: var(--studio-red) !important;
        border-color: var(--studio-red) !important;
        color: var(--studio-white) !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div {
        background: var(--studio-white) !important;
        color: var(--studio-black) !important;
        border: 1px solid #BBBBBB !important;
        border-radius: 3px !important;
        box-shadow: none !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="input"] *,
    [data-baseweb="textarea"] * {
        color: var(--studio-black) !important;
        text-shadow: none !important;
    }

    [data-testid="stMetric"] {
        background: transparent !important;
        border: 0 !important;
        border-left: 3px solid var(--studio-black) !important;
        border-radius: 0 !important;
        padding: 5px 0 5px 11px !important;
        box-shadow: none !important;
    }

    .section-card {
        background: var(--studio-white);
        border: 1px solid var(--studio-border);
        border-top: 2px solid var(--studio-black);
        border-radius: 2px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: none;
    }

    .section-title {
        color: var(--studio-black) !important;
        font-size: 16px;
        font-weight: 800;
        letter-spacing: -0.2px;
        margin-bottom: 10px;
    }

    [data-testid="stAlert"] {
        background: var(--studio-white) !important;
        color: var(--studio-black) !important;
        border: 1px solid var(--studio-border) !important;
        border-left: 3px solid var(--studio-red) !important;
        border-radius: 2px !important;
    }

    [data-testid="stExpander"] {
        background: var(--studio-white) !important;
        border: 1px solid var(--studio-border) !important;
        border-radius: 2px !important;
        box-shadow: none !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--studio-border);
        border-radius: 2px;
    }

    [data-testid="stProgressBar"] > div > div {
        background: var(--studio-red) !important;
    }

    [data-testid="stMarkdownContainer"] a {
        color: var(--studio-red) !important;
    }

    hr {
        border-color: var(--studio-border) !important;
    }

    .workspace-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 0 12px;
        margin-bottom: 12px;
        border-bottom: 1px solid var(--studio-border);
    }

    .workspace-module {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--studio-muted) !important;
    }

    .workspace-module strong {
        color: var(--studio-black) !important;
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
        <div class="sidebar-section-label">Workspace Navigation</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Executive Cockpit", use_container_width=True, key="nav_cockpit"):
        navigate_to(EXECUTIVE_COCKPIT)

    for category, tabs in categories.items():
        st.markdown(f'<div class="nav-category">{category}</div>', unsafe_allow_html=True)
        for tab in tabs:
            if tab == EXECUTIVE_COCKPIT:
                continue
            if tab == st.session_state.active_tab:
                st.markdown(
                    f'<div class="nav-active-marker"><div>{tab}</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                key = "nav_" + "_".join(tab.lower().split())
                if st.button(tab, use_container_width=True, key=key):
                    navigate_to(tab)

    st.markdown("---")
    st.caption(f"Current workspace: {st.session_state.active_tab}")


def render_executive_cockpit() -> None:
    project = st.session_state.project
    family = project.get("design_family", "Commercial")
    status = project.get("design_status", "Concept Ready")

    st.markdown(
        f'<div class="workspace-bar"><div class="workspace-module">Workspace / <strong>{st.session_state.active_tab}</strong></div></div>',
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
            font=dict(color="#111111"),
            margin=dict(t=20, b=10, l=10, r=10),
            showlegend=False,
        )
        fig.update_xaxes(showgrid=False, tickfont=dict(color="#111111"))
        fig.update_yaxes(gridcolor="#E5E5E5", tickfont=dict(color="#111111"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Design Families</div>', unsafe_allow_html=True)
        st.caption("Open a dedicated generator for each building family.")
        for label, key in [
            ("Residential", "residential_design"),
            ("Commercial", "commercial_design"),
            ("Industrial", "industrial_design"),
        ]:
            if st.button(label, use_container_width=True, key=key):
                st.session_state.project["design_family"] = label
                navigate_to(f"{label} Design")
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


active_tab = st.session_state.active_tab

if active_tab == EXECUTIVE_COCKPIT:
    render_executive_cockpit()
elif active_tab in module_mapping:
    module = module_mapping[active_tab]
    if module is None:
        st.error(f"Module '{active_tab}' is registered but has no implementation.")
    else:
        st.markdown(
            f'<div class="workspace-bar"><div class="workspace-module">Workspace / <strong>{active_tab}</strong></div></div>',
            unsafe_allow_html=True,
        )
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
