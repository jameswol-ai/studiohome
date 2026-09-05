"""Electrical building-services design module."""

from __future__ import annotations

import math
import streamlit as st


def render() -> None:
    """Render preliminary electrical load and distribution design."""
    st.markdown("## 🔌 Electrical Design & Power Systems")
    st.caption("Develop preliminary electrical demand, distribution, standby power, renewable generation, and resilience strategies.")

    p = st.session_state.project
    gfa = float(p.get("total_gfa", 30000.0))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        lighting = st.number_input("Lighting Load (W/m²)", 4.0, 25.0, 10.0, 0.5)
    with c2:
        small_power = st.number_input("Small Power (W/m²)", 5.0, 35.0, 12.0, 0.5)
    with c3:
        hvac_kw = st.number_input("HVAC Connected Load (kW)", 50.0, 10000.0, max(250.0, gfa * 0.08), 50.0)
    with c4:
        demand_factor = st.slider("Overall Demand Factor", 0.50, 0.95, 0.75, 0.05)

    connected_kw = (gfa * (lighting + small_power) / 1000.0) + hvac_kw
    demand_kw = connected_kw * demand_factor
    transformer_kva = math.ceil((demand_kw / 0.90) / 50.0) * 50
    standby_kva = math.ceil((demand_kw * 0.65 / 0.90) / 50.0) * 50

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Connected Load", f"{connected_kw:,.0f} kW")
    m2.metric("Maximum Demand", f"{demand_kw:,.0f} kW")
    m3.metric("Transformer Allowance", f"{transformer_kva:,.0f} kVA")
    m4.metric("Standby Generator", f"{standby_kva:,.0f} kVA")

    st.markdown("### ⚡ Electrical Architecture")
    c1, c2, c3 = st.columns(3)
    with c1:
        p["electrical_distribution"] = st.selectbox("Distribution", ["LV radial", "LV busbar trunking", "MV/LV dual-transformer", "Dual utility + generator"])
    with c2:
        p["backup_strategy"] = st.selectbox("Backup Strategy", ["Generator", "Generator + UPS", "Battery energy storage", "Generator + BESS + UPS"])
    with c3:
        p["renewable_target"] = st.slider("On-site Renewable Target (%)", 0, 100, int(p.get("renewable_target", 30)), 5)

    st.info("Preliminary sizing only. Final electrical design must be checked against the applicable electrical code, utility requirements, protection studies, short-circuit levels, voltage drop, earthing, and qualified-engineer review.")
