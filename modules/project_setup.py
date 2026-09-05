"""Project setup and AEC design brief module."""

from __future__ import annotations

import streamlit as st


def render() -> None:
    """Render the project setup workspace."""
    st.markdown("## 🧭 Project Setup & AEC Design Brief")
    st.caption("Define the project brief, site parameters, performance targets, and delivery assumptions used by downstream design modules.")

    p = st.session_state.project

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            p["project_name"] = st.text_input("Project Name", p.get("project_name", "studiohome AEC Project"))
            p["client"] = st.text_input("Client / Developer", p.get("client", "Studiohome Development"))
        with c2:
            p["typology"] = st.selectbox(
                "Building Typology",
                [
                    "Commercial Innovation Hub",
                    "Mixed-Use Development",
                    "Residential Tower",
                    "Healthcare Facility",
                    "Education Campus",
                    "Industrial / Logistics Facility",
                    "Civic / Institutional Building",
                ],
                index=[
                    "Commercial Innovation Hub",
                    "Mixed-Use Development",
                    "Residential Tower",
                    "Healthcare Facility",
                    "Education Campus",
                    "Industrial / Logistics Facility",
                    "Civic / Institutional Building",
                ].index(p.get("typology", "Commercial Innovation Hub")),
            )
        with c3:
            p["delivery_method"] = st.selectbox(
                "Procurement / Delivery",
                ["Design-Bid-Build", "Design & Build", "EPC / Turnkey", "Construction Management"],
                index=1,
            )

    st.markdown("### 📐 Core Project Parameters")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        p["site_area"] = st.number_input("Site Area (m²)", min_value=100.0, value=float(p.get("site_area", 2500.0)), step=100.0)
    with c2:
        p["floors"] = st.number_input("Storeys", min_value=1, max_value=100, value=int(p.get("floors", 12)), step=1)
    with c3:
        p["grid_spacing"] = st.number_input("Structural Grid (m)", min_value=3.0, max_value=20.0, value=float(p.get("grid_spacing", 8.0)), step=0.5)
    with c4:
        p["floor_to_floor"] = st.number_input("Floor-to-Floor (m)", min_value=2.4, max_value=6.0, value=float(p.get("floor_to_floor", 3.5)), step=0.1)

    p["total_gfa"] = p["site_area"] * 0.65 * p["floors"]
    p["estimated_cost"] = p["total_gfa"] * p.get("unit_rate", 1650.0)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Indicative GFA", f"{p['total_gfa']:,.0f} m²")
    m2.metric("Building Height", f"{p['floors'] * p['floor_to_floor']:.1f} m")
    m3.metric("Indicative CAPEX", f"${p['estimated_cost']:,.0f}")
    m4.metric("Design Grid", f"{p['grid_spacing']:.1f} × {p['grid_spacing']:.1f} m")

    st.markdown("### 🎯 Performance Brief")
    c1, c2, c3 = st.columns(3)
    with c1:
        p["energy_target"] = st.selectbox("Energy Target", ["Conventional", "High Performance", "Net-Zero Ready", "Net-Zero Carbon"], index=2)
    with c2:
        p["carbon_target"] = st.number_input("Embodied Carbon Target (kgCO₂e/m²)", min_value=50.0, max_value=1200.0, value=float(p.get("carbon_target", 420.0)), step=10.0)
    with c3:
        p["code_basis"] = st.selectbox("Primary Code Basis", ["International / IBC", "Eurocodes", "BS Standards", "Local Authority / National Code"], index=0)
