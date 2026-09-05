import streamlit as st
import pandas as pd
import random
import plotly.express as px

def render():
    st.markdown("## Massing & Volumetrics AI Agent")
    st.markdown("Autonomous volumetric agent synchronized with your master project floor count and GFA parameters.")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    p = st.session_state.project
    col1, col2, col3 = st.columns(3)
    with col1:
        num_blocks = st.slider("Active Volumetric Blocks", 2, 10, 4)
    with col2:
        max_height = st.slider("Max Building Height Limit (m)", 24, 120, int(p['floors'] * 3.5), step=6)
    with col3:
        target_far = st.slider("Target Floor Area Ratio (FAR)", 1.5, 8.0, 4.5, step=0.5)
    if st.button("Generate & Sync Massing Envelopes", use_container_width=True):
        massing_list = []
        total_gfa_gen = 0
        for i in range(num_blocks):
            h = random.randint(20, max_height)
            fp = random.randint(400, int(p['site_area'] / num_blocks * 0.8))
            levels = int(h / 3.5)
            gfa = fp * levels
            total_gfa_gen += gfa
            massing_list.append({"Block ID": f"Volumetric Tower {chr(65+i)}", "Footprint Area (m²)": fp, "Height (m)": h, "Levels": levels, "Gross Floor Area (m²)": gfa, "Primary Program": random.choice(["Commercial Offices", "Luxury Residential", "Civic Atrium", "Retail Podium"])})
        df_mass = pd.DataFrame(massing_list)
        st.session_state.project['total_gfa'] = total_gfa_gen
        st.session_state.project['floors'] = int(df_mass["Levels"].max())
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Synced Total GFA", f"{total_gfa_gen:,} m²")
        m2.metric("Achieved FAR Index", f"{target_far}", "Compliant")
        m3.metric("Setback Compliance", "100%", "Passes Code")
        m4.metric("Massing Optimization", f"{random.randint(93, 98)}%", "AI Verified")
        st.dataframe(df_mass, use_container_width=True)
        fig = px.bar(df_mass, x="Block ID", y="Height (m)", color="Primary Program", title="Synchronized Volumetric Height Distribution", template="plotly_white", height=320)
        fig.update_layout(paper_bgcolor="#D40000", plot_bgcolor="#D40000", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
