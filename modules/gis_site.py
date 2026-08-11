import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def render():
    st.markdown("## 🌍 GIS & Site Terrain Analyzer")
    st.markdown("Examine topological surface contours, geotechnical profiles, and solar radiation exposure vectors.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        slope_angle = st.slider("Site Average Inclination Slope (°)", 0.0, 40.0, 6.5, step=0.5)
        soil_profile = st.selectbox("Subsurface Geotechnical Stratum", ["Dense Weathered Sandstone", "Stiff Glacial Till", "Competent Bedrock", "Alluvial Silt Deposits"])
    with col2:
        solar_orientation = st.slider("Site Aspect Orientation (° from North)", 0, 360, 30, step=15)
        bearing_capacity = 350 if "Bedrock" in soil_profile or "Sandstone" in soil_profile else 160
        st.metric("Allowable Bearing Capacity", f"{bearing_capacity} kPa")

    # 3D Elevation Mesh Simulation using Plotly
    x = np.linspace(-10, 10, 40)
    y = np.linspace(-10, 10, 40)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X / 3) * np.cos(Y / 3) * (slope_angle / 3.0)

    fig = px.imshow(Z, title="Topographic Elevation Heatmap & Contour Projection", template="plotly_dark", color_continuous_scale="Viridis")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
