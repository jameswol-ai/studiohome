import streamlit as st
import plotly.express as px
import pandas as pd

def render():
    st.markdown("## ♻️ Life Cycle Assessment & Material Circularity Audit")
    st.markdown("Quantify cradle-to-cradle embodied carbon, end-of-life material recovery potential, and circularity index scores.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    
    col1, col2, col3 = st.columns(3)
    with col1:
        timber_ratio = st.slider("Mass Timber Structural Ratio (%)", 0, 100, 85, step=5)
    with col2:
        recycled_steel = st.slider("Recycled Steel Content (%)", 20, 100, 90, step=5)
    with col3:
        facade_type = st.selectbox("Envelope Specification", ["Triple-Glazed Unitized Curtain Wall", "Biophilic Terracotta Composite", "Photovoltaic Integrated BIPV"])
        
    embodied_c = round(p['total_gfa'] * (0.18 if timber_ratio > 70 else 0.45), 1)
    circularity_score = round(75 + (timber_ratio * 0.15) + (recycled_steel * 0.10), 1)
    
    # Update shared project state carbon score
    p['carbon_score'] = embodied_c
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Embodied Carbon", f"{embodied_c:,.1f} tCO₂e", "-58% vs Baseline")
    c2.metric("Circularity Index", f"{circularity_score}%", "High Reuse")
    c3.metric("Carbon Payback Period", "4.2 Years", "Optimal")
    c4.metric("End-of-Life Recovery", f"{int(timber_ratio + 10)}%", "A+ Grade")
    
    lca_df = pd.DataFrame({
        "Lifecycle Stage": ["A1-A3 Product Production", "A4-A5 Construction Process", "B1-B7 In-Service Use & Energy", "C1-C4 End-of-Life & Recovery"],
        "Carbon Impact (tCO₂e)": [embodied_c * 0.45, embodied_c * 0.10, embodied_c * 0.15, embodied_c * 0.30]
    })
    
    fig = px.bar(lca_df, x="Lifecycle Stage", y="Carbon Impact (tCO₂e)", color="Lifecycle Stage", 
                 title="EN 15978 Cradle-to-Grave Carbon Breakdown", template="plotly_dark", height=320)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)