import streamlit as st
import pandas as pd

def render():
    st.header("Cost Estimation Engine")
    st.write("Dynamic budget modeling breakdown based on regional indices and material specifications.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        total_area = st.number_input("Total Gross Floor Area (GFA m²)", value=3500.0, step=250.0)
        unit_rate = st.slider("Base Unit Cost Rate ($/m²)", 800, 2500, 1400, step=50)
        
        base_cost = total_area * unit_rate
        breakdown = {
            "Substructure & Foundation": base_cost * 0.12,
            "Superstructure Frame": base_cost * 0.28,
            "Building Envelope & Facade": base_cost * 0.20,
            "MEP Services": base_cost * 0.22,
            "Interior Finishes & Fitout": base_cost * 0.10,
            "Contingency & Professional Fees": base_cost * 0.08
        }
        
        st.metric("Total Project Cost Estimate", f"${sum(breakdown.values()):,.0f}")
        st.bar_chart(pd.Series(breakdown))
        st.markdown('</div>', unsafe_allow_html=True)
