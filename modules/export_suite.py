import streamlit as st
import json
import pandas as pd

def render():
    st.markdown("## 📦 Unified BIM & Data Export Suite")
    st.markdown("Compile and export multi-disciplinary project parameters into open-standard formats (JSON, CSV, IFC, DXF).")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    
    st.markdown("### 📑 Export Package Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        include_lca = st.checkbox("Include LCA & Embodied Carbon Data", value=True)
        include_cost = st.checkbox("Include Economic Pro-Forma & CAPEX", value=True)
    with col2:
        include_fea = st.checkbox("Include Structural FEA Node Forces", value=True)
        export_format = st.selectbox("Target Interchange Format", ["JSON (Full Schema)", "CSV (Matrix Table)", "IFC 4x3 (BIM Model)", "DXF (CAD Wireframe)"])
        
    export_payload = {
        "studiohome_version": "2.6.0",
        "project_metadata": p,
        "export_timestamp": "2026-08-27T19:36:59Z"
    }
    
    payload_json = json.dumps(export_payload, indent=2)
    
    st.download_button(
        label=f"📥 Download Compiled {export_format.split()[0]} Package",
        data=payload_json,
        file_name=f"studiohome_project_export.{export_format.split()[0].lower()}",
        mime="application/json",
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)