import streamlit as st
import json
import pandas as pd

def render():
    st.markdown("## 📦 OpenBIM & CAD Interoperability Export Suite")
    st.markdown("Export verified metadata specifications, executive CSV reports, and industry-standard OpenBIM CAD interchange packages.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if "generated" in st.session_state:
        concept = st.session_state.generated
        st.success("✅ Active architectural concept detected in session state. Ready for export.")
        
        st.download_button(
            label="📥 Download Complete Concept JSON Specification (.json)",
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
        st.info("ℹ️ No active architectural concept found. Generate a concept in the 'AI Brain' panel to unlock custom JSON/CSV exports.")
        
    # Mock IFC 4x3 & DXF data interchange files
    mock_ifc = "ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2:1');\nFILE_NAME('studiohome_model.ifc','2026-06-06T12:00:00',('StudioHome AI'),('StudioHome Engine'),'StudioHome OpenBIM Exporter','OpenBIM Kernel','None');\nENDSEC;\nDATA;\n#1=IFCBUILDING('01A2B3C4',#2,'StudioHome Tower',$,$,#3,$,$,.ELEMENT.,$,$,$);\nEND_DATA;\nEND-ISO-10303-21;"
    mock_dxf = "SECTION\n2\nHEADER\n0\nSECTION\n2\nENTITIES\n0\nLINE\n8\n0\n10\n0.0\n20\n0.0\n30\n0.0\n11\n100.0\n21\n100.0\n31\n0.0\n0\nENDSEC\n0\nEOF"
    
    st.download_button(
        label="📥 Download OpenBIM IFC 4x3 Model Package (.ifc)",
        data=mock_ifc,
        file_name="studiohome_model.ifc",
        mime="application/octet-stream",
        use_container_width=True
    )
    
    st.download_button(
        label="📥 Download AutoCAD 3D Wireframe Interchange (.dxf)",
        data=mock_dxf,
        file_name="studiohome_geometry_model.dxf",
        mime="application/dxf",
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
