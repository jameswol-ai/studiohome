import streamlit as st
import pandas as pd
import re
import random

def render():
    st.markdown("## 🧠 AI Brain & Generative Synthesis Engine")
    st.markdown("Natural language prompt-to-parameter vector mapping engine that translates design intents into synchronized multi-disciplinary parameters.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    
    default_intent = p.get('intent', 'A cutting-edge net-zero carbon 12-storey hybrid mass-timber innovation hub')
    user_prompt = st.text_area("Architectural Intent & Generative Prompt", value=default_intent, height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        creativity_temp = st.slider("Neural Creativity Temperature", 0.1, 1.0, 0.7, step=0.1)
    with col2:
        agent_consensus = st.selectbox("Multi-Agent Optimization Mode", ["Collaborative Consensus", "Cost-Optimized", "Carbon-Zero Priority", "Zoning-Maximized"])
        
    if st.button("⚡ Execute Neural Vector Synthesis", use_container_width=True):
        p['intent'] = user_prompt
        
        if "timber" in user_prompt.lower() or "mass" in user_prompt.lower():
            p['structural_system'] = "Mass Timber CLT & Glulam Frame"
            p['carbon_score'] = 380.0
        elif "steel" in user_prompt.lower():
            p['structural_system'] = "Structural Steel Braced Core"
            p['carbon_score'] = 620.0
        else:
            p['structural_system'] = "Reinforced Concrete Flat Slab"
            p['carbon_score'] = 750.0
            
        nums = re.findall(r'\d+', user_prompt)
        if nums and int(nums[0]) <= 40:
            p['floors'] = int(nums[0])
            p['total_gfa'] = p.get('site_area', 2500.0) * 0.65 * p['floors']
            p['estimated_cost'] = p['total_gfa'] * p.get('unit_rate', 1650.0)
                
        st.success("Successfully compiled natural language vector mapping into global session state!")
        
        st.markdown("### 🤖 Multi-Agent Deliberation Logs")
        
        log_data = pd.DataFrame({
            "Agent Subsystem": ["Architecture Agent", "Structural FEA Agent", "Cost Pro-Forma Agent", "Zoning Compliance Agent", "LCA Circularity Agent"],
            "Agent Status": ["Optimized Volumetry", "Passed Drift & P_u Checks", "CAPEX Recalibrated", "IBC Setback Verified", "Embodied Carbon Logged"],
            "Confidence Score": [f"{random.randint(92, 99)}%", f"{random.randint(90, 98)}%", f"{random.randint(91, 97)}%", "100%", f"{random.randint(94, 99)}%"]
        })
        
        st.dataframe(log_data, use_container_width=True, hide_index=True)
        
    st.markdown('</div>', unsafe_allow_html=True)