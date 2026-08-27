import streamlit as st
import plotly.express as px
import pandas as pd

def render():
    st.markdown("## ⚡ MEP & Building Energy Performance Agent")
    st.markdown("Simulate HVAC loads, energy use intensity (EUI), renewable generation potential, and thermal comfort distributions.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    
    col1, col2, col3 = st.columns(3)
    with col1:
        hvac_system = st.selectbox("HVAC Distribution System", ["VRF with Heat Recovery", "Chilled Beam & DOAS", "Geothermal Ground Source Heat Pump", "All-Air VAV System"])
    with col2:
        pv_coverage = st.slider("BIPV Rooftop Solar Coverage (%)", 0, 100, 75, step=5)
    with col3:
        target_leed = st.selectbox("Target Certification", ["LEED Platinum", "LEED Gold", "WELL Building Standard", "Net-Zero Carbon Certified"], index=0)
        p['energy_rating'] = target_leed
        
    eui = round(75.0 - (pv_coverage * 0.25) - (15.0 if "Geothermal" in hvac_system else 5.0), 1)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Energy Use Intensity (EUI)", f"{eui} kWh/m²/yr", "-42% vs Baseline")
    m2.metric("Annual PV Generation", f"{int(p['total_gfa'] * 0.18 * (pv_coverage/100)):,} kWh", "Renewable Offset")
    m3.metric("Peak Cooling Load", f"{int(p['total_gfa'] * 0.085)} TR", "Optimized")
    m4.metric("Certification Status", target_leed, "Verified Ready")
    
    mep_df = pd.DataFrame({
        "System Domain": ["Heating & Boiler", "Cooling & Chillers", "Ventilation (DOAS)", "Lighting & Plug Loads", "Renewable Generation"],
        "Consumption Share (%)": [15, 30, 25, 20, -35]
    })
    
    fig = px.bar(mep_df, x="System Domain", y="Consumption Share (%)", color="System Domain", title="Annual Energy Balance & Load Distribution", template="plotly_dark", height=320)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)