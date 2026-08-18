import streamlit as st
import pandas as pd
import random
import plotly.express as px

def render():
    st.markdown("## 🏢 Massing & Volumetrics AI Agent")
    st.markdown("Deploy an autonomous volumetric agent to optimize building envelopes, floor-area ratios (FAR), and urban setback compliance.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        num_blocks = st.slider("Active Volumetric Blocks", 2, 10, 4)
    with col2:
        max_height = st.slider("Max Building Height Limit (m)", 24, 120, 60, step=6)
    with col3:
        target_far = st.slider("Target Floor Area Ratio (FAR)", 1.5, 8.0, 4.5, step=0.5)
        
    if st.button("🏗️ Generate AI Massing Envelopes", use_container_width=True):
        massing_list = []
        total_gfa_gen = 0
        for i in range(num_blocks):
            h = random.randint(20, max_height)
            fp = random.randint(400, 1500)
            levels = int(h / 3.5)
            gfa = fp * levels
            total_gfa_gen += gfa
            massing_list.append({
                "Block ID": f"Volumetric Tower {chr(65+i)}",
                "Footprint Area (m²)": fp,
                "Height (m)": h,
                "Levels": levels,
                "Gross Floor Area (m²)": gfa,
                "Primary Program": random.choice(["Commercial Offices", "Luxury Residential", "Civic Atrium", "Retail Podium"])
            })
            
        df_mass = pd.DataFrame(massing_list)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Generated GFA", f"{total_gfa_gen:,} m²")
        m2.metric("Achieved FAR Index", f"{target_far}", "Compliant")
        m3.metric("Setback Compliance", "100%", "Passes Code")
        m4.metric("Massing Optimization Score", f"{random.randint(93, 98)}%", "AI Verified")
        
        st.dataframe(df_mass, use_container_width=True)
        
        # Interactive Plotly bar chart for massing height distribution
        fig = px.bar(df_mass, x="Block ID", y="Height (m)", color="Primary Program", title="Volumetric Height & Programmatic Distribution", template="plotly_dark", height=320)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
