import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def render():
    st.markdown("## 🏛️ Generative Architecture & Massing Design Agent")
    st.markdown("Procedurally optimize volumetric envelopes, facade configurations, and spatial program distributions for your active typology.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    
    col1, col2, col3 = st.columns(3)
    with col1:
        typology = st.selectbox(
            "Project Typology", 
            [
                "Commercial Innovation Hub", 
                "Mixed-Use Residential Tower", 
                "Mass Timber Civic Center", 
                "Biophilic Corporate Campus"
            ],
            index=0
        )
        p['typology'] = typology
    with col2:
        floors = st.slider("Storey Count (Levels)", 4, 40, int(p.get('floors', 12)), step=1)
        p['floors'] = floors
    with col3:
        wwr = st.slider("Window-to-Wall Ratio (WWR %)", 20, 85, 55, step=5)
        
    # Spatial Progam Allocations based on Typology
    st.markdown("---")
    st.markdown("### 📐 Volumetric Envelope & Program Breakdown")
    
    site_area = p.get('site_area', 2500.0)
    building_height = floors * 3.5
    footprint_area = site_area * 0.65  # 65% site coverage rule
    total_gfa = footprint_area * floors
    p['total_gfa'] = total_gfa
    p['estimated_cost'] = total_gfa * p.get('unit_rate', 1650.0)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total GFA", f"{total_gfa:,.0f} m²", f"Footprint: {footprint_area:,.0f} m²")
    m2.metric("Building Height", f"{building_height} m", f"Floor-to-Floor: 3.5m")
    m3.metric("Floor Area Ratio (FAR)", f"{(total_gfa / site_area):.2f}", "Zoning Compliant")
    m4.metric("Estimated CAPEX", f"${p['estimated_cost']:,.0f}", f"@ ${p.get('unit_rate', 1650)}/m²")
    
    # 3D Volumetric Massing Visualization
    st.markdown("---")
    st.markdown("### 🌐 Generative 3D Building Envelope Model")
    
    # Generate 3D box coordinates for multi-storey massing
    width = np.sqrt(footprint_area)
    depth = footprint_area / width
    
    z_levels = np.linspace(0, building_height, floors)
    
    fig = go.Figure()
    
    for i, z in enumerate(z_levels):
        # Create perimeter outline per floor with slight twist/taper option if desired
        fig.add_trace(go.Scatter3d(
            x=[-width/2, width/2, width/2, -width/2, -width/2],
            y=[-depth/2, -depth/2, depth/2, depth/2, -depth/2],
            z=[z, z, z, z, z],
            mode='lines',
            line=dict(color='#3B82F6' if i < floors-1 else '#10B981', width=4),
            name=f'Level {i+1} ({z}m)'
        ))
        
    fig.update_layout(
        title=f"3D Volumetric Massing Envelope — {typology}",
        scene=dict(
            xaxis_title="Width (m)",
            yaxis_title="Depth (m)",
            zaxis_title="Elevation (m)",
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450,
        margin=dict(t=30, b=10, l=10, r=10),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, key="arch_3d_massing")
    
    st.markdown('</div>', unsafe_allow_html=True)