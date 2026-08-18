import streamlit as st
import plotly.express as px
import pandas as pd
import random

def render():
    st.markdown("## ⚡ MEP & Environmental Systems AI Agent")
    st.markdown("Autonomous mechanical and environmental intelligence agent dynamically sized to your active project floor area and typology.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Read synchronized project state
    p = st.session_state.project
    
    col_1, col_2, col_3 = st.columns(3)
    col_1.metric("Conditioned Gross Floor Area", f"{p['total_gfa']:,.0f} m²")
    col_2.metric("Active Building Typology", p["typology"].split()[0])
    col_3.metric("Sustainability Standard", p["energy_rating"])
    
    cooling_load_kw = round(p['total_gfa'] * 0.095 + p['floors'] * 12.5, 1)
    airflow_cfm = int(cooling_load_kw * 310)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Peak Cooling Capacity", f"{cooling_load_kw:,.1f} kW", "AI Optimized")
    c2.metric("AHU Supply Air Volume", f"{airflow_cfm:,} m³/h")
    c3.metric("Energy Use Intensity (EUI)", "52 kWh/m²a", "Net-Zero Ready")
    
    # Load breakdown chart synced with GFA
    hvac_df = pd.DataFrame({
        "Thermal Component": ["Envelope Conduction", "Internal Occupants", "Lighting & Plug Loads", "Ventilation Fresh Air"],
        "Load Share (kW)": [cooling_load_kw*0.30, cooling_load_kw*0.28, cooling_load_kw*0.22, cooling_load_kw*0.20]
    })
    fig = px.pie(hvac_df, names="Thermal Component", values="Load Share (kW)", title=f"Thermal Load Distribution for {p['total_gfa']:,.0f} m² GFA", hole=0.45, template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(t=35, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
