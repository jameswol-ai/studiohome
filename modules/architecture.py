import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render():
    st.markdown("## 📐 Architecture & Spatial Layout Agent")
    st.markdown("Generate and review spatial grid layouts, core riser positions, and functional zoning synchronized with your active project design.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Read synchronized project state
    p = st.session_state.project
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Typology", p["typology"])
    with col2:
        st.metric("Grid Module Spacing", f"{p['grid_spacing']}m x {p['grid_spacing']}m")
    with col3:
        st.metric("Total GFA", f"{p['total_gfa']:,.0f} m²")
        
    st.markdown("### 🏛️ Spatial Core & Zoning Configuration")
    
    # Interactive spatial distribution breakdown
    zones_df = pd.DataFrame({
        "Functional Zone": ["Core Circulation & Riser Shafts", "Primary Open Workspaces / Living", "Biophilic Atrium & Common Areas", "Service & MEP Plant"],
        "Area Allocation (%)": [15.0, 55.0, 20.0, 10.0],
        "Target Floor": [f"Levels 1–{p['floors']}", f"Levels 1–{p['floors']}", "Levels 1–3", f"Level {p['floors']} / Basement"]
    })
    
    st.dataframe(zones_df, use_container_width=True)
    
    # Plotly Scatter/Grid simulation representing spatial nodes
    grid_sz = int(p['grid_spacing'])
    x_coords = np.arange(0, 40, grid_sz)
    y_coords = np.arange(0, 40, grid_sz)
    xx, yy = np.meshgrid(x_coords, y_coords)
    
    grid_df = pd.DataFrame({
        "X": xx.flatten(),
        "Y": yy.flatten(),
        "Load Category": np.random.choice(["Core Column", "Perimeter Spandrel", "Atrium Void"], size=len(xx.flatten()), p=[0.6, 0.3, 0.1])
    })
    
    fig = px.scatter(grid_df, x="X", y="Y", color="Load Category", title=f"Synchronized Structural Grid Layout ({p['grid_spacing']}m Module)", template="plotly_dark", height=320)
    fig.update_traces(marker=dict(size=12, symbol="square"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
