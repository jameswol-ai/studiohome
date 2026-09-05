"""Parametric design generator for residential, commercial and industrial projects."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.design_state import apply_design_state, build_design_state

DESIGN_FAMILIES = {
    "Residential": {"typologies": ["Apartment Building", "Townhouse Development", "Mixed Residential Block", "Student Housing"], "default_floors": 8, "default_grid": 7.2, "default_unit": 1450.0},
    "Commercial": {"typologies": ["Office Building", "Retail Centre", "Mixed-Use Commercial", "Innovation Hub"], "default_floors": 10, "default_grid": 8.0, "default_unit": 1750.0},
    "Industrial": {"typologies": ["Manufacturing Facility", "Warehouse and Distribution", "Food Processing Plant", "Light Industrial Campus"], "default_floors": 2, "default_grid": 12.0, "default_unit": 1250.0},
}


def _plan(state: dict) -> go.Figure:
    width = state["floorplate_width"]
    depth = state["floorplate_depth"]
    grid_x = state["actual_grid_spacing_x"]
    grid_y = state["actual_grid_spacing_y"]
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#111111"), height=560,
        margin=dict(l=20, r=20, t=45, b=20), title=f'{state["design_family"].upper()} CONCEPT FLOOR PLAN',
        xaxis=dict(range=[-2, width + 2], visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-2, depth + 2], visible=False), showlegend=False,
    )
    fig.add_shape(type="rect", x0=0, y0=0, x1=width, y1=depth, line=dict(color="#111111", width=4), fillcolor="rgba(255,255,255,0)")
    for i in range(1, state["grid_bays_x"]):
        x = i * grid_x
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=depth, line=dict(color="#777777", width=1, dash="dot"))
    for i in range(1, state["grid_bays_y"]):
        y = i * grid_y
        fig.add_shape(type="line", x0=0, y0=y, x1=width, y1=y, line=dict(color="#777777", width=1, dash="dot"))
    core_w = width * 0.22
    core_d = depth * 0.32
    cx = (width - core_w) / 2
    cy = (depth - core_d) / 2
    fig.add_shape(type="rect", x0=cx, y0=cy, x1=cx + core_w, y1=cy + core_d, line=dict(color="#D40000", width=3), fillcolor="rgba(212,0,0,0.06)")
    fig.add_annotation(x=cx + core_w / 2, y=cy + core_d / 2, text="CORE", showarrow=False, font=dict(color="#111111", size=13))
    fig.add_annotation(x=width / 2, y=-1, text=f'GRID {grid_x:.1f} x {grid_y:.1f} m | {state["floors"]} STOREYS', showarrow=False, font=dict(color="#111111", size=11))
    return fig


def render():
    st.markdown("## Generative Design Studio")
    st.markdown("Generate a coordinated concept and publish shared geometry for downstream AEC modules.")
    family = st.radio("Design Family", list(DESIGN_FAMILIES), horizontal=True, key="design_family")
    cfg = DESIGN_FAMILIES[family]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        typology = st.selectbox("Typology", cfg["typologies"], key=f"typology_{family}")
    with c2:
        site_area = st.number_input("Site Area (m²)", min_value=200.0, value=2500.0, step=100.0, key=f"site_area_{family}")
    with c3:
        floors = st.number_input("Storeys", min_value=1, max_value=80, value=cfg["default_floors"], step=1, key=f"floors_{family}")
    with c4:
        grid = st.number_input("Structural Grid (m)", min_value=4.0, max_value=24.0, value=cfg["default_grid"], step=0.4, key=f"grid_{family}")
    if st.button("Generate Design", use_container_width=True, key="generate_design"):
        state = build_design_state(st.session_state.project, family=family, typology=typology, site_area=site_area, floors=int(floors), grid_spacing=grid, unit_rate=cfg["default_unit"])
        apply_design_state(st.session_state.project, state)
    p = st.session_state.project
    if p.get("design_family") == family and p.get("floorplate_width"):
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Design Family", family)
        m2.metric("GFA", f'{p["total_gfa"]:,.0f} m²')
        m3.metric("Indicative CAPEX", f'${p["estimated_cost"]:,.0f}')
        m4.metric("FAR", f'{p["far"]:.2f}')
        st.markdown("### 2D Concept Plan")
        st.plotly_chart(_plan(p), use_container_width=True, config={"displayModeBar": False})
        schedule = pd.DataFrame(p.get("program_schedule", []), columns=["Program", "Share", "Area (m²)"])
        schedule["Share"] = schedule["Share"].map(lambda x: f"{x:.1%}")
        st.markdown("### Parametric Design Metrics")
        metrics = pd.DataFrame([
            ["Footprint", p["footprint_area"], "m²"], ["Width", p["floorplate_width"], "m"], ["Depth", p["floorplate_depth"], "m"],
            ["Height", p["building_height"], "m"], ["Envelope", p["envelope_area"], "m²"], ["Windows", p["window_area"], "m²"],
            ["Roof", p["roof_area"], "m²"], ["Grid Bays", f'{p["grid_bays_x"]} x {p["grid_bays_y"]}', "bays"], ["Core", p["core_area"], "m²"],
        ], columns=["Metric", "Value", "Unit"])
        st.dataframe(metrics, use_container_width=True, hide_index=True)
        st.markdown("### Program Schedule")
        st.dataframe(schedule, use_container_width=True, hide_index=True)
