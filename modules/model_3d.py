"""Interactive 3D parametric building design studio."""
from __future__ import annotations

import math

import plotly.graph_objects as go
import streamlit as st

from modules.design_state import build_design_state

BLACK = "#111111"
RED = "#D40000"
GREY = "#777777"


def _cuboid(fig: go.Figure, x0: float, y0: float, z0: float, x1: float, y1: float, z1: float, *, name: str, opacity: float = 0.28, color: str = BLACK) -> None:
    x = [x0, x1, x1, x0, x0, x1, x1, x0]
    y = [y0, y0, y1, y1, y0, y0, y1, y1]
    z = [z0, z0, z0, z0, z1, z1, z1, z1]
    faces = [(0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6), (0, 4, 5), (0, 5, 1), (1, 5, 6), (1, 6, 2), (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0)]
    i, j, k = zip(*faces)
    fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color=color, opacity=opacity, name=name, flatshading=True, hovertext=name, hoverinfo="text", showlegend=False))


def _line(fig: go.Figure, xs, ys, zs, *, color=BLACK, width=3, name="") -> None:
    fig.add_trace(go.Scatter3d(x=list(xs), y=list(ys), z=list(zs), mode="lines", line=dict(color=color, width=width), name=name, hoverinfo="skip", showlegend=False))


def _building_figure(state: dict, show_grid: bool, show_structure: bool, show_core: bool, show_floorplates: bool, facade_opacity: float, explode: float) -> go.Figure:
    width = state["floorplate_width"]
    depth = state["floorplate_depth"]
    floors = state["floors"]
    f2f = state["floor_to_floor"]
    height = state["building_height"]
    gap = explode * f2f
    fig = go.Figure()

    for level in range(floors):
        z0 = level * (f2f + gap)
        z1 = z0 + f2f
        _cuboid(fig, 0, 0, z0, width, depth, z1, name=f"Level {level + 1}", opacity=facade_opacity, color=GREY)
        if show_floorplates:
            _line(fig, [0, width, width, 0, 0], [0, 0, depth, depth, 0], [z0, z0, z0, z0, z0], color=BLACK, width=2)
        if show_grid:
            for i in range(1, state["grid_bays_x"]):
                x = i * state["actual_grid_spacing_x"]
                _line(fig, [x, x], [0, depth], [z0, z0], color=GREY, width=1)
            for i in range(1, state["grid_bays_y"]):
                y = i * state["actual_grid_spacing_y"]
                _line(fig, [0, width], [y, y], [z0, z0], color=GREY, width=1)
        if show_structure:
            for i in range(state["grid_bays_x"] + 1):
                x = min(width, i * state["actual_grid_spacing_x"])
                for j in range(state["grid_bays_y"] + 1):
                    y = min(depth, j * state["actual_grid_spacing_y"])
                    _line(fig, [x, x], [y, y], [z0, z1], color=BLACK, width=2)

    if show_core:
        core_w = width * 0.22
        core_d = depth * 0.32
        cx = (width - core_w) / 2
        cy = (depth - core_d) / 2
        _cuboid(fig, cx, cy, 0, cx + core_w, cy + core_d, height + floors * gap, name="Vertical Core", opacity=0.42, color=RED)

    fig.update_layout(
        title=f"3D Parametric Building Model | {state['design_family']} | {floors} Storeys",
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color=BLACK), height=760,
        margin=dict(l=0, r=0, t=55, b=0), showlegend=False,
        scene=dict(
            bgcolor="#FFFFFF", aspectmode="data",
            xaxis=dict(title="Width (m)", backgroundcolor="#FFFFFF", gridcolor="#DDDDDD", color=BLACK),
            yaxis=dict(title="Depth (m)", backgroundcolor="#FFFFFF", gridcolor="#DDDDDD", color=BLACK),
            zaxis=dict(title="Height (m)", backgroundcolor="#FFFFFF", gridcolor="#DDDDDD", color=BLACK),
            camera=dict(eye=dict(x=1.55, y=1.55, z=1.25)),
        ),
    )
    return fig


def render():
    st.markdown("## 3D Design Studio")
    st.markdown("Interactive parametric building model synchronized with the master design state.")
    project = st.session_state.project
    state = build_design_state(project)
    project.update(state)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        facade_opacity = st.slider("Facade Transparency", 0.08, 0.65, 0.24, 0.02)
    with c2:
        explode = st.slider("Floor Explode", 0.0, 0.50, 0.0, 0.02)
    with c3:
        show_grid = st.checkbox("Show Structural Grid", value=True)
    with c4:
        show_structure = st.checkbox("Show Structure", value=True)

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        show_core = st.checkbox("Show Core", value=True)
    with c6:
        show_floorplates = st.checkbox("Show Floorplates", value=True)
    with c7:
        view = st.selectbox("Camera", ["Isometric", "Top", "Front", "Side"])
    with c8:
        if st.button("Sync 3D Model", use_container_width=True):
            state = build_design_state(project)
            project.update(state)
            st.session_state.project = project
            st.rerun()

    if view == "Top": camera = dict(eye=dict(x=0.01, y=0.01, z=2.4))
    elif view == "Front": camera = dict(eye=dict(x=0.01, y=2.8, z=1.0))
    elif view == "Side": camera = dict(eye=dict(x=2.8, y=0.01, z=1.0))
    else: camera = dict(eye=dict(x=1.55, y=1.55, z=1.25))

    fig = _building_figure(state, show_grid, show_structure, show_core, show_floorplates, facade_opacity, explode)
    fig.update_layout(scene_camera=camera)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "scrollZoom": True})

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Width", f"{state['floorplate_width']:.1f} m")
    m2.metric("Depth", f"{state['floorplate_depth']:.1f} m")
    m3.metric("Height", f"{state['building_height']:.1f} m")
    m4.metric("GFA", f"{state['total_gfa']:,.0f} m²")
    m5.metric("Grid", f"{state['grid_bays_x']} x {state['grid_bays_y']}")
    m6.metric("FAR", f"{state['far']:.2f}")

    st.markdown("### 3D Coordination Data")
    st.dataframe(
        __import__("pandas").DataFrame([
            ["Building family", state["design_family"]], ["Typology", state["typology"]], ["Storeys", state["floors"]],
            ["Floor-to-floor", f"{state['floor_to_floor']:.2f} m"], ["Footprint", f"{state['footprint_area']:,.1f} m²"],
            ["Core area", f"{state['core_area']:,.1f} m²"], ["Envelope", f"{state['envelope_area']:,.1f} m²"],
        ], columns=["Parameter", "Coordinated Value"]), use_container_width=True, hide_index=True
    )
    st.session_state.project = project
