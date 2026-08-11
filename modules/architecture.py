import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def render():
    st.markdown("## 🏛️ Advanced Architecture & Spatial Zoning Engine")
    st.markdown("Configure multi-zone floorplate distributions, core circulation strategies, and programmatic space-planning matrices.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        grid_spacing = st.slider("Structural Column Grid Module (m)", 4.0, 12.0, 8.0, step=0.5)
    with col2:
        grid_extent = st.slider("Total Floorplate Side Extent (m)", 24, 96, 48, step=4)
    with col3:
        core_type = st.selectbox("Vertical Circulation Core", [
            "Central Service Core", 
            "Dual Side Core Banks", 
            "Perimeter Anchor Core", 
            "Atrium Perimeter Ring"
        ])
        
    col_a, col_b = st.columns(2)
    with col_a:
        primary_program = st.selectbox("Dominant Interior Program", ["Open-Plan Coworking", "Cellular Executive Suites", "Laboratories & R&D", "Civic Atrium & Gallery"])
    with col_b:
        glazing_ratio = st.slider("Facade Glazing Ratio (%)", 20, 95, 65, step=5)

    if st.button("Generate Spatial Matrix & Zoning Layout", use_container_width=True):
        rows = int(grid_extent / grid_spacing)
        cols = rows
        matrix_data = []
        zone_counts = {"Core": 0, "Perimeter Glazing": 0, "Interior Workstation": 0}
        
        for r in range(rows):
            row_vals = []
            for c in range(cols):
                if core_type == "Central Service Core" and abs(r - rows/2) < 1.2 and abs(c - cols/2) < 1.2:
                    zone = "🔒 Service Core"
                    zone_counts["Core"] += 1
                elif r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    zone = f"🌿 Perimeter ({glazing_ratio}% Glaze)"
                    zone_counts["Perimeter Glazing"] += 1
                else:
                    zone = f"🏢 {primary_program}"
                    zone_counts["Interior Workstation"] += 1
                row_vals.append(zone)
            matrix_data.append(row_vals)
            
        df_grid = pd.DataFrame(matrix_data, columns=[f"X: {i*grid_spacing}m" for i in range(cols)], index=[f"Y: {i*grid_spacing}m" for i in range(rows)])
        
        st.success(f"Successfully synthesized {rows} × {cols} architectural floorplate utilizing **{core_type}** and **{primary_program}**.")
        
        # Display Interactive Matrix Table
        st.dataframe(df_grid, use_container_width=True)
        
        # Programmatic Space Allocation Donut Chart using Plotly
        df_zones = pd.DataFrame(list(zone_counts.items()), columns=["Zone Type", "Module Count"])
        fig = px.pie(df_zones, names="Zone Type", values="Module Count", title="Spatial Program Allocation Ratio", hole=0.45, template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300, margin=dict(t=35, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

