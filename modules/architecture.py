import streamlit as st
import pandas as pd
import numpy as np

def render():
    st.markdown("## 🏛️ Architecture & Spatial Zoning Engine")
    st.markdown("Define modular structural column grids, programmatic allocations, and core circulation strategies.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        grid_spacing = st.slider("Column Grid Spacing (m)", 4.0, 12.0, 8.0, step=0.5)
    with col2:
        grid_extent = st.slider("Total Floorplate Extent (m)", 20, 80, 48, step=4)
    with col3:
        core_type = st.selectbox("Core Layout Architecture", ["Central Service Core", "Dual Side Core Banks", "Perimeter Anchor Core", "Atrium Perimeter Ring"])
    
    if st.button("Generate Spatial Matrix", use_container_width=True):
        rows = int(grid_extent / grid_spacing)
        cols = rows
        matrix_data = []
        for r in range(rows):
            row_vals = []
            for c in range(cols):
                if core_type == "Central Service Core" and abs(r - rows/2) < 1.2 and abs(c - cols/2) < 1.2:
                    zone = "🔒 Service Core"
                elif r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    zone = "🌿 Perimeter Glazing"
                else:
                    zone = f"🏢 Zone [{r},{c}]"
                row_vals.append(zone)
            matrix_data.append(row_vals)
            
        df_grid = pd.DataFrame(matrix_data, columns=[f"X: {i*grid_spacing}m" for i in range(cols)], index=[f"Y: {i*grid_spacing}m" for i in range(rows)])
        st.success(f"Successfully configured spatial layout grid: {rows} × {cols} zones using {core_type}.")
        st.dataframe(df_grid, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
