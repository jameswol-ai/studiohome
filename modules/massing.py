"""Deterministic massing and volumetric coordination module."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.design_state import build_design_state


def render():
    st.markdown("## Massing & Volumetrics AI Agent")
    st.markdown("Generate deterministic building volumes synchronized with the master floorplate, storey count, height and GFA.")
    p = st.session_state.project
    state = build_design_state(p)
    p.update(state)
    col1, col2, col3 = st.columns(3)
    with col1:
        num_blocks = st.slider("Active Volumetric Blocks", 1, 6, 1)
    with col2:
        max_height = st.slider("Max Building Height Limit (m)", 6, 240, max(24, int(state["building_height"])), step=6)
    with col3:
        target_far = st.slider("Target Floor Area Ratio (FAR)", 0.5, 12.0, float(min(12, max(0.5, state["far"]))), step=0.5)
    if st.button("Generate & Sync Massing Envelopes", use_container_width=True):
        block_count = max(1, int(num_blocks))
        base_width = state["floorplate_width"]
        base_depth = state["floorplate_depth"]
        total_gfa = state["total_gfa"]
        rows = []
        remaining_gfa = total_gfa
        for i in range(block_count):
            share = 1.0 / block_count
            if i == block_count - 1:
                gfa = remaining_gfa
            else:
                gfa = total_gfa * share
                remaining_gfa -= gfa
            levels = max(1, round(state["floors"] / block_count)) if block_count > 1 else state["floors"]
            levels = min(levels, max(1, int(max_height / state["floor_to_floor"])))
            footprint = gfa / max(levels, 1)
            aspect = base_width / max(base_depth, 1.0)
            width = (footprint * aspect) ** 0.5
            depth = footprint / max(width, 1.0)
            height = levels * state["floor_to_floor"]
            rows.append({"Block ID": f"Volumetric Block {chr(65 + i)}", "Footprint Area (m²)": round(footprint, 1), "Width (m)": round(width, 1), "Depth (m)": round(depth, 1), "Height (m)": round(height, 1), "Levels": levels, "Gross Floor Area (m²)": round(gfa, 1), "Primary Program": state["typology"]})
        df_mass = pd.DataFrame(rows)
        p["massing_blocks"] = rows
        p["massing_gfa"] = float(df_mass["Gross Floor Area (m²)"].sum())
        p["target_far"] = target_far
        p["massing_height"] = float(df_mass["Height (m)"].max())
        st.session_state.project = p
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Coordinated GFA", f"{p['massing_gfa']:,.0f} m²")
        m2.metric("Achieved FAR", f"{p['massing_gfa'] / state['site_area']:.2f}", f"Target {target_far:.2f}")
        m3.metric("Building Height", f"{p['massing_height']:.1f} m")
        m4.metric("Grid", f"{state['grid_bays_x']} x {state['grid_bays_y']}")
        st.dataframe(df_mass, use_container_width=True, hide_index=True)
        fig = px.bar(df_mass, x="Block ID", y="Height (m)", title="Coordinated Volumetric Height Distribution", template="plotly_white", height=320)
        fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10), showlegend=False)
        fig.update_traces(marker_color="#D40000")
        st.plotly_chart(fig, use_container_width=True)
    st.session_state.project = p
