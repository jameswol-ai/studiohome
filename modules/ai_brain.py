import streamlit as st
import random
import plotly.express as px
import pandas as pd

def render():
    st.markdown("## 🧠 AI Design Brain & Generative Synthesis")
    st.markdown("Transform natural language parameters into a unified project specification that instantly drives all downstream engineering modules.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([2.2, 1])
    with col1:
        intent = st.text_area(
            "Architectural Prompt & Narrative",
            value=st.session_state.project["intent"],
            height=130
        )
    with col2:
        site_area = st.number_input("Site Footprint Area (m²)", value=st.session_state.project["site_area"], step=100.0)
        target_use = st.selectbox("Primary Building Typology", ["Commercial Innovation Hub", "Mixed-Use Residential", "Biophilic Corporate HQ", "Institutional Academic Center", "Advanced Industrial Lab"], index=0)
        sustainability_tier = st.select_slider("Sustainability Standard", options=["Baseline Code", "LEED Gold", "LEED Platinum", "Living Building Challenge"], value="LEED Platinum")
        
        generate_clicked = st.button("Synthesize & Broadcast to Ecosystem", use_container_width=True)

    if generate_clicked:
        floors = max(4, len(intent) % 8 + 6)
        grid = random.choice([6, 8, 9, 12])
        struct = "Mass Timber CLT & Glulam Frame" if "Timber" in target_use or "Biophilic" in target_use else "Post-Tensioned Concrete Slab"
        cost_val = floors * site_area * random.randint(1200, 1600)
        carbon_val = round(site_area * floors * 0.13, 2)
        total_gfa = site_area * floors
        
        # WRITE TO SHARED GLOBAL PROJECT STATE
        st.session_state.project = {
            "intent": intent,
            "typology": target_use,
            "site_area": site_area,
            "floors": floors,
            "grid_spacing": float(grid),
            "structural_system": struct,
            "live_load": 4.0,
            "unit_rate": cost_val / total_gfa,
            "total_gfa": total_gfa,
            "estimated_cost": cost_val,
            "carbon_score": carbon_val,
            "energy_rating": sustainability_tier
        }
        st.success("✨ Concept synthesized and broadcast successfully across all studiohome modules!")
    st.markdown('</div>', unsafe_allow_html=True)
        
    p = st.session_state.project
    st.markdown("### 📊 Synchronized Project Metrics")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Storeys / Height", f"{p['floors']} Levels")
    c2.metric("Structural Grid", f"{p['grid_spacing']}m x {p['grid_spacing']}m")
    c3.metric("Structural System", p["structural_system"].split()[0] + "...")
    c4.metric("Capital Outlay", f"${p['estimated_cost']:,.0f}")
    c5.metric("Embodied Carbon", f"{p['carbon_score']:,.1f} tCO₂e")

    metrics_df = pd.DataFrame({
        "Category": ["Substructure", "Superstructure", "Envelope / Facade", "MEP & Smart Core", "Interior Fitout"],
        "Cost Share ($)": [p['estimated_cost']*0.12, p['estimated_cost']*0.30, p['estimated_cost']*0.20, p['estimated_cost']*0.25, p['estimated_cost']*0.13]
    })
    fig = px.bar(metrics_df, x="Category", y="Cost Share ($)", color="Category", 
                 title="Estimated Capital Cost Distribution (Synced with Cost Module)",
                 template="plotly_dark", height=300)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
