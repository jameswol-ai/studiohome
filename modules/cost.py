import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.markdown("## 💰 Cost Estimation & Financial Pro-Forma AI")
    st.markdown("Run parametric construction cost takeoffs, inflation forecasting, and real-time capital expenditure (CAPEX) simulations.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_gfa = st.number_input("Gross Floor Area (GFA m²)", value=5500.0, step=250.0)
    with col2:
        unit_rate = st.slider("Base Regional Construction Rate ($/m²)", 1000, 3500, 1650, step=50)
    with col3:
        contingency_rate = st.slider("Contingency & Risk Buffer (%)", 5, 20, 12, step=1)
        
    base_capex = total_gfa * unit_rate
    total_capex = base_capex * (1 + contingency_rate / 100.0)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Base Construction Cost", f"${base_capex:,.0f}")
    c2.metric("Total Project CAPEX", f"${total_capex:,.0f}", f"+{contingency_rate}% Buffer")
    c3.metric("Est. Net Operating Income", f"${total_capex * 0.085:,.0f}/yr", "8.5% Yield")
    
    # Cost element breakdown dataframe & visualization
    cost_data = {
        "Cost Element": ["Substructure & Foundations", "Structural Frame & Slabs", "Façade & Envelope", "MEP & Smart Core", "Interior Fit-Out", "Professional Fees & Contingency"],
        "Allocation ($)": [
            total_capex * 0.10,
            total_capex * 0.28,
            total_capex * 0.20,
            total_capex * 0.22,
            total_capex * 0.12,
            total_capex * (contingency_rate / 100.0)
        ]
    }
    
    df_cost = pd.DataFrame(cost_data)
    fig = px.bar(df_cost, x="Cost Element", y="Allocation ($)", color="Cost Element", title="AI Parametric Cost Element Distribution", template="plotly_dark", height=320)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
