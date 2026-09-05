"""Interactive BIM-style 3D parametric building design studio."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.design_state import build_design_state, get_program_schedule

BLACK = "#111111"
RED = "#D40000"
GREY = "#777777"
LIGHT = "#CCCCCC"


def _mesh(fig, x, y, z, faces, *, name, color=GREY, opacity=0.25):
    i, j, k = zip(*faces)
    fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color=color, opacity=opacity, flatshading=True, hovertext=name, hoverinfo="text", showlegend=False))


def _box(fig, x0, y0, z0, x1, y1, z1, *, name, color=GREY, opacity=0.25):
    x = [x0, x1, x1, x0, x0, x1, x1, x0]
    y = [y0, y0, y1, y1, y0, y0, y1, y1]
    z = [z0, z0, z0, z0, z1, z1, z1, z1]
    faces = [(0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6), (0, 4, 5), (0, 5, 1), (1, 5, 6), (1, 6, 2), (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0)]
    _mesh(fig, x, y, z, faces, name=name, color=color, opacity=opacity)


def _line(fig, xs, ys, zs, *, color=BLACK, width=3):
    fig.add_trace(go.Scatter3d(x=list(xs), y=list(ys), z=list(zs), mode="lines", line=dict(color=color, width=width), hoverinfo="skip", showlegend=False))


def _structural_grid(fig, state, z):
    w, d = state["floorplate_width"], state["floorplate_depth"]
    for i in range(state["grid_bays_x"] + 1):
        x = min(w, i * state["actual_grid_spacing_x"])
        _line(fig, [x, x], [0, d], [z, z], color=GREY, width=1)
    for i in range(state["grid_bays_y"] + 1):
        y = min(d, i * state["actual_grid_spacing_y"])
        _line(fig, [0, w], [y, y], [z, z], color=GREY, width=1)


def _columns(fig, state, z0, z1):
    w, d = state["floorplate_width"], state["floorplate_depth"]
    for i in range(state["grid_bays_x"] + 1):
        x = min(w, i * state["actual_grid_spacing_x"])
        for j in range(state["grid_bays_y"] + 1):
            y = min(d, j * state["actual_grid_spacing_y"])
            _line(fig, [x, x], [y, y], [z0, z1], color=BLACK, width=2)


def _core(fig, state, height, gap):
    w, d = state["floorplate_width"], state["floorplate_depth"]
    cw, cd = w * 0.22, d * 0.32
    cx, cy = (w - cw) / 2, (d - cd) / 2
    _box(fig, cx, cy, 0, cx + cw, cy + cd, height + state["floors"] * gap, name="Vertical Core", color=RED, opacity=0.42)


def _program_zones(fig, state, gap, selected_level, show_labels):
    """Create deterministic program zones from the shared program schedule."""
    w, d = state["floorplate_width"], state["floorplate_depth"]
    f2f = state["floor_to_floor"]
    core_w, core_d = w * 0.22, d * 0.32
    cx, cy = (w - core_w) / 2, (d - core_d) / 2
    left_w = max(1.0, cx)
    right_w = max(1.0, w - (cx + core_w))
    schedule = get_program_schedule(state)
    levels = range(state["floors"]) if selected_level == "All Levels" else [int(selected_level.split()[-1]) - 1]
    palette = ["#DDDDDD", "#EEEEEE", "#BBBBBB", "#999999", "#777777", "#CCCCCC"]
    for level in levels:
        z0 = level * (f2f + gap) + 0.22
        z1 = z0 + f2f - 0.35
        usable_w = left_w + right_w
        cursor = 0.0
        for index, (name, share, area) in enumerate(schedule):
            zone_w = max(0.9, usable_w * float(share))
            if cursor + zone_w > usable_w:
                zone_w = usable_w - cursor
            if zone_w <= 0:
                continue
            x0 = cursor if cursor < left_w else cursor + core_w
            x1 = min(w, x0 + zone_w)
            if x1 <= x0:
                continue
            _box(fig, x0, 0.7, z0, x1, d - 0.7, z1, name=f"{name} | Level {level + 1}", color=palette[index % len(palette)], opacity=0.18)
            if show_labels:
                fig.add_trace(go.Scatter3d(x=[(x0 + x1) / 2], y=[d / 2], z=[(z0 + z1) / 2], mode="text", text=[name], textfont=dict(color=BLACK, size=9), hovertext=f"{name}: {area:,.0f} m²", hoverinfo="text", showlegend=False))
            cursor += zone_w
            if cursor >= left_w and cursor < left_w + right_w:
                cursor += core_w


def _slabs(fig, state, gap, selected_level):
    w, d = state["floorplate_width"], state["floorplate_depth"]
    f2f = state["floor_to_floor"]
    levels = range(state["floors"]) if selected_level == "All Levels" else [max(1, int(selected_level.split()[-1])) - 1]
    for level in levels:
        z = level * (f2f + gap)
        _box(fig, 0, 0, z, w, d, z + 0.16, name=f"Slab Level {level + 1}", color=BLACK, opacity=0.30)


def _facade(fig, state, opacity, gap):
    w, d, h = state["floorplate_width"], state["floorplate_depth"], state["building_height"] + state["floors"] * gap
    _box(fig, 0, 0, 0, w, d, h, name="Building Envelope", color=LIGHT, opacity=opacity)
    wwr = state["window_wall_ratio"]
    band = max(0.4, min(1.4, wwr * 2.0))
    for level in range(state["floors"]):
        z = level * (state["floor_to_floor"] + gap) + state["floor_to_floor"] * 0.35
        for x in [w * 0.15, w * 0.35, w * 0.55, w * 0.75]:
            _line(fig, [x, min(w, x + band)], [0, 0], [z, z], color=RED, width=4)
            _line(fig, [x, min(w, x + band)], [d, d], [z, z], color=RED, width=4)


def _mep(fig, state, gap):
    w, d = state["floorplate_width"], state["floorplate_depth"]
    for level in range(state["floors"]):
        z = level * (state["floor_to_floor"] + gap) + state["floor_to_floor"] * 0.72
        _line(fig, [w * 0.20, w * 0.80], [d * 0.50, d * 0.50], [z, z], color=RED, width=5)
        _line(fig, [w * 0.50, w * 0.50], [d * 0.20, d * 0.80], [z, z], color=RED, width=4)


def _stairs(fig, state, gap):
    w, d = state["floorplate_width"], state["floorplate_depth"]
    f2f = state["floor_to_floor"]
    x0, y0 = w * 0.10, d * 0.12
    for level in range(state["floors"] - 1):
        z0 = level * (f2f + gap)
        for step in range(8):
            z = z0 + f2f * (step + 1) / 9
            _line(fig, [x0, x0 + w * 0.12], [y0 + step * 0.15, y0 + step * 0.15], [z, z], color=BLACK, width=2)


def _doors_windows(fig, state, gap):
    w, d = state["floorplate_width"], state["floorplate_depth"]
    f2f = state["floor_to_floor"]
    for level in range(state["floors"]):
        z = level * (f2f + gap) + f2f * 0.45
        for x in [w * 0.30, w * 0.50, w * 0.70]:
            _line(fig, [x, x + min(1.0, w * 0.025)], [0, 0], [z, z], color=BLACK, width=7)
        for y in [d * 0.20, d * 0.50, d * 0.80]:
            _line(fig, [0, 0], [y, y + min(1.0, d * 0.05)], [z, z], color=RED, width=5)


def _figure(state, *, show_facade, show_structure, show_grid, show_core, show_slabs, show_mep, show_stairs, show_openings, show_program, show_labels, opacity, explode, selected_level):
    fig = go.Figure()
    gap = explode * state["floor_to_floor"]
    if show_program:
        _program_zones(fig, state, gap, selected_level, show_labels)
    if show_facade:
        _facade(fig, state, opacity, gap)
    if show_slabs:
        _slabs(fig, state, gap, selected_level)
    if show_grid:
        for level in range(state["floors"]):
            _structural_grid(fig, state, level * (state["floor_to_floor"] + gap))
    if show_structure:
        for level in range(state["floors"]):
            z0 = level * (state["floor_to_floor"] + gap)
            _columns(fig, state, z0, z0 + state["floor_to_floor"])
    if show_core:
        _core(fig, state, state["building_height"], gap)
    if show_mep:
        _mep(fig, state, gap)
    if show_stairs:
        _stairs(fig, state, gap)
    if show_openings:
        _doors_windows(fig, state, gap)
    fig.update_layout(title=f"3D BIM Design Model | {state['typology']} | {state['floors']} Storeys", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color=BLACK), height=800, margin=dict(l=0, r=0, t=55, b=0), showlegend=False, scene=dict(bgcolor="#FFFFFF", aspectmode="data", xaxis=dict(title="Width (m)", color=BLACK, gridcolor="#DDDDDD"), yaxis=dict(title="Depth (m)", color=BLACK, gridcolor="#DDDDDD"), zaxis=dict(title="Elevation (m)", color=BLACK, gridcolor="#DDDDDD")))
    return fig


def render():
    st.markdown("## 3D Design Studio")
    st.markdown("Program-driven BIM-style coordination viewer for architecture, structure and building systems.")
    project = st.session_state.project
    state = build_design_state(project)
    project.update(state)

    st.markdown("### Discipline and BIM Visibility")
    c1, c2, c3, c4 = st.columns(4)
    show_facade = c1.checkbox("Architecture / Facade", True)
    show_structure = c2.checkbox("Structure / Columns", True)
    show_core = c3.checkbox("Core", True)
    show_slabs = c4.checkbox("Slabs", True)
    c5, c6, c7, c8 = st.columns(4)
    show_mep = c5.checkbox("MEP Routes", True)
    show_stairs = c6.checkbox("Stairs", True)
    show_openings = c7.checkbox("Doors / Windows", True)
    show_grid = c8.checkbox("Structural Grid", True)
    c9, c10 = st.columns(2)
    show_program = c9.checkbox("Program Zones", True)
    show_labels = c10.checkbox("Room / Zone Labels", True)

    c1, c2, c3 = st.columns(3)
    opacity = c1.slider("Envelope Transparency", 0.05, 0.70, 0.20, 0.02)
    explode = c2.slider("Level Separation", 0.0, 0.50, 0.0, 0.02)
    levels = ["All Levels"] + [f"Level {i}" for i in range(1, state["floors"] + 1)]
    selected_level = c3.selectbox("Level Focus", levels)

    camera_name = st.selectbox("Camera", ["Isometric", "Top", "Front", "Side"])
    cameras = {"Isometric": dict(eye=dict(x=1.55, y=1.55, z=1.25)), "Top": dict(eye=dict(x=0.01, y=0.01, z=2.6)), "Front": dict(eye=dict(x=0.01, y=2.8, z=1.0)), "Side": dict(eye=dict(x=2.8, y=0.01, z=1.0))}
    fig = _figure(state, show_facade=show_facade, show_structure=show_structure, show_grid=show_grid, show_core=show_core, show_slabs=show_slabs, show_mep=show_mep, show_stairs=show_stairs, show_openings=show_openings, show_program=show_program, show_labels=show_labels, opacity=opacity, explode=explode, selected_level=selected_level)
    fig.update_layout(scene_camera=cameras[camera_name])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "scrollZoom": True})

    schedule = get_program_schedule(state)
    schedule_df = pd.DataFrame([[name, share * 100, area] for name, share, area in schedule], columns=["Program Zone", "Share (%)", "Area (m²)"])
    st.markdown("### Program-Driven BIM Schedule")
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)

    st.markdown("### Coordinated Model Quantities")
    quantities = [["Floorplate", f"{state['floorplate_width']:.1f} x {state['floorplate_depth']:.1f} m"], ["Building height", f"{state['building_height']:.1f} m"], ["Storeys", state["floors"]], ["GFA", f"{state['total_gfa']:,.0f} m²"], ["Footprint", f"{state['footprint_area']:,.0f} m²"], ["Structural grid", f"{state['grid_bays_x']} x {state['grid_bays_y']} bays"], ["Core area", f"{state['core_area']:,.0f} m²"], ["Envelope area", f"{state['envelope_area']:,.0f} m²"]]
    st.dataframe(pd.DataFrame(quantities, columns=["Parameter", "Value"]), use_container_width=True, hide_index=True)
    st.success("3D model synchronized with the shared parametric project state.")
    st.caption("Conceptual coordination representation. Discipline-specific engineering calculations remain subject to detailed analysis and code verification.")
    st.session_state.project = project
