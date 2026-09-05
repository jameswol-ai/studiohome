"""Parametric design generator for residential, commercial and industrial projects."""

from __future__ import annotations

import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DESIGN_FAMILIES = {
    "Residential": {
        "typologies": ["Apartment Building", "Townhouse Development", "Mixed Residential Block", "Student Housing"],
        "default_floors": 8,
        "default_grid": 7.2,
        "default_unit": 1450.0,
        "core_ratio": 0.12,
        "program": [("Residential Units", 0.68), ("Circulation", 0.14), ("Core", 0.12), ("Amenity", 0.06)],
    },
    "Commercial": {
        "typologies": ["Office Building", "Retail Centre", "Mixed-Use Commercial", "Innovation Hub"],
        "default_floors": 10,
        "default_grid": 8.0,
        "default_unit": 1750.0,
        "core_ratio": 0.15,
        "program": [("Work / Retail", 0.63), ("Circulation", 0.12), ("Core", 0.15), ("Amenities", 0.10)],
    },
    "Industrial": {
        "typologies": ["Manufacturing Facility", "Warehouse and Distribution", "Food Processing Plant", "Light Industrial Campus"],
        "default_floors": 2,
        "default_grid": 12.0,
        "default_unit": 1250.0,
        "core_ratio": 0.08,
        "program": [("Production / Storage", 0.72), ("Circulation", 0.10), ("Services", 0.08), ("Administration", 0.10)],
    },
}


def _plan(family: str, width: float, depth: float, grid: float, floors: int) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(color="#000000"),
        height=560,
        margin=dict(l=20, r=20, t=45, b=20),
        title=f"{family.upper()} CONCEPT FLOOR PLAN",
        xaxis=dict(range=[-2, width + 2], visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-2, depth + 2], visible=False),
        showlegend=False,
    )

    def rect(x0, y0, x1, y1, fill="rgba(0,0,0,0)", line_width=4):
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color="#000000", width=line_width), fillcolor=fill)

    rect(0, 0, width, depth, "rgba(255,255,255,0)", 6)
    for x in [i * grid for i in range(1, math.floor(width / grid))]:
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=depth, line=dict(color="#000000", width=1, dash="dot"))
    for y in [i * grid for i in range(1, math.floor(depth / grid))]:
        fig.add_shape(type="line", x0=0, y0=y, x1=width, y1=y, line=dict(color="#000000", width=1, dash="dot"))

    core_w = width * 0.22
    core_d = depth * 0.32
    cx = (width - core_w) / 2
    cy = (depth - core_d) / 2
    rect(cx, cy, cx + core_w, cy + core_d, "rgba(0,0,0,0.12)", 4)
    fig.add_annotation(x=cx + core_w / 2, y=cy + core_d / 2, text="CORE", showarrow=False, font=dict(color="#000000", size=13))

    labels = {
        "Residential": [(width * .20, depth * .72, "LIVING / UNITS"), (width * .78, depth * .72, "LIVING / UNITS"), (width * .20, depth * .25, "LIVING / UNITS"), (width * .78, depth * .25, "LIVING / UNITS")],
        "Commercial": [(width * .18, depth * .72, "WORKSPACE"), (width * .82, depth * .72, "WORKSPACE"), (width * .18, depth * .25, "WORKSPACE"), (width * .82, depth * .25, "AMENITY")],
        "Industrial": [(width * .28, depth * .50, "PRODUCTION / STORAGE"), (width * .76, depth * .50, "PRODUCTION / STORAGE"), (width * .12, depth * .16, "ADMIN"), (width * .86, depth * .16, "SERVICES")],
    }
    for x, y, text in labels[family]:
        fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(color="#000000", size=12))

    fig.add_annotation(x=width / 2, y=-1, text=f"GRID {grid:.1f} m | {floors} STOREYS", showarrow=False, font=dict(color="#000000", size=11))
    return fig


def render():
    st.markdown("## Generative Design Studio")
    st.markdown("Generate a coordinated concept and divide the design system into Residential, Commercial and Industrial families.")

    family = st.radio("Design Family", list(DESIGN_FAMILIES), horizontal=True, key="design_family")
    cfg = DESIGN_FAMILIES[family]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        typology = st.selectbox("Typology", cfg["typologies"], key=f"typology_{family}")
    with c2:
        site_area = st.number_input("Site Area (m²)", min_value=200.0, value=2500.0, step=100.0)
    with c3:
        floors = st.number_input("Storeys", min_value=1, max_value=80, value=cfg["default_floors"], step=1)
    with c4:
        grid = st.number_input("Structural Grid (m)", min_value=4.0, max_value=24.0, value=cfg["default_grid"], step=0.4)

    if st.button("Generate Design", use_container_width=True):
        coverage = {"Residential": 0.38, "Commercial": 0.50, "Industrial": 0.60}[family]
        gfa = site_area * coverage * floors
        cost = gfa * cfg["default_unit"]
        p = st.session_state.project
        p.update({"design_family": family, "typology": typology, "site_area": site_area, "floors": int(floors), "grid_spacing": grid, "total_gfa": gfa, "estimated_cost": cost, "design_status": "Concept Generated"})
        st.session_state.project = p

    p = st.session_state.project
    if p.get("design_family") == family:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Design Family", family)
        m2.metric("GFA", f"{p.get('total_gfa', 0):,.0f} m²")
        m3.metric("Indicative CAPEX", f"${p.get('estimated_cost', 0):,.0f}")
        m4.metric("Status", p.get("design_status", "Ready"))

        st.markdown("### 2D Concept Plan")
        width = max(24.0, min(72.0, math.sqrt(p.get("total_gfa", 1200) / max(int(floors), 1)) * 1.45))
        depth = max(18.0, min(60.0, (p.get("total_gfa", 1200) / max(int(floors), 1)) / width))
        st.plotly_chart(_plan(family, width, depth, grid, int(floors)), use_container_width=True)

        schedule = pd.DataFrame(cfg["program"], columns=["Program", "Share"])
        schedule["Area (m²)"] = schedule["Share"] * p.get("total_gfa", 0)
        st.markdown("### Program Schedule")
        st.dataframe(schedule, use_container_width=True, hide_index=True)
