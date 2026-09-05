"""Interactive architectural drawing, view and documentation studio.

The module is intentionally lightweight and dependency-friendly: Plotly is used
for 2D/3D presentation so the Streamlit deployment does not require a desktop CAD
runtime. Geometry is parametric and stored in project state for later BIM/export work.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


ELEMENTS = {
    "Walls": "walls",
    "Doors": "doors",
    "Windows": "windows",
    "Furniture": "furniture",
    "Toilets": "toilets",
    "Kitchens": "kitchens",
    "Stairs": "stairs",
    "Lifts": "lifts",
    "Columns": "columns",
    "Structural grid": "grid",
    "Dimensions": "dimensions",
    "Annotations": "annotations",
    "MEP fixtures": "mep",
}

VIEWS = [
    "Ground Floor Plan",
    "Typical Floor Plan",
    "Roof Plan",
    "Reflected Ceiling Plan",
    "Furniture Plan",
    "Fire & Life Safety Plan",
    "HVAC Coordination Plan",
    "Electrical Plan",
    "Plumbing Plan",
    "Section A-A",
    "Section B-B",
    "North Elevation",
    "South Elevation",
    "East Elevation",
    "West Elevation",
    "Wall Detail",
    "Door Detail",
    "Window Detail",
    "Stair Detail",
    "Toilet Detail",
]


def _dims() -> tuple[float, float]:
    p = st.session_state.project
    width = float(p.get("floorplate_width", 32.0))
    depth = float(p.get("floorplate_depth", 24.0))
    return max(width, 8.0), max(depth, 8.0)


def _add_rect(fig: go.Figure, x0: float, y0: float, x1: float, y1: float, name: str, width: int = 3) -> None:
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(width=width), fillcolor="rgba(80,120,180,0.06)")


def _add_line(fig: go.Figure, x0: float, y0: float, x1: float, y1: float, name: str, width: int = 2) -> None:
    fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(width=width))


def _plan_figure(width: float, depth: float, visible: set[str], title: str) -> go.Figure:
    fig = go.Figure()
    if "grid" in visible:
        spacing = float(st.session_state.project.get("grid_spacing", 8.0))
        for x in range(0, int(width) + 1, max(1, int(spacing))):
            _add_line(fig, x, 0, x, depth, "grid", 1)
        for y in range(0, int(depth) + 1, max(1, int(spacing))):
            _add_line(fig, 0, y, width, y, "grid", 1)

    if "walls" in visible:
        _add_rect(fig, 0, 0, width, depth, "walls", 5)
        _add_line(fig, width * 0.55, 0, width * 0.55, depth, "walls", 3)
        _add_line(fig, 0, depth * 0.55, width * 0.55, depth * 0.55, "walls", 3)

    if "doors" in visible:
        for x, y, dx, dy in [(width * .55, depth * .22, 2.0, 0), (width * .55, depth * .72, 2.0, 0), (width * .28, depth * .55, 0, 2.0)]:
            _add_line(fig, x, y, x + dx, y + dy, "doors", 5)
            fig.add_shape(type="arc", x0=x, y0=y, x1=x + (dx or 2), y1=y + (dy or 2), line=dict(width=1))

    if "windows" in visible:
        for x in [width * .15, width * .32, width * .70, width * .86]:
            _add_line(fig, x, 0, x + 2.0, 0, "windows", 7)
            _add_line(fig, x, depth, x + 2.0, depth, "windows", 7)
        for y in [depth * .20, depth * .40, depth * .65, depth * .82]:
            _add_line(fig, 0, y, 0, y + 1.5, "windows", 7)
            _add_line(fig, width, y, width, y + 1.5, "windows", 7)

    if "columns" in visible:
        xs = [float(st.session_state.project.get("grid_spacing", 8.0)) * i for i in range(1, max(1, int(width // float(st.session_state.project.get("grid_spacing", 8.0))))) if float(st.session_state.project.get("grid_spacing", 8.0)) * i < width]
        ys = [float(st.session_state.project.get("grid_spacing", 8.0)) * i for i in range(1, max(1, int(depth // float(st.session_state.project.get("grid_spacing", 8.0))))) if float(st.session_state.project.get("grid_spacing", 8.0)) * i < depth]
        for x in xs:
            for y in ys:
                fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=9, symbol="square"), name="Columns", showlegend=False))

    if "furniture" in visible:
        for x, y, w, h in [(4, 4, 5, 2), (13, 4, 5, 2), (4, 15, 4, 3), (13, 15, 4, 3), (23, 4, 6, 3)]:
            _add_rect(fig, x, y, min(x + w, width - 1), min(y + h, depth - 1), "furniture", 2)

    if "toilets" in visible:
        for x, y in [(width * .10, depth * .72), (width * .20, depth * .72), (width * .30, depth * .72)]:
            fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=13, symbol="circle-open"), name="Toilet", showlegend=False))
            fig.add_shape(type="rect", x0=x - .8, y0=y - .7, x1=x + .8, y1=y + .7, line=dict(width=1))

    if "kitchens" in visible:
        _add_rect(fig, width * .60, depth * .72, width * .92, depth * .88, "kitchens", 2)
        for x in [width * .66, width * .76, width * .86]:
            fig.add_trace(go.Scatter(x=[x], y=[depth * .80], mode="markers", marker=dict(size=8), showlegend=False))

    if "stairs" in visible:
        for i in range(8):
            _add_line(fig, width * .40, depth * .08 + i * .45, width * .52, depth * .08 + i * .45, "stairs", 1)

    if "lifts" in visible:
        _add_rect(fig, width * .72, depth * .40, width * .84, depth * .55, "lifts", 3)

    if "mep" in visible:
        for x, y in [(width * .65, depth * .22), (width * .75, depth * .22), (width * .85, depth * .22), (width * .65, depth * .62), (width * .75, depth * .62)]:
            fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=7, symbol="diamond"), name="MEP", showlegend=False))

    if "dimensions" in visible:
        fig.add_annotation(x=width / 2, y=-1.2, text=f"{width:.1f} m", showarrow=False)
        fig.add_annotation(x=-1.4, y=depth / 2, text=f"{depth:.1f} m", textangle=-90, showarrow=False)

    if "annotations" in visible:
        fig.add_annotation(x=width * .28, y=depth * .25, text="OPEN OFFICE", showarrow=False)
        fig.add_annotation(x=width * .78, y=depth * .48, text="CORE", showarrow=False)

    fig.update_layout(title=title, template="plotly_dark", height=650, margin=dict(l=30, r=20, t=55, b=30), showlegend=False)
    fig.update_xaxes(range=[-3, width + 3], scaleanchor="y", scaleratio=1, title="m")
    fig.update_yaxes(range=[-3, depth + 3], title="m")
    return fig


def _elevation_figure(width: float, height: float, title: str) -> go.Figure:
    fig = go.Figure()
    _add_rect(fig, 0, 0, width, height, "building", 4)
    levels = int(st.session_state.project.get("floors", 12))
    for i in range(1, levels):
        y = i * height / levels
        _add_line(fig, 0, y, width, y, "floor", 1)
    for level in range(levels):
        y0 = level * height / levels + .7
        y1 = min(y0 + height / levels * .45, height - .2)
        for x in [2, 6, 10, 14, 18, 22, 26, 30]:
            if x < width:
                _add_rect(fig, x, y0, min(x + 2.5, width - .5), y1, "window", 1)
    fig.update_layout(title=title, template="plotly_dark", height=600, margin=dict(l=30, r=20, t=55, b=30), showlegend=False)
    fig.update_xaxes(range=[-2, width + 2], title="m")
    fig.update_yaxes(range=[0, height + 2], title="m")
    return fig


def _section_figure(width: float, height: float, title: str) -> go.Figure:
    fig = _elevation_figure(width, height, title)
    levels = int(st.session_state.project.get("floors", 12))
    floor_h = height / levels
    for i in range(levels):
        y = i * floor_h
        fig.add_shape(type="rect", x0=width * .38, y0=y + .2, x1=width * .62, y1=y + floor_h - .2, line=dict(width=1))
    fig.add_shape(type="line", x0=width * .45, y0=0, x1=width * .45, y1=height, line=dict(width=3))
    fig.add_shape(type="line", x0=width * .55, y0=0, x1=width * .55, y1=height, line=dict(width=3))
    return fig


def _detail_figure(kind: str) -> go.Figure:
    fig = go.Figure()
    if kind == "Door Detail":
        _add_rect(fig, 0, 0, 1.0, 2.1, "door", 5)
        _add_line(fig, 0, 0, 1.0, 0, "threshold", 3)
    elif kind == "Window Detail":
        _add_rect(fig, 0, 0, 2.0, 1.5, "window", 5)
        _add_line(fig, 1, 0, 1, 1.5, "mullion", 2)
    elif kind == "Stair Detail":
        for i in range(8):
            _add_line(fig, i * .35, i * .22, (i + 1) * .35, i * .22, "tread", 3)
    elif kind == "Toilet Detail":
        fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=70, symbol="circle-open"), showlegend=False))
        _add_rect(fig, -1.2, -1.0, 1.2, 1.0, "room", 3)
    else:
        _add_rect(fig, 0, 0, 3, 2, "detail", 5)
        _add_line(fig, 0, .5, 3, .5, "datum", 2)
    fig.update_layout(title=kind, template="plotly_dark", height=600, margin=dict(l=30, r=20, t=55, b=30), showlegend=False)
    fig.update_xaxes(scaleanchor="y", scaleratio=1)
    return fig


def render() -> None:
    st.markdown("## 📐 Drawing Studio | Plans • Sections • Elevations • Details")
    st.caption("Parametric architectural documentation workspace with coordinated 2D/3D presentation and building elements.")

    project = st.session_state.project
    width, depth = _dims()
    height = float(project.get("floor_to_floor", 3.5)) * int(project.get("floors", 12))

    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        width = c1.number_input("Floorplate width (m)", 8.0, 200.0, width, 1.0, key="draw_width")
        depth = c2.number_input("Floorplate depth (m)", 8.0, 200.0, depth, 1.0, key="draw_depth")
        mode = c3.selectbox("View mode", ["2D Documentation", "3D Model", "Presentation"])
        view = c4.selectbox("Drawing view", VIEWS)
        project["floorplate_width"] = width
        project["floorplate_depth"] = depth

    if mode == "2D Documentation":
        if view in ("Section A-A", "Section B-B"):
            fig = _section_figure(width, height, view)
        elif "Elevation" in view:
            fig = _elevation_figure(width, height, view)
        elif "Detail" in view:
            fig = _detail_figure(view)
        else:
            selected = st.multiselect("Visible elements", list(ELEMENTS.keys()), default=list(ELEMENTS.keys()), key="drawing_layers")
            visible = {ELEMENTS[e] for e in selected}
            fig = _plan_figure(width, depth, visible, view)
        st.plotly_chart(fig, use_container_width=True)

    elif mode == "3D Model":
        fig = go.Figure()
        floors = int(project.get("floors", 12))
        f2f = float(project.get("floor_to_floor", 3.5))
        for level in range(floors):
            z = level * f2f
            x = [0, width, width, 0, 0, width, width, 0]
            y = [0, 0, depth, depth, 0, 0, depth, depth]
            zc = [z, z, z, z, z + f2f, z + f2f, z + f2f, z + f2f]
            faces = [(0,1,2),(0,2,3),(4,6,5),(4,7,6),(0,4,5),(0,5,1),(1,5,6),(1,6,2),(2,6,7),(2,7,3),(3,7,4),(3,4,0)]
            i, j, k = zip(*faces)
            fig.add_trace(go.Mesh3d(x=x, y=y, z=zc, i=i, j=j, k=k, opacity=.16, name=f"Level {level+1}", showlegend=False))
        fig.update_layout(title=f"3D Building Mass | {floors} Levels", template="plotly_dark", height=700, scene=dict(aspectmode="data", xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Z (m)"))
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Presentation mode combines the active drawing with a simplified coordination dashboard. Use 2D Documentation for production-style layers and 3D Model for massing review.")
        st.plotly_chart(_plan_figure(width, depth, set(ELEMENTS.values()), "Presentation Floor Plan"), use_container_width=True)

    st.markdown("### 🧱 Building Element Schedule")
    schedule = pd.DataFrame([
        ["Walls", "A-WALL", "Partition / external", "Parametric"],
        ["Doors", "A-DOOR", "Single / double / fire", "Parametric"],
        ["Windows", "A-WIND", "Glazing / opening", "Parametric"],
        ["Furniture", "A-FURN", "Loose / fixed furniture", "Indicative"],
        ["Toilets", "P-FIXT", "WC / basin / shower", "MEP coordinated"],
        ["Stairs", "A-STAIR", "Flight / landing / rail", "Parametric"],
        ["Lifts", "A-LIFT", "Lift shaft / core", "Coordinated"],
        ["Columns", "S-COL", "Structural grid", "Structural"],
        ["MEP fixtures", "MEP-FIXT", "HVAC / electrical / plumbing", "Coordination"],
    ], columns=["Element", "Tag", "Description", "Status"])
    st.dataframe(schedule, use_container_width=True, hide_index=True)

    st.markdown("### 📋 Drawing Set")
    set_df = pd.DataFrame({"Sheet": ["A-001", "A-101", "A-102", "A-201", "A-301", "A-401", "A-501"], "Content": ["Cover / general notes", "Ground floor plan", "Typical / roof plans", "Elevations", "Sections", "Enlarged plans / details", "Door / window / toilet / stair details"], "Status": ["Live", "Live", "Live", "Live", "Live", "Live", "Live"]})
    st.dataframe(set_df, use_container_width=True, hide_index=True)

    st.success("Drawing Studio is coordinated from the project state. The geometry is intentionally a parametric design-review layer, ready to become a deeper BIM/IFC authoring pipeline.")
