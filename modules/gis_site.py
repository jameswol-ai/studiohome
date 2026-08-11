import streamlit as st
import numpy as np
import pandas as pd

def render():
    st.header("GIS & Site Terrain Analyzer")
    st.write("Analyze topography contours, solar exposure vectors, and stormwater run-off paths.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            slope_angle = st.slider("Site Average Slope (°)", 0.0, 45.0, 8.5)
            soil_type = st.selectbox("Subsurface Soil Classification", ["Dense Sand / Gravel", "Stiff Clay", "Weathered Rock", "Soft Alluvium"])
        with col2:
            orientation = st.slider("Site Orientation Angle (° from North)", 0, 360, 45)
            st.metric("Geotechnical Bearing Capacity", f"{'300 kPa' if 'Rock' in soil_type else '150 kPa'}")

        x = np.linspace(0, 10, 100)
        elevation_profile = np.sin(x) * (slope_angle / 5.0)
        st.line_chart(pd.DataFrame({"Elevation Contour (m)": elevation_profile}, index=x))
        st.markdown('</div>', unsafe_allow_html=True)
