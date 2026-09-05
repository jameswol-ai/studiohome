"""Building envelope and façade performance module."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st


def render() -> None:
    """Render envelope performance studies."""
    st.markdown("## 🪟 Building Envelope & Façade Designer")
    st.caption("Coordinate WWR, glazing, shading, thermal performance, daylight intent, and façade embodied-carbon assumptions.")

    p = st.session_state.project
    c1, c2, c3 = st.columns(3)
    with c1:
        wwr = st.slider("Window-to-Wall Ratio (%)", 15, 80, int(p.get("wwr", 45)), 5)
        p["wwr"] = wwr
    with c2:
        u_value = st.slider("Glazing U-Value (W/m²K)", 0.6, 3.0, float(p.get("glazing_u", 1.2)), 0.1)
        p["glazing_u"] = u_value
    with c3:
        shading = st.slider("External Solar Shading (%)", 0, 80, int(p.get("shading", 35)), 5)
        p["shading"] = shading

    thermal_score = max(0.0, min(100.0, 100 - (u_value - 0.6) * 28 - max(0, wwr - 45) * 0.55 + shading * 0.22))
    solar_gain = max(5.0, 38 - shading * 0.35 + max(0, wwr - 40) * 0.45)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Envelope Performance", f"{thermal_score:.0f}/100")
    m2.metric("Indicative Solar Gain", f"{solar_gain:.1f} W/m²")
    m3.metric("WWR", f"{wwr}%")
    m4.metric("Glazing U-Value", f"{u_value:.1f} W/m²K")

    fig = go.Figure(go.Indicator(mode="gauge+number", value=thermal_score, title={"text": "Envelope Performance Index"}, gauge={"axis": {"range": [0, 100]}}))
    fig.update_layout(height=280, margin=dict(t=40, b=10, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧱 Façade Strategy")
    p["facade_strategy"] = st.selectbox("Primary Façade System", ["High-performance curtain wall", "Brick / masonry rainscreen", "Timber rainscreen", "Precast concrete panels", "Hybrid opaque + glazed façade"])
