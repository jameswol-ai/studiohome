"""Plumbing, drainage and fire protection preliminary design module."""

from __future__ import annotations

import math
import streamlit as st


def render() -> None:
    """Render preliminary water, drainage and fire-system design."""
    st.markdown("## 🚿 Plumbing, Drainage & Fire Protection")
    st.caption("Coordinate domestic water, hot water, sanitary drainage, stormwater, fire water storage, and preliminary riser strategy.")

    p = st.session_state.project
    floors = int(p.get("floors", 12))
    gfa = float(p.get("total_gfa", 30000.0))

    c1, c2, c3 = st.columns(3)
    with c1:
        occupants = st.number_input("Design Occupancy (people)", 10, 10000, max(100, int(gfa / 18)), 10)
    with c2:
        daily_lpc = st.number_input("Domestic Water Allowance (L/person/day)", 40.0, 400.0, 120.0, 5.0)
    with c3:
        peak_factor = st.slider("Peak Demand Factor", 1.2, 4.0, 2.5, 0.1)

    daily_m3 = occupants * daily_lpc / 1000.0
    peak_lps = daily_m3 * peak_factor / 86.4
    storage_m3 = daily_m3 * 1.25
    fire_storage = max(20.0, floors * 2.0)
    stormwater_m3 = gfa * 0.025 / 1000.0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Daily Domestic Water", f"{daily_m3:,.1f} m³/day")
    m2.metric("Peak Flow", f"{peak_lps:.2f} L/s")
    m3.metric("Domestic Storage", f"{storage_m3:,.1f} m³")
    m4.metric("Indicative Fire Storage", f"{fire_storage:,.0f} m³")

    st.markdown("### 🧯 Systems Strategy")
    c1, c2, c3 = st.columns(3)
    with c1:
        p["water_strategy"] = st.selectbox("Water Distribution", ["Direct mains", "Roof tank + gravity", "Break tank + booster", "Dual-zone boosted system"])
    with c2:
        p["drainage_strategy"] = st.selectbox("Drainage", ["Gravity sanitary + storm", "Gravity + pumped basement drainage", "Separate greywater reuse", "Blackwater treatment + reuse"])
    with c3:
        p["fire_strategy"] = st.selectbox("Fire Protection", ["Wet sprinkler + hydrants", "Wet sprinkler + standpipe", "Dry / wet hybrid", "Engineered special hazard system"])

    st.markdown("### 📏 Preliminary Riser Coordination")
    risers = max(2, math.ceil(floors / 6))
    st.write(f"Suggested vertical plumbing/service riser zones: **{risers}**. Coordinate final shaft sizes, fixture units, pressure zones, fire-flow demand, and authority requirements during detailed design.")
    st.info("Preliminary planning tool only. Final plumbing, drainage and fire-protection design requires applicable code calculations, hydraulic analysis, authority review, and qualified-engineer/fire-specialist approval.")
