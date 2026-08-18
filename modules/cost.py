import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.markdown("## 💰 Cost Estimation & Financial Pro-Forma AI")
    st.markdown("Parametric construction cost takeoffs dynamically calculated from your active design specification.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Read synchronized project state
    p = st.session_state.project
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gross Floor Area (GFA)", f"{p['total_gfa']:,.0f} m²")
    with col2:
        unit_rate = st.number_input("Unit Rate ($/m²)", value=float(p['unit_rate']), step=50.0)
    with col3:
        contingency_rate = st.slider("Contingency & Risk Buffer (%)", 5, 20, 12, step=1)
        
    base_capex = p['total_gfa'] * unit_rate
    total_capex = base_capex * (1 + contingency_rate / 100.0)
    
    # Update shared state with latest calculations
    st.session_state.project["estimated_cost"] = total_capex
    st.session_state.project["unit_rate"] = unit_rate
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Base Construction Cost", f"${base_capex:,.0f}")
    c2.metric("Total Project CAPEX", f"${total_capex:,.0f}", f"+{contingency_rate}% Buffer")
    c3.metric("Est. Net Operating Income", f"${total_capex * 0.085:,.0f}/yr", "8.5% Yield")
    
    # Cost element breakdown
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
    fig = px.bar(df_cost, x="Cost Element", y="Allocation ($)", color="Cost Element", title="Synchronized Parametric Cost Breakdown", template="plotly_dark", height=320)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
