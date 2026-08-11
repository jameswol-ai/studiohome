import streamlit as st
import random

def render():
    st.header("AI Design Brain")
    st.write("Synthesize complete architectural schemes, layout parameters, and spatial configurations from raw intent.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.session_state.intent_text = st.text_area(
                "Describe your building intent",
                value=st.session_state.get("intent_text", ""),
                height=120,
                placeholder="e.g., A sustainable 6-storey hybrid mass-timber commercial structure with central atrium..."
            )
        with col2:
            st.session_state.site_area = st.number_input(
                "Site area (m²)",
                value=st.session_state.get("site_area", 1000.0),
                min_value=100.0,
                step=50.0
            )
            target_use = st.selectbox("Primary Typology", ["Commercial", "Residential", "Mixed-Use", "Institutional", "Industrial"])
            if st.button("Generate Concept", use_container_width=True):
                floors = max(2, len(st.session_state.intent_text) % 15 + 3)
                grid = random.choice([6, 8, 10])
                st.session_state.generated = {
                    "typology": target_use,
                    "floors": floors,
                    "grid_spacing": grid,
                    "structural_system": "Mass Timber CLT" if target_use == "Residential" else "Reinforced Concrete Frame",
                    "estimated_cost": floors * st.session_state.site_area * random.randint(900, 1400),
                    "carbon_score": round(st.session_state.site_area * floors * 0.18, 2)
                }
                st.success("AI design concept generated successfully.")
        st.markdown('</div>', unsafe_allow_html=True)
            
    if "generated" in st.session_state:
        st.markdown("### Synthesized Concept Overview")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        g = st.session_state.generated
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Storeys", g["floors"])
        m2.metric("Grid Spacing", f"{g['grid_spacing']} m")
        m3.metric("Structure", g["structural_system"])
        m4.metric("Est. Cost", f"${g['estimated_cost']:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
