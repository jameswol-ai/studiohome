"""Generative architecture and massing design module."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st


def render():
    st.markdown("## Generative Architecture & Massing Design")
    st.markdown("Procedurally optimize volumetric envelopes, facade configurations, and spatial program distributions for the active typology.")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    p = st.session_state.project

    col1, col2, col3 = st.columns(3)
    with col1:
        typology = st.selectbox(
            "Project Typology",
            [
                "Commercial Innovation Hub",
                "Mixed-Use Residential Tower",
                "Mass Timber Civic Center",
                "Biophilic Corporate Campus",
            ],
            index=0,
        )
        p["typology"] = typology
    with col2:
        floors = st.slider("Storey Count (Levels)", 1, 40, int(p.get("floors", 12)), step=1)
        p["floors"] = floors
    with col3:
        wwr = st.slider("Window-to-Wall Ratio (WWR %)", 20, 85, 55, step=5)
        p["wwr"] = wwr

    st.markdown("### Volumetric Envelope & Program Breakdown")
    site_area = float(p.get("site_area", 2500.0))
    building_height = floors * float(p.get("floor_to_floor", 3.5))
    footprint_area = site_area * 0.65
    total_gfa = footprint_area * floors
    p["total_gfa"] = total_gfa
    p["estimated_cost"] = total_gfa * float(p.get("unit_rate", 1650.0))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total GFA", f"{total_gfa:,.0f} m²", f"Footprint: {footprint_area:,.0f} m²")
    m2.metric("Building Height", f"{building_height:.1f} m", f"Floor-to-Floor: {p.get('floor_to_floor', 3.5):.1f} m")
    m3.metric("Floor Area Ratio (FAR)", f"{(total_gfa / site_area):.2f}", "Concept Review")
    m4.metric("Estimated CAPEX", f"${p['estimated_cost']:,.0f}", f"@ ${p.get('unit_rate', 1650):,.0f}/m²")

    st.markdown("### Generative 3D Building Envelope Model")
    width = np.sqrt(footprint_area)
    depth = footprint_area / width
    z_levels = np.linspace(0, building_height, floors + 1)

    fig = go.Figure()
    for i, z in enumerate(z_levels):
        fig.add_trace(
            go.Scatter3d(
                x=[-width / 2, width / 2, width / 2, -width / 2, -width / 2],
                y=[-depth / 2, -depth / 2, depth / 2, depth / 2, -depth / 2],
                z=[z, z, z, z, z],
                mode="lines",
                line=dict(color="#D40000" if i == len(z_levels) - 1 else "#000000", width=3),
                showlegend=False,
            )
        )

    fig.update_layout(
        title=f"3D Volumetric Massing Envelope | {typology}",
        scene=dict(
            xaxis_title="Width (m)",
            yaxis_title="Depth (m)",
            zaxis_title="Elevation (m)",
            bgcolor="#FFFFFF",
            xaxis=dict(backgroundcolor="#FFFFFF", gridcolor="#D8D8D8", color="#000000"),
            yaxis=dict(backgroundcolor="#FFFFFF", gridcolor="#D8D8D8", color="#000000"),
            zaxis=dict(backgroundcolor="#FFFFFF", gridcolor="#D8D8D8", color="#000000"),
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#000000"),
        height=450,
        margin=dict(t=45, b=10, l=10, r=10),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key="arch_3d_massing")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.project = p
