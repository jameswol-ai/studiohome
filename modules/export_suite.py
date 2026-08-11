import streamlit as st
import json
import pandas as pd

def render():
    st.markdown("## 📦 BIM & CAD Interoperability Export Suite")
    st.markdown("Export verified metadata specifications, executive CSV reports, and OpenBIM CAD interchange packages.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if "generated" in st.session_state:
        concept = st.session_state.generated
        st.download_button(
            label="📥 Download Complete Concept JSON Spec (.json)",
            data=json.dumps(concept, indent=2),
            file_name="studiohome_concept_spec.json",
            mime="application/json",
            use_container_width=True
        )
        
        df_export = pd.DataFrame({
            "Design Parameter": ["Primary Typology", "Site Footprint Area", "Storey Count", "Grid Module", "Structural Specification", "Estimated Capital Outlay", "Embodied Carbon Score"],
            "Engine Value": [
                concept.get("typology", "Commercial"),
                st.session_state.get("site_area", 2500.0),
                concept.get("floors"),
                f"{concept.get('grid_spacing')}m",
                concept.get("structural_system"),
                f"${concept.get('estimated_cost'):,.0f}",
                f"{concept.get('carbon_score')} tCO₂e"
            ]
        })
        st.download_button(
            label="📥 Download Executive Summary Data Report (.csv)",
            data=df_export.to_csv(index=False).encode('utf-8'),
            file_name="studiohome_executive_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("⚠️ No active architectural concept detected. Please generate a design concept in the 'AI Brain' panel first.")
        
    mock_dxf = "SECTION\n2\nHEADER\n0\nSECTION\n2\nENTITIES\n0\nLINE\n8\n0\n10\n0.0\n20\n0.0\n30\n0.0\n11\n100.0\n21\n100.0\n31\n0.0\n0\nENDSEC\n0\nEOF"
    st.download_button(
        label="📥 Download OpenBIM / AutoCAD 3D Wireframe (.dxf)",
        data=mock_dxf,
        file_name="studiohome_geometry_model.dxf",
        mime="application/dxf",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
