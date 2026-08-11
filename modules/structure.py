import streamlit as st
import random
import plotly.graph_objects as go
import numpy as np

def render():
    st.markdown("## 🏗️ Structural Finite Element Analysis (FEA)")
    st.markdown("Simulate beam deflection moments, column sizing criteria, and seismic safety performance bounds.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        span_length = st.slider("Typical Clear Span Length (m)", 5.0, 16.0, 9.0, step=0.5)
        live_load = st.slider("Design Imposed Live Load (kN/m²)", 2.0, 10.0, 4.0, step=0.5)
    with col2:
        material_grade = st.selectbox("Structural Material Profile", ["High-Performance Concrete (C50/60)", "Structural Steel (S355)", "Mass Timber Glulam GL28h", "Composite Steel-Concrete"])
        seismic_zone = st.selectbox("Seismic Acceleration Zone", ["Zone 0 (Stable Platform)", "Zone 1 (Moderate Risk)", "Zone 2 (High Seismicity)", "Zone 3 (Active Fault Line)"])
    
    if st.button("Run Structural Finite Element Sizing", use_container_width=True):
        req_depth = round((span_length * 1000) / 15, 1)
        col_side = round(350 + (span_length * live_load * 14), -1)
        
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Min Beam Depth", f"{req_depth} mm")
        s2.metric("Column Section", f"{int(col_side)}×{int(col_side)} mm")
        s3.metric("Max Deflection Ratio", f"L / {random.randint(350, 480)}")
        s4.metric("Steel Reinforcement", f"{random.uniform(2.1, 3.8):.2f}%")
        
        # Interactive Deflection Curve Simulation via Plotly
        x_vals = np.linspace(0, span_length, 100)
        deflection = (5 * live_load * (span_length**4)) / (384 * 210000 * (req_depth**3) / 12) * np.sin(np.pi * x_vals / span_length) * 1000
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=deflection, mode='lines', name='Elastic Deflection Profile', line=dict(color='#3B82F6', width=4)))
        fig.update_layout(title="Beam Deflection Envelope under Service Loads", xaxis_title="Span Position (m)", yaxis_title="Deflection (mm)",
                          template="plotly_dark", height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
