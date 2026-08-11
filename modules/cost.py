import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.markdown("## 💰 Dynamic Cost Estimation & Bill of Quantities")
    st.markdown("Real-time parametric budget forecasting, construction inflation tracking, and quantity takeoff modeling.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    total_gfa = st.number_input("Gross Floor Area (GFA m²)", value=5000.0, step=250.0)
    unit_rate = st.slider("Target Regional Unit Cost Rate ($/m²)", 900, 3000, 1550, step=50)
    
    total_budget = total_gfa * unit_rate
    cost_breakdown = {
        "Substructure & Excavation": total_budget * 0.10,
        "Structural Frame & Slabs": total_budget * 0.28,
        "Building Façade & Envelope": total_budget * 0.22,
        "Mechanical, Electrical & Plumbing": total_budget * 0.24,
        "Interior Fit-Out & Finishes": total_budget * 0.10,
        "Professional Fees & Contingency": total_budget * 0.06
    }
    
    st.metric("Total Estimated Capital Expenditure (CAPEX)", f"${total_budget:,.0f}")
    
    df_cost = pd.DataFrame(list(cost_breakdown.items()), columns=["Cost Element", "Allocation ($)"])
    fig = px.pie(df_cost, names="Cost Element", values="Allocation ($)", title="Capital Expenditure Proportion Breakdown", hole=0.45, template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=340, margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
