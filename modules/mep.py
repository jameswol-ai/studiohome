import streamlit as st

def render():
    st.header("MEP Systems Engine")
    st.write("Size mechanical, electrical, and plumbing distribution trunks based on building occupancy profiles.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        mep_tab1, mep_tab2, mep_tab3 = st.tabs(["Mechanical & HVAC", "Electrical Distribution", "Plumbing & Drainage"])
        with mep_tab1:
            floor_area_mep = st.number_input("Conditioned Floor Area (m²)", value=2500.0, step=100.0)
            occupants = st.number_input("Design Occupancy Count", value=150, step=10)
            cooling_load_kw = round(floor_area_mep * 0.12 + occupants * 0.15, 1)
            airflow_m3h = int(cooling_load_kw * 310)
            
            c1, c2 = st.columns(2)
            c1.metric("Calculated Peak Cooling Load", f"{cooling_load_kw} kW")
            c2.metric("Required Supply Airflow", f"{airflow_m3h:,} m³/h")
        with mep_tab2:
            transformer_kva = int((floor_area_mep * 0.08) + 120)
            st.metric("Recommended Transformer Capacity", f"{transformer_kva} kVA")
            st.write("Primary Distribution Panels:")
            st.json({"Lighting Sub-Panel": "3x 100A 3P", "HVAC Power Center": "1x 400A 3P", "Emergency Life Safety": "1x 250A 3P"})
        with mep_tab3:
            water_demand_lpd = int(occupants * 50)
            st.metric("Estimated Daily Potable Water Demand", f"{water_demand_lpd:,} L/day")
            st.metric("Sanitary Drainage Peak Flow", f"{round(water_demand_lpd * 0.00045, 2)} L/s")
        st.markdown('</div>', unsafe_allow_html=True)
