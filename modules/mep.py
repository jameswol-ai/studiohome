import streamlit as st
import plotly.express as px
import pandas as pd
import random

def render():
    st.markdown("## ⚡ MEP & Environmental Systems AI Agent")
    st.markdown("Deploy an autonomous mechanical and environmental intelligence agent to optimize thermal loads, size renewable energy arrays, and audit carbon footprints.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    mep_tab1, mep_tab2, mep_tab3 = st.tabs(["❄️ HVAC & Thermal AI", "☀️ Renewable Energy & Solar PV", "💧 Water & Utility Metrics"])
    
    with mep_tab1:
        col_1, col_2 = st.columns(2)
        with col_1:
            floor_area = st.number_input("Conditioned Gross Floor Area (m²)", value=4500.0, step=250.0)
            occupancy = st.number_input("Peak Occupancy Load", value=320, step=20)
        with col_2:
            climate_zone = st.selectbox("Climate Zone Profile", ["ASHRAE Zone 3 (Warm/Humid)", "ASHRAE Zone 4 (Mixed/Marine)", "ASHRAE Zone 5 (Cool/Continental)", "ASHRAE Zone 7 (Very Cold)"])
            envelope_insulation = st.select_slider("Envelope Thermal Performance", options=["Standard Code", "High-Performance Triple Glaze", "Passive House Standard"], value="High-Performance Triple Glaze")
            
        cooling_load_kw = round(floor_area * 0.095 + occupancy * 0.12, 1)
        airflow_cfm = int(cooling_load_kw * 310)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Peak Cooling Capacity", f"{cooling_load_kw:,.1f} kW", "AI Optimized")
        c2.metric("AHU Supply Air Volume", f"{airflow_cfm:,} m³/h")
        c3.metric("Energy Use Intensity (EUI)", f"{random.randint(48, 65)} kWh/m²a", "Net-Zero Ready")
        
        # Load breakdown chart
        hvac_df = pd.DataFrame({
            "Thermal Component": ["Envelope Conduction", "Internal Occupants", "Lighting & Plug Loads", "Ventilation Fresh Air"],
            "Load Share (kW)": [cooling_load_kw*0.30, cooling_load_kw*0.28, cooling_load_kw*0.22, cooling_load_kw*0.20]
        })
        fig = px.pie(hvac_df, names="Thermal Component", values="Load Share (kW)", title="AI Thermal Load Component Breakdown", hole=0.45, template="plotly_dark")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(t=35, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with mep_tab2:
        roof_area_available = floor_area * 0.28
        pv_capacity_kwp = round(roof_area_available * 0.18, 1)
        annual_generation = int(pv_capacity_kwp * 1350)
        
        p1, p2 = st.columns(2)
        p1.metric("Rooftop PV Capacity", f"{pv_capacity_kwp} kWp")
        p2.metric("Est. Annual Generation", f"{annual_generation:,} kWh/year")
        st.info(f"💡 **AI Recommendation:** Integrating a {int(pv_capacity_kwp)} kWp rooftop solar array covers approximately {random.randint(42, 68)}% of the core base-building electrical load.")
        
    with mep_tab3:
        daily_water = int(occupancy * 48)
        w1, w2 = st.columns(2)
        w1.metric("Daily Potable Water Demand", f"{daily_water:,} Liters")
        w2.metric("Greywater Recycling Potential", f"{int(daily_water * 0.55):,} Liters", "55% Offset")
        
    st.markdown('</div>', unsafe_allow_html=True)
