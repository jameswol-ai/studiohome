"""Civil works and site infrastructure planning module."""

from __future__ import annotations

import streamlit as st


def render() -> None:
    """Render preliminary civil/site infrastructure planning."""
    st.markdown("## 🚧 Civil Works & Site Infrastructure")
    st.caption("Coordinate grading, access, parking, drainage, utilities corridors, landscape interfaces, and construction-site constraints.")

    p = st.session_state.project
    site_area = float(p.get("site_area", 2500.0))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        coverage = st.slider("Impervious Site Coverage (%)", 20, 95, 65, 5)
    with c2:
        road_width = st.number_input("Primary Access Width (m)", 4.0, 14.0, 6.0, 0.5)
    with c3:
        parking_ratio = st.number_input("Parking Bays / 100 m² GFA", 0.0, 8.0, 1.5, 0.1)
    with c4:
        rainfall = st.number_input("Design Rainfall Intensity (mm/hr)", 20.0, 250.0, 80.0, 5.0)

    impervious = site_area * coverage / 100.0
    landscaped = site_area - impervious
    gfa = float(p.get("total_gfa", site_area))
    parking = round(gfa / 100.0 * parking_ratio)
    runoff_index = impervious * rainfall / 1000.0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Impervious Area", f"{impervious:,.0f} m²")
    m2.metric("Landscape / Permeable", f"{landscaped:,.0f} m²")
    m3.metric("Indicative Parking", f"{parking:,} bays")
    m4.metric("Runoff Index", f"{runoff_index:,.1f}")

    st.markdown("### 🛣️ Site Strategy")
    c1, c2, c3 = st.columns(3)
    with c1:
        p["site_access"] = st.selectbox("Access Strategy", ["Single primary access", "Separate service + public access", "Loop road", "Two-access resilience"])
    with c2:
        p["stormwater_strategy"] = st.selectbox("Stormwater", ["Conventional drainage", "Detention + controlled discharge", "SuDS / bioswales", "Rainwater harvesting + SuDS"])
    with c3:
        p["utility_strategy"] = st.selectbox("Utilities Corridor", ["Central service trench", "Perimeter utility corridor", "Shared underground services", "Distributed utility zones"])

    st.success("Civil coordination baseline established. Link this module with GIS & Site, Architecture, Structure, MEP and Cost before issuing a coordinated design package.")
