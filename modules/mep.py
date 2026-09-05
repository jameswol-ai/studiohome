"""Mechanical and building energy performance concept module."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render():
    st.markdown("## MEP & Building Energy Performance")
    st.markdown("Simulate HVAC loads, energy use intensity, renewable generation potential, and building energy performance for the active project.")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    p = st.session_state.project
    total_gfa = float(p.get("total_gfa", 0.0))

    col1, col2, col3 = st.columns(3)
    with col1:
        hvac_system = st.selectbox("HVAC Distribution System", ["VRF with Heat Recovery", "Chilled Beam & DOAS", "Geothermal Ground Source Heat Pump", "All-Air VAV System"])
        p["hvac_system"] = hvac_system
    with col2:
        pv_coverage = st.slider("BIPV Rooftop Solar Coverage (%)", 0, 100, 75, step=5)
        p["pv_coverage"] = pv_coverage
    with col3:
        target_leed = st.selectbox("Target Certification", ["LEED Platinum", "LEED Gold", "WELL Building Standard", "Net-Zero Carbon Certified"], index=0)
        p["energy_rating"] = target_leed

    eui = round(75.0 - (pv_coverage * 0.25) - (15.0 if "Geothermal" in hvac_system else 5.0), 1)
    annual_pv = int(total_gfa * 0.18 * (pv_coverage / 100))
    cooling_load = int(total_gfa * 0.085)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Energy Use Intensity", f"{eui:.1f} kWh/m²/yr", "Concept target")
    m2.metric("Annual PV Generation", f"{annual_pv:,} kWh", "Renewable offset")
    m3.metric("Peak Cooling Load", f"{cooling_load:,} TR", "Concept estimate")
    m4.metric("Certification Target", target_leed, "Design target")

    mep_df = pd.DataFrame(
        {
            "System Domain": ["Heating & Boiler", "Cooling & Chillers", "Ventilation (DOAS)", "Lighting & Plug Loads", "Renewable Generation"],
            "Consumption Share (%)": [15, 30, 25, 20, -35],
        }
    )
    fig = px.bar(
        mep_df,
        x="System Domain",
        y="Consumption Share (%)",
        title="Annual Energy Balance & Load Distribution",
        template="plotly_white",
        height=320,
    )
    fig.update_traces(marker_color="#000000")
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#000000"),
        margin=dict(t=45, b=10, l=10, r=10),
        showlegend=False,
    )
    fig.update_xaxes(gridcolor="#FFFFFF", color="#000000")
    fig.update_yaxes(gridcolor="#E5E5E5", color="#000000")
    st.plotly_chart(fig, use_container_width=True, key="mep_energy_balance")
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.project = p
