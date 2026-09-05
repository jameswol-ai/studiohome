"""Parametric floorplate and space-planning module."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from modules.design_state import build_design_state


def render():
    st.markdown("## Generative Floorplate & Space Planning Agent")
    st.markdown("Procedurally optimize internal zoning, core placement and circulation from the active parametric building geometry.")
    p = st.session_state.project
    state = build_design_state(p)
    p.update(state)
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            layout_style = st.selectbox("Workspace Layout Typology", ["Open-Plan Collaborative", "Cellular Executive Suites", "Mixed Hybrid Modular", "Activity-Based Working (ABW)"])
        with col2:
            core_position = st.selectbox("Vertical Core Placement", ["Central Core", "Perimeter Offset Core", "Twin Dual-Core Split"])
        with col3:
            atrium_void = st.checkbox("Include Biophilic Atrium Void", value=True)
        if st.button("Generate Procedural Floorplate Matrix", use_container_width=True):
            width, depth = state["floorplate_width"], state["floorplate_depth"]
            xs = np.linspace(0, width, state["grid_bays_x"] + 1)
            ys = np.linspace(0, depth, state["grid_bays_y"] + 1)
            zones = []
            for x in xs[:-1]:
                for y in ys[:-1]:
                    cx, cy = x + (xs[1] - xs[0]) / 2, y + (ys[1] - ys[0]) / 2
                    dist_center = np.hypot(cx - width / 2, cy - depth / 2)
                    if "Central" in core_position and dist_center < min(width, depth) * 0.18:
                        zone = "Vertical Core & Risers"
                    elif atrium_void and dist_center < min(width, depth) * 0.32:
                        zone = "Biophilic Atrium Void"
                    elif cx < width * 0.15 or cx > width * 0.85 or cy < depth * 0.15 or cy > depth * 0.85:
                        zone = "Perimeter Daylight Zone"
                    else:
                        zone = layout_style.split()[0] + " Work Zone"
                    zones.append({"X": round(cx, 2), "Y": round(cy, 2), "Zone": zone})
            df_floor = pd.DataFrame(zones)
            fig = px.scatter(df_floor, x="X", y="Y", color="Zone", title=f"Generated Floorplate Plan | {state['actual_grid_spacing_x']:.1f} x {state['actual_grid_spacing_y']:.1f} m Grid", template="plotly_white", height=400)
            fig.update_traces(marker=dict(size=18, symbol="square", line=dict(color="#000000", width=1)))
            fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10), legend=dict(font=dict(color="#000000")))
            st.plotly_chart(fig, use_container_width=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("Daylight Access Ratio", "88%", "Concept target")
            m2.metric("Circulation Efficiency", f"{(state['net_program_area'] / state['total_gfa']) * 100:.0f}%", "Program efficiency")
            m3.metric("Grid Bays", f"{state['grid_bays_x']} x {state['grid_bays_y']}")
        st.markdown("### Coordinated Geometry")
        st.dataframe(pd.DataFrame([
            ["Floorplate", state["floorplate_width"], state["floorplate_depth"], "m"],
            ["Footprint", state["footprint_area"], "", "m²"],
            ["Core", state["core_area"], "", "m²"],
            ["Circulation", state["circulation_area"], "", "m²"],
        ], columns=["Metric", "Width / Area", "Depth", "Unit"]), use_container_width=True, hide_index=True)
    st.session_state.project = p
