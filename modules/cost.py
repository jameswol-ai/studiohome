"""Parametric economic pro-forma and concept cost estimator."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.design_state import build_design_state


def render():
    st.markdown("## Economic Pro-Forma & Cost Estimating Agent")
    st.markdown("Real-time parametric capital expenditure, operating expenditure and project-return modeling from coordinated design quantities.")
    with st.container(border=True):
        p = st.session_state.project
        state = build_design_state(p)
        p.update(state)
        col1, col2 = st.columns(2)
        with col1:
            unit_rate = st.slider("Base Construction Unit Rate ($/m²)", 1200, 2500, int(p.get("unit_rate", 1650)), step=50)
            p["unit_rate"] = unit_rate
        with col2:
            contingency = st.slider("Project Contingency Rate (%)", 5, 20, 10, step=1)

        total_gfa = float(p.get("total_gfa", state["total_gfa"]))
        base_cost = total_gfa * unit_rate
        total_capex = base_cost * (1 + contingency / 100.0)
        p["estimated_cost"] = total_capex
        p["cost_contingency"] = contingency
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Project CAPEX", f"${total_capex:,.0f}", f"@ ${unit_rate}/m²")
        c2.metric("Hard Construction Costs", f"${base_cost:,.0f}", f"Contingency: {contingency}%")
        c3.metric("Estimated NOI (Annual)", f"${int(total_capex * 0.078):,.0f}", "7.8% yield assumption")
        c4.metric("Internal Rate of Return", "14.2%", "Target assumption")

        cost_df = pd.DataFrame({
            "Cost Category": ["Substructure & Foundations", "Superstructure & Frame", "Envelope & Glazing", "MEP & Smart Systems", "Interior Fit-Out & Soft Costs"],
            "Allocation ($)": [total_capex * 0.12, total_capex * 0.28, total_capex * 0.20, total_capex * 0.22, total_capex * 0.18],
        })
        fig = px.pie(cost_df, names="Cost Category", values="Allocation ($)", title="Parametric CAPEX Cost Breakdown", template="plotly_white", height=320, hole=0.4)
        fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10))
        fig.update_traces(textfont_color="#000000")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Coordinated Cost Drivers")
        st.dataframe(pd.DataFrame([
            ["Gross floor area", total_gfa, "m²"], ["Footprint", state["footprint_area"], "m²"],
            ["Envelope area", state["envelope_area"], "m²"], ["Window area", state["window_area"], "m²"],
            ["Roof area", state["roof_area"], "m²"], ["Storeys", state["floors"], "levels"],
        ], columns=["Quantity", "Value", "Unit"]), use_container_width=True, hide_index=True)
    st.session_state.project = p
