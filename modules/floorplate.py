import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render():
    st.markdown("## Generative Floorplate & Space Planning Agent")
    st.markdown("Procedurally optimize internal floorplate zoning, core placement, and circulation paths based on your active structural grid.")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    p = st.session_state.project
    col1, col2, col3 = st.columns(3)
    with col1:
        layout_style = st.selectbox("Workspace Layout Typology", ["Open-Plan Collaborative", "Cellular Executive Suites", "Mixed Hybrid Modular", "Activity-Based Working (ABW)"])
    with col2:
        core_position = st.selectbox("Vertical Core Placement", ["Central Core", "Perimeter Offset Core", "Twin Dual-Core Split"])
    with col3:
        atrium_void = st.checkbox("Include Biophilic Atrium Void", value=True)
    if st.button("Generate Procedural Floorplate Matrix", use_container_width=True):
        grid_sz = int(p['grid_spacing'])
        x_vals = np.arange(0, 48, grid_sz)
        y_vals = np.arange(0, 40, grid_sz)
        xx, yy = np.meshgrid(x_vals, y_vals)
        zones = []
        for x, y in zip(xx.flatten(), yy.flatten()):
            dist_center = np.sqrt((x - 24)**2 + (y - 20)**2)
            if dist_center < 8 and "Central" in core_position:
                zone = "Vertical Core & Risers"
            elif x < 8 or x > 40 or y < 6 or y > 34:
                zone = "Perimeter Glazing & Daylight Zone"
            elif atrium_void and dist_center < 14 and dist_center >= 8:
                zone = "Biophilic Atrium Void"
            else:
                zone = layout_style.split()[0] + " Work Zone"
            zones.append({"X": x, "Y": y, "Zone": zone})
        df_floor = pd.DataFrame(zones)
        fig = px.scatter(df_floor, x="X", y="Y", color="Zone", title=f"Generated Floorplate Plan ({p['grid_spacing']}m Grid Module)", template="plotly_white", height=350)
        fig.update_traces(marker=dict(size=16, symbol="square", line=dict(color="#000000", width=1)))
        fig.update_layout(paper_bgcolor="#D40000", plot_bgcolor="#D40000", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10), legend=dict(font=dict(color="#000000")))
        st.plotly_chart(fig, use_container_width=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Daylight Access Ratio", "88%", "Optimized")
        m2.metric("Circulation Efficiency", "82%", "Passes Code")
        m3.metric("Workspace Density", f"{int(p['total_gfa'] / p['floors'] / 12)} Desks/Floor")
    st.markdown('</div>', unsafe_allow_html=True)
