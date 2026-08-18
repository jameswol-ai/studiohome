"""
studiohome
Generative Architecture & Civil Engine
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from rl_engine import RLCityEngine

from modules.registry import (
    build_categories,
    build_module_mapping,
    get_render_function,
)

from modules.routing import (
    validate_quick_action_route,
)


# =====================================================
# STREAMLIT PAGE CONFIGURATION
# Must be the first Streamlit command.
# =====================================================

st.set_page_config(
    page_title="studiohome | Generative Architecture & Civil Engine",
    page_icon="🏛️",
    layout="wide",
)


# =====================================================
# UNIFIED GLOBAL PROJECT STATE
# =====================================================

if "rl_engine" not in st.session_state:
    st.session_state.rl_engine = RLCityEngine()


if "project" not in st.session_state:
    st.session_state.project = {
        "intent": (
            "A cutting-edge net-zero carbon 12-storey "
            "hybrid mass-timber innovation hub"
        ),
        "typology": "Commercial Innovation Hub",
        "site_area": 2500.0,
        "floors": 12,
        "grid_spacing": 8.0,
        "structural_system": "Mass Timber CLT & Glulam Frame",
        "live_load": 4.0,
        "unit_rate": 1650.0,
        "total_gfa": 30000.0,
        "estimated_cost": 49500000.0,
        "carbon_score": 420.0,
        "energy_rating": "LEED Platinum",
    }


if "active_tab" not in st.session_state:
    params = st.query_params

    st.session_state.active_tab = params.get(
        "tab",
        "Executive Cockpit",
    )


if "civilization_state" not in st.session_state:
    st.session_state.civilization_state = {
        "stability": 0.91,
        "conflict": 0.12,
        "innovation": 0.88,
        "culture_score": 0.82,
    }


# =====================================================
# MODULE REGISTRY
# =====================================================

categories = build_categories()

module_mapping = build_module_mapping()


flat_tab_labels = [
    tab
    for tabs in categories.values()
    for tab in tabs
]


# =====================================================
# ACTIVE TAB NORMALIZATION
# =====================================================

if st.session_state.active_tab not in flat_tab_labels:
    st.session_state.active_tab = "Executive Cockpit"


# =====================================================
# GLOBAL UI / GLASSMORPHISM
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgb(13, 20, 38) 0%,
                rgb(7, 11, 20) 85%
            );

        color: #F1F5F9;

        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            sans-serif;
    }

    .studio-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 14px;

        padding: 12px 0 20px 0;

        border-bottom:
            1px solid rgba(255, 255, 255, 0.08);

        margin-bottom: 20px;
    }

    .studio-logo-icon {
        width: 42px;
        height: 42px;

        background:
            linear-gradient(
                135deg,
                #3B82F6,
                #1D4ED8
            );

        border-radius: 12px;

        display: flex;
        align-items: center;
        justify-content: center;

        box-shadow:
            0 6px 20px
            rgba(59, 130, 246, 0.45);
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

    .glass-card {
        background:
            rgba(30, 41, 59, 0.4);

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);

        border:
            1px solid rgba(255, 255, 255, 0.08);

        border-radius: 18px;

        padding: 28px;

        margin-bottom: 24px;

        box-shadow:
            0 12px 40px 0
            rgba(0, 0, 0, 0.45);
    }

    h1,
    h2,
    h3 {
        letter-spacing: -0.6px;
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] {
        background-color:
            rgba(11, 17, 32, 0.9);

        border-right:
            1px solid rgba(255, 255, 255, 0.06);
    }

    .stButton button {
        background:
            linear-gradient(
                135deg,
                #3B82F6,
                #2563EB
            );

        color: white;

        border: none;

        border-radius: 10px;

        font-weight: 600;

        padding: 0.6rem 1.2rem;

        box-shadow:
            0 4px 15px
            rgba(59, 130, 246, 0.3);

        transition:
            all 0.25s ease-in-out;
    }

    .stButton button:hover {
        background:
            linear-gradient(
                135deg,
                #2563EB,
                #1D4ED8
            );

        box-shadow:
            0 6px 20px
            rgba(59, 130, 246, 0.5);

        transform:
            translateY(-2px);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# SIDEBAR BRANDING
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div class="studio-logo-wrapper">

            <div class="studio-logo-icon">

                <svg
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                >
                    <path d="
                        M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3z
                    "/>
                </svg>

            </div>

            <div class="studio-logo-text">
                studio<span>home</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            font-size: 11px;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 700;
            margin-bottom: 8px;
        ">
            Navigation Suite
        </p>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

category_names = list(categories.keys())


def get_category_for_tab(tab: str) -> str:
    """
    Return the category containing a tab.

    Falls back to the first category.
    """

    for category, tabs in categories.items():

        if tab in tabs:
            return category

    return category_names[0]


def normalize_active_tab() -> None:
    """
    Ensure active_tab always points to a registered tab.
    """

    active_tab_value = st.session_state.get(
        "active_tab",
        "Executive Cockpit",
    )

    if active_tab_value not in flat_tab_labels:

        st.session_state.active_tab = (
            "Executive Cockpit"
        )


def on_category_change() -> None:
    """
    Synchronize active_tab when the user changes category.
    """

    category = st.session_state.module_category

    tabs = categories.get(category, [])

    if not tabs:
        return

    current_tab = st.session_state.get(
        "active_tab",
        "Executive Cockpit",
    )

    if current_tab in tabs:
        st.session_state.tab_radio = current_tab
        return

    st.session_state.active_tab = tabs[0]
    st.session_state.tab_radio = tabs[0]


def on_tab_change() -> None:
    """
    Synchronize active_tab when the user changes module.
    """

    selected_tab = st.session_state.tab_radio

    if selected_tab not in flat_tab_labels:
        return

    st.session_state.active_tab = selected_tab

    category = get_category_for_tab(
        selected_tab
    )

    st.session_state.module_category = category


normalize_active_tab()


active_category = get_category_for_tab(
    st.session_state.active_tab
)


# -----------------------------------------------------
# Synchronize widget state before rendering widgets.
# -----------------------------------------------------

if (
    st.session_state.get("module_category")
    not in category_names
):
    st.session_state.module_category = (
        active_category
    )


if (
    st.session_state.get("tab_radio")
    not in flat_tab_labels
):
    st.session_state.tab_radio = (
        st.session_state.active_tab
    )


with st.sidebar:

    selected_category = st.selectbox(
        "Module Category",
        category_names,
        index=category_names.index(
            st.session_state.module_category
        ),
        key="module_category",
        on_change=on_category_change,
        label_visibility="collapsed",
    )


    available_tabs = categories.get(
        selected_category,
        [],
    )


    if not available_tabs:

        st.error(
            f"No modules registered for "
            f"category '{selected_category}'."
        )

        active_tab = st.session_state.active_tab

    else:

        if (
            st.session_state.active_tab
            not in available_tabs
        ):
            st.session_state.active_tab = (
                available_tabs[0]
            )


        if (
            st.session_state.get("tab_radio")
            not in available_tabs
        ):
            st.session_state.tab_radio = (
                st.session_state.active_tab
            )


        active_tab = st.radio(
            "Select panel",
            available_tabs,
            index=available_tabs.index(
                st.session_state.active_tab
            ),
            key="tab_radio",
            on_change=on_tab_change,
            label_visibility="collapsed",
        )


st.session_state.active_tab = active_tab


# =====================================================
# SAFE QUICK-ACTION NAVIGATION
# =====================================================

def route_cockpit_action(action: str) -> None:
    """
    Validate and execute a cockpit quick action.

    The application only calls st.rerun() after the
    destination has passed both registry checks.
    """

    (
        valid,
        destination,
        error,
    ) = validate_quick_action_route(
        action=action,
        module_mapping=module_mapping,
        flat_tab_labels=flat_tab_labels,
    )


    # -------------------------------------------------
    # Validation failure
    # -------------------------------------------------

    if not valid:

        st.error(
            f"🚨 Quick-action routing error: "
            f"{error}"
        )

        return


    # -------------------------------------------------
    # Defensive destination check
    # -------------------------------------------------

    if destination is None:

        st.error(
            f"🚨 Quick-action '{action}' produced "
            "an empty destination."
        )

        return


    if destination not in flat_tab_labels:

        st.error(
            f"🚨 Cannot navigate to "
            f"'{destination}'. "
            "The destination is not registered "
            "in flat_tab_labels."
        )

        return


    if destination not in module_mapping:

        st.error(
            f"🚨 Cannot navigate to "
            f"'{destination}'. "
            "The destination is not registered "
            "in module_mapping."
        )

        return


    if module_mapping[destination] is None:

        st.error(
            f"🚨 Cannot navigate to "
            f"'{destination}'. "
            "The destination has no registered module."
        )

        return


    # -------------------------------------------------
    # Commit navigation
    # -------------------------------------------------

    st.session_state.active_tab = destination

    st.session_state.module_category = (
        get_category_for_tab(destination)
    )

    st.session_state.tab_radio = destination

    st.rerun()


# =====================================================
# EXECUTIVE COCKPIT
# =====================================================

def render_executive_cockpit() -> None:
    """
    Render the Executive Project Cockpit.
    """

    st.markdown(
        "## 🏛️ studiohome | Executive Project Cockpit"
    )

    st.markdown(
        """
        Master control hub monitoring live
        multi-disciplinary parameters synced across
        all design, engineering, and regulatory agents.
        """
    )


    project = st.session_state.project


    # =================================================
    # GLASS CARD
    # =================================================

    st.markdown(
        '<div class="glass-card">',
        unsafe_allow_html=True,
    )


    # =================================================
    # KPI ROW
    # =================================================

    c1, c2, c3, c4, c5 = st.columns(5)


    c1.metric(
        "Active Typology",
        project["typology"].split()[0],
    )


    c2.metric(
        "Project CAPEX",
        f"${project['estimated_cost']:,.0f}",
    )


    c3.metric(
        "Embodied Carbon",
        f"{project['carbon_score']} tCO₂e",
    )


    c4.metric(
        "Storey Height",
        f"{project['floors']} Levels",
    )


    c5.metric(
        "System Status",
        "Synchronized",
        "Live",
    )


    # =================================================
    # ECOSYSTEM TELEMETRY
    # =================================================

    st.markdown(
        "### 📊 Synchronized Ecosystem Telemetry"
    )


    df_overview = pd.DataFrame(
        {
            "Discipline Module": [
                "AI Synthesis",
                "Architecture",
                "Structure (FEA)",
                "MEP & Energy",
                "Zoning Compliance",
                "Cost Pro-Forma",
            ],
            "Performance Index (%)": [
                98,
                94,
                96,
                91,
                100,
                93,
            ],
        }
    )


    fig = px.bar(
        df_overview,
        x="Discipline Module",
        y="Performance Index (%)",
        color="Performance Index (%)",
        title=(
            "Unified Cross-Module "
            "Engineering Performance"
        ),
        template="plotly_dark",
        height=320,
        range_y=[80, 100],
    )


    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            t=40,
            b=10,
            l=10,
            r=10,
        ),
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
    )


    # =================================================
    # QUICK ACTIONS
    # =================================================

    st.markdown(
        "### 🚀 Quick Inter-Module Actions"
    )


    col_a, col_b, col_c = st.columns(3)


    with col_a:

        if st.button(
            "📜 Run Zoning Code Audit",
            use_container_width=True,
            key="cockpit_zoning",
        ):

            route_cockpit_action(
                "zoning_audit"
            )


    with col_b:

        if st.button(
            "⚡ Run Full Simulation Audit",
            use_container_width=True,
            key="cockpit_full_sim",
        ):

            route_cockpit_action(
                "full_simulation"
            )


    with col_c:

        if st.button(
            "📦 Export Unified BIM Suite",
            use_container_width=True,
            key="cockpit_export",
        ):

            route_cockpit_action(
                "export_bim"
            )


    # =================================================
    # CLOSE GLASS CARD
    # =================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# =====================================================
# ACTIVE MODULE RENDERING
# =====================================================

if active_tab == "Executive Cockpit":

    render_executive_cockpit()


elif active_tab in module_mapping:

    module = module_mapping[active_tab]


    if module is None:

        st.error(
            f"Module '{active_tab}' is registered "
            "but has no module implementation."
        )


    else:

        render = get_render_function(module)


        if render is None:

            st.error(
                f"Module '{active_tab}' does not expose "
                "a callable render() function."
            )


        else:

            try:

                render()

            except Exception as exc:

                st.error(
                    f"Unable to render '{active_tab}'."
                )

                with st.expander(
                    "Technical details",
                    expanded=False,
                ):

                    st.exception(exc)


else:

    st.error(
        f"Unknown module: '{active_tab}'"
    )


# =====================================================
# SIDEBAR FOOTER
# =====================================================

st.sidebar.markdown("---")


st.sidebar.caption(
    f"Active Module: **{st.session_state.active_tab}**"
)