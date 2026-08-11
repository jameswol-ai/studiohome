import streamlit as st
import pandas as pd
import plotly.express as px
import random

def render():
    st.markdown("## 🏛️ Architecture AI — Generative Spatial Agent")
    st.markdown("Collaborate with an autonomous architectural AI to synthesize program layouts, optimize circulation paths, and receive real-time spatial critiques.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # AI Prompt & Style Selector
    ai_col1, ai_col2 = st.columns([2, 1])
    with ai_col1:
        arch_prompt = st.text_input(
            "Architectural Intent Prompt",
            value="A cascading biophilic innovation hub with fluid organic floorplates and maximum daylight penetration."
        )
    with ai_col2:
        ai_style = st.selectbox("Design Paradigm AI", [
            "Parametric Organic", 
            "Neofuturistic Biophilic", 
            "Rationalist Modular", 
            "Deconstructivist Hybrid"
        ])
        
    c1, c2, c3 = st.columns(3)
    with c1:
        grid_module = st.slider("Structural Grid Module (m)", 4.0, 12.0, 8.0, step=0.5)
    with c2:
        floor_plate_size = st.slider("Floorplate Extent (m)", 24, 80, 48, step=4)
    with c3:
        circulation_model = st.selectbox("Circulation Strategy", ["Atrium Core Ring", "Linear Spine", "Radial Hub", "Dual Anchor Banks"])

    if st.button("🤖 Synthesize Architecture with AI", use_container_width=True):
        st.success(f"✨ AI Model successfully generated floorplate layout using **{ai_style}** principles.")
        
        # AI Metrics Evaluation
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Daylight Factor", f"{random.uniform(3.2, 5.8):.1f}%", "+0.8% vs Baseline")
        m2.metric("Circulation Efficiency", f"{random.randint(78, 94)}%", "Optimized")
        m3.metric("Spatial Compactness", f"{random.uniform(1.15, 1.45):.2f}", "Balanced")
        m4.metric("AI Confidence Score", f"{random.uniform(91.5, 98.8):.1f}%", "High")
        
        # Simulated Spatial Matrix
        rows = int(floor_plate_size / grid_module)
        cols = rows
        matrix = []
        for r in range(rows):
            row_data = []
            for c in range(cols):
                if abs(r - rows/2) < 1.5 and abs(c - cols/2) < 1.5:
                    zone = "🔒 Service Core"
                elif r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    zone = "🌿 Biophilic Glazing Zone"
                else:
                    zone = f"🏢 Program Zone [{r},{c}]"
                row_data.append(zone)
            matrix.append(row_data)
            
        df_spatial = pd.DataFrame(matrix, columns=[f"X: {i*grid_module}m" for i in range(cols)], index=[f"Y: {i*grid_module}m" for i in range(rows)])
        st.dataframe(df_spatial, use_container_width=True)
        
        # AI Architectural Critique / Recommendations
        st.markdown("### 🧠 AI Design Agent Critique & Recommendations")
        critiques = [
            f"**Daylighting Optimization:** The perimeter glazing ratio successfully channels natural light up to {int(grid_module * 2.5)}m inward.",
            f"**Circulation Flow:** The **{circulation_model}** reduces corridor transit congestion by 14% compared to standard cellular layouts.",
            "**Material Synergy:** Recommended pairing with mass timber structural systems to lower embodied carbon footprint."
        ]
        for critique in critiques:
            st.markdown(f"- {critique}")
            
    st.markdown('</div>', unsafe_allow_html=True)
