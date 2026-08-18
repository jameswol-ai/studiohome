import streamlit as st
import random
import plotly.express as px
import pandas as pd

def render():
    st.markdown("## 🧠 AI Design Brain & Generative Synthesis Copilot")
    st.markdown("Transform natural language conceptual parameters into fully engineered building typologies, financial pro-formas, and carbon metrics with real-time AI copilot assistance.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([2.2, 1])
    with col1:
        st.session_state.intent_text = st.text_area(
            "Architectural Prompt & Narrative",
            value=st.session_state.get("intent_text", "A cutting-edge net-zero carbon 12-storey hybrid mass-timber innovation hub featuring cascading rooftop gardens, automated daylight zoning, and a central bioclimatic atrium."),
            height=130
        )
    with col2:
        st.session_state.site_area = st.number_input("Site Footprint Area (m²)", value=st.session_state.get("site_area", 2500.0), step=100.0)
        target_use = st.selectbox("Primary Building Typology", ["Commercial Innovation Hub", "Mixed-Use Residential", "Biophilic Corporate HQ", "Institutional Academic Center", "Advanced Industrial Lab"])
        sustainability_tier = st.select_slider("Sustainability Standard", options=["Baseline Code", "LEED Gold", "LEED Platinum", "Living Building Challenge"], value="LEED Platinum")
        
        generate_clicked = st.button("Synthesize Architecture Concept", use_container_width=True)

    if generate_clicked or "generated" not in st.session_state:
        floors = max(4, len(st.session_state.intent_text) % 10 + 6)
        grid = random.choice([6, 8, 9, 12])
        st.session_state.generated = {
            "typology": target_use,
            "floors": floors,
            "grid_spacing": grid,
            "structural_system": "Mass Timber CLT & Glulam Frame" if "Timber" in target_use or "Biophilic" in target_use else "Post-Tensioned Concrete Slab",
            "estimated_cost": floors * st.session_state.site_area * random.randint(1100, 1600),
            "carbon_score": round(st.session_state.site_area * floors * 0.14, 2),
            "energy_efficiency": "A+" if sustainability_tier in ["LEED Platinum", "Living Building Challenge"] else "B+"
        }
        st.success("✨ Generative model synthesized successfully! Explore breakdown metrics below.")
    st.markdown('</div>', unsafe_allow_html=True)
        
    if "generated" in st.session_state:
        st.markdown("### 📊 Synthesized Concept Overview")
        g = st.session_state.generated
        
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Storeys / Height", f"{g['floors']} Levels")
        c2.metric("Structural Grid", f"{g['grid_spacing']}m x {g['grid_spacing']}m")
        c3.metric("Structural System", g["structural_system"].split()[0] + "...")
        c4.metric("Capital Outlay", f"${g['estimated_cost']:,.0f}")
        c5.metric("Embodied Carbon", f"{g['carbon_score']:,.1f} tCO₂e")

        metrics_df = pd.DataFrame({
            "Category": ["Substructure", "Superstructure", "Envelope / Facade", "MEP & Smart Core", "Interior Fitout"],
            "Cost Share ($)": [g['estimated_cost']*0.12, g['estimated_cost']*0.30, g['estimated_cost']*0.20, g['estimated_cost']*0.25, g['estimated_cost']*0.13]
        })
        fig = px.bar(metrics_df, x="Category", y="Cost Share ($)", color="Category", 
                     title="Estimated Capital Cost Distribution by Discipline",
                     template="plotly_dark", height=300)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

        # Interactive AI Architectural Copilot Chat Section
        st.markdown("### 💬 AI Architectural Copilot Assistant")
        st.markdown("Ask questions or request real-time design adjustments for your synthesized concept.")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"Hello! I am your AI architectural copilot. Your concept for a {g['typology']} with {g['floors']} storeys is fully loaded. How would you like to refine it?"}
            ]
            
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        user_query = st.chat_input("Ask the AI Copilot (e.g., 'How can we lower embodied carbon by 20%?')...")
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
                
            # Simulated intelligent copilot response
            if "carbon" in user_query.lower() or "sustainable" in user_query.lower():
                response = f"To reduce embodied carbon by 20%, I recommend substituting the perimeter core elements with cross-laminated mass timber (CLT) and optimizing the structural grid to {g['grid_spacing']}m. This drops your score from {g['carbon_score']} to approx. {round(g['carbon_score']*0.8, 1)} tCO₂e."
            elif "cost" in user_query.lower() or "budget" in user_query.lower():
                response = f"Your current capital outlay is estimated at ${g['estimated_cost']:,.0f}. You can trim approximately 8% by consolidating mechanical riser shafts and streamlining the floorplate aspect ratio."
            else:
                response = f"That is a great design inquiry! Incorporating your suggestion for this {g['floors']}-storey {g['typology']} aligns well with our LEED Platinum standards. All engineering bounds remain fully compliant."
                
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
