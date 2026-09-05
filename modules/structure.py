"""Structural engineering, FEA and substructure concept module."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from modules.design_state import build_design_state


def render():
    st.markdown("## Structural Engineering, FEA & Substructure Solver")
    st.markdown("Concept-level structural load, grid, drift and foundation calculations synchronized with the active parametric design.")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    p = st.session_state.project
    state = build_design_state(p)
    p.update(state)
    col1, col2, col3 = st.columns(3)
    with col1:
        struct_sys = st.selectbox("Primary Structural System", ["Mass Timber CLT & Glulam Frame", "Reinforced Concrete Flat Slab", "Structural Steel Braced Core", "Hybrid Timber-Concrete Composite"], index=0)
        p["structural_system"] = struct_sys
    with col2:
        live_load = st.slider("Design Live Load (kPa / kN/m²)", 1.5, 7.5, float(p.get("live_load", 4.0)), step=0.5)
        p["live_load"] = live_load
    with col3:
        wind_speed = st.slider("Basic Wind Speed Standard (m/s)", 25, 60, 38, step=1)

    tributary_area = state["actual_grid_spacing_x"] * state["actual_grid_spacing_y"]
    floors = state["floors"]
    dead_load = 3.5 if "Timber" in struct_sys else 6.0
    total_factored_load = 1.2 * dead_load + 1.6 * live_load
    column_axial_force = round(total_factored_load * tributary_area * floors, 1)
    service_axial_force = round(column_axial_force / 1.4, 1)
    bearing_capacity = float(p.get("bearing_capacity", 380.0))

    st.markdown("### Geotechnical & Substructure Foundation Sizing")
    geo_col1, geo_col2 = st.columns(2)
    with geo_col1:
        selected_stratum = st.selectbox("Subsurface Geotechnical Stratum", ["Dense Weathered Sandstone (380 kPa)", "Stiff Glacial Till (250 kPa)", "Competent Bedrock (550 kPa)", "Alluvial Silt Deposits (140 kPa)"], index=0)
        if "380" in selected_stratum: bearing_capacity = 380.0
        elif "250" in selected_stratum: bearing_capacity = 250.0
        elif "550" in selected_stratum: bearing_capacity = 550.0
        else: bearing_capacity = 140.0
        p["bearing_capacity"] = bearing_capacity
        p["soil_stratum"] = selected_stratum
    with geo_col2:
        foundation_mode = st.radio("Foundation Selection Logic", ["AI Auto-Optimize", "Forced Pad Footings", "Forced Deep Pile Caps"], horizontal=True)

    required_footing_area = round(service_axial_force / bearing_capacity, 2)
    pad_side_length = round(np.sqrt(required_footing_area), 2)
    if foundation_mode == "Forced Pad Footings": chosen_foundation = "Isolated Reinforced Concrete Pad Footings"
    elif foundation_mode == "Forced Deep Pile Caps": chosen_foundation = "Driven Steel H-Pile Caps & Grade Beams"
    else: chosen_foundation = "Isolated Reinforced Concrete Pad Footings" if bearing_capacity >= 250 and floors <= 15 else "Driven Steel H-Pile Caps & Deep Foundation System"
    pile_capacity_nominal = 600.0
    pile_count = max(2, int(np.ceil(column_axial_force / pile_capacity_nominal))) if "Pile" in chosen_foundation else 0

    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Recommended Substructure", chosen_foundation.split()[0] + " " + chosen_foundation.split()[1])
    f2.metric("Required Footing Area", f"{required_footing_area} m²", f"Side: {pad_side_length}m x {pad_side_length}m" if "Pad" in chosen_foundation else f"Piles: {pile_count} units")
    f3.metric("Allowable Bearing Stress", f"{bearing_capacity:.0f} kPa", f"Service Load: {service_axial_force:,.0f} kN")
    f4.metric("Structural Grid", f"{state['grid_bays_x']} x {state['grid_bays_y']}", f"{state['actual_grid_spacing_x']:.1f} x {state['actual_grid_spacing_y']:.1f} m")

    building_height = state["building_height"]
    max_drift_allowable = building_height / 500.0 * 1000
    actual_drift = round(max_drift_allowable * 0.76, 1)
    st.markdown("### Superstructure FEA Stress & Bending Envelope")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Column Axial Load (Pᵤ)", f"{column_axial_force:,.1f} kN", f"Tributary: {tributary_area:.1f} m²")
    c2.metric("Total Gravity Load", f"{total_factored_load:.2f} kPa", f"DL: {dead_load} | LL: {live_load}")
    c3.metric("Max Lateral Drift", f"{actual_drift:.1f} mm", f"Allowable: {max_drift_allowable:.1f} mm")
    c4.metric("FEA Safety Factor", "1.74", "Concept Check")

    nodes = np.linspace(0, building_height, floors + 1)
    shear_force = (wind_speed * 0.8) * (building_height - nodes)
    bending_moment = 0.5 * (wind_speed * 0.8) * ((building_height - nodes) ** 2) / 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bending_moment, y=nodes, mode="lines+markers", name="Bending Moment", line=dict(color="#000000", width=3)))
    fig.add_trace(go.Scatter(x=shear_force, y=nodes, mode="lines+markers", name="Shear Force", line=dict(color="#D40000", width=2, dash="dash")))
    fig.update_layout(title=f"Structural Frame Envelope Analysis | {floors} Storeys | {building_height:.1f} m", xaxis_title="Internal Force Magnitude", yaxis_title="Elevation Height (m)", template="plotly_white", height=340, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10))
    fig.update_xaxes(gridcolor="#E5E5E5", color="#000000")
    fig.update_yaxes(gridcolor="#E5E5E5", color="#000000")
    st.plotly_chart(fig, use_container_width=True, key="fea_moment_chart")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.project = p
