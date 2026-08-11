import streamlit as st
import pandas as pd

def render():
    st.header("Architecture Engine")
    st.write("Configure spatial zoning, programmatic distribution, and structural column grids.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            grid_spacing = st.slider("Grid spacing (m)", 3.0, 12.0, 6.0, step=0.5)
        with col2:
            grid_extent = st.slider("Grid dimension extent (m)", 12, 80, 36, step=4)
        with col3:
            core_type = st.selectbox("Core Configuration", ["Central Core", "Dual Side Cores", "Perimeter Core", "Open Plan"])
        
        if st.button("Compute Spatial Grid Layout", use_container_width=True):
            rows = int(grid_extent / grid_spacing)
            cols = rows
            grid_matrix = []
            for r in range(rows):
                row_items = []
                for c in range(cols):
                    zone_label = "Core" if (core_type=="Central Core" and abs(r-rows/2)<1 and abs(c-cols/2)<1) else f"Zone-{r},{c}"
                    row_items.append(zone_label)
                grid_matrix.append(row_items)
            df_grid = pd.DataFrame(grid_matrix, columns=[f"X:{i*grid_spacing}m" for i in range(cols)], index=[f"Y:{i*grid_spacing}m" for i in range(rows)])
            st.success(f"Generated {rows}x{cols} grid network with {core_type}.")
            st.dataframe(df_grid, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
