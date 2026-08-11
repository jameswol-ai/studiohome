import streamlit as st
import plotly.express as px
import pandas as pd

def render():
    st.markdown("## ⚡ MEP Systems & Environmental Engineering")
    st.markdown("Size HVAC thermal loads, electrical substation transformer capacity, and hydraulic flow distribution pipes.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    mep_tab1, mep_tab2, mep_tab3 = st.tabs(["❄️ Mechanical & HVAC", "⚡ Electrical Infrastructure", "💧 Plumbing & Drainage"])
    
    with mep_tab1:
        floor_area = st.number_input("Conditioned Gross Floor Area (m²)", value=4200.0, step=200.0)
        occupants = st.number_input("Maximum Occupancy Load", value=280, step=20)
        cooling_kw = round(floor_area * 0.115 + occupants * 0.14, 1)
        airflow = int(cooling_kw * 320)
        
        c1, c2 = st.columns(2)
        c1.metric("Peak Cooling Capacity Required", f"{cooling_kw:,.1f} kW")
        c2.metric("AHU Supply Airflow Volume", f"{airflow:,} m³/h")
        
        # Pie chart of HVAC load breakdown
        hvac_df = pd.DataFrame({
            "Source": ["Envelope Conduction", "Internal Occupants", "Lighting & Equipment", "Ventilation Fresh Air"],
            "Load (kW)": [cooling_kw*0.35, cooling_kw*0.25, cooling_kw*0.20, cooling_kw*0.20]
        })
        fig = px.pie(hvac_df, names="Source", values="Load (kW)", title="Thermal Load Component Breakdown", hole=0.4, template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(t=30, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with mep_tab2:
        transformer_kva = int((floor_area * 0.085) + 150)
        st.metric("Recommended Main Transformer Capacity", f"{transformer_kva} kVA")
        st.write("Configured Primary Switchgear Panels:")
        st.json({"Main Switchboard (MSB)": "1200A 3P+N", "HVAC Motor Control Center": "600A 3P", "Critical Life-Safety Backup": "300A Auto-Transfer Switch"})
        
    with mep_tab3:
        water_lpd = int(occupants * 55)
        st.metric("Estimated Daily Potable Water Demand", f"{water_lpd:,} Liters/day")
        st.metric("Sanitary Drainage Peak Discharge", f"{round(water_lpd * 0.0005, 2)} L/s")
    st.markdown('</div>', unsafe_allow_html=True)
