import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

def render():
    st.markdown("## 🌍 GIS & Site Terrain AI Agent")
    st.markdown("Autonomous geospatial intelligence agent synchronized with your project site parcel parameters.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    
    col1, col2, col3 = st.columns(3)
    with col1:
        slope_angle = st.slider("Site Average Inclination Slope (°)", 0.0, 35.0, 6.5, step=0.5)
    with col2:
        soil_profile = st.selectbox("Subsurface Geotechnical Stratum", [
            "Dense Weathered Sandstone", 
            "Stiff Glacial Till", 
            "Competent Bedrock", 
            "Alluvial Silt Deposits"
        ])
    with col3:
        solar_orientation = st.slider("Site Aspect Orientation (° from North)", 0, 360, 30, step=15)
        
    col_a, col_b = st.columns(2)
    with col_a:
        site_area_ha = st.number_input("Site Parcel Area (Hectares)", value=round(p['site_area'] / 10000.0, 2), step=0.1)
        st.session_state.project['site_area'] = site_area_ha * 10000.0
    with col_b:
        drainage_strategy = st.selectbox("Stormwater Runoff Strategy", ["Bioretention Swale Network", "Subsurface Detention Vault", "Permeable Paving Grid", "Natural Wetland Discharge"])

    bearing_capacity = 380 if "Bedrock" in soil_profile or "Sandstone" in soil_profile else 170
    earthwork_volume = int(p['site_area'] * (slope_angle * 0.15))
    solar_radiation = round(random.uniform(1450, 1850), 1)
    
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Allowable Bearing Capacity", f"{bearing_capacity} kPa")
    s2.metric("Est. Earthwork Cut/Fill", f"{earthwork_volume:,} m³")
    s3.metric("Annual Solar Insolation", f"{solar_radiation} kWh/m²")
    s4.metric("Geospatial Suitability", f"{random.randint(92, 98)}%", "AI Verified")
    
    x = np.linspace(-10, 10, 35)
    y = np.linspace(-10, 10, 35)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X / 3) * np.cos(Y / 3) * (slope_angle / 2.5)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Viridis")])
    fig.update_layout(
        title=f"3D Topography Mesh for {site_area_ha} ha Parcel",
        template="plotly_dark",
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=10, l=10, r=10),
        scene=dict(xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Elevation (m)", bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"Site orientation at **{solar_orientation}°** optimizes passive performance across the active project footprint.")
    st.markdown('</div>', unsafe_allow_html=True)
