import streamlit as st
import pandas as pd
import random
import plotly.express as px

def render():
    st.markdown("## 🏢 Interactive Spatial Massing Viewer")
    st.markdown("Inspect volumetric block distributions, proportional floor heights, and functional zoning envelopes.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    num_blocks = st.slider("Active Massing Blocks", 2, 10, 5)
    
    massing_list = []
    for i in range(num_blocks):
        massing_list.append({
            "Block ID": f"Volumetric Block {chr(65+i)}",
            "Footprint (m²)": random.randint(300, 1200),
            "Height (m)": random.randint(18, 75),
            "Levels": random.randint(5, 22),
            "Program": random.choice(["Executive Offices", "Residential Apartments", "Retail Podium", "Civic Atrium"])
        })
        
    df_mass = pd.DataFrame(massing_list)
    st.dataframe(df_mass, use_container_width=True)
    
    fig = px.bar(df_mass, x="Block ID", y="Height (m)", color="Program", title="Massing Height Distribution across Blocks", template="plotly_dark", height=300)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
