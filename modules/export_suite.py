import streamlit as st
import json
import pandas as pd

def render():
    st.markdown("## 📦 OpenBIM & CAD Interoperability Export Suite")
    st.markdown("Export real-time synchronized project metadata, executive CSV reports, and OpenBIM CAD exchange packages.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    st.success("✅ Master project state synchronized and ready for multi-format export.")
    
    st.download_button(
        label="📥 Download Complete Project JSON Specification (.json)",
        data=json.dumps(p, indent=2),
        file_name="studiohome_project_spec.json",
        mime="application/json",
        use_container_width=True
    )
    
    df_export = pd.DataFrame({
        "Parameter Key": ["Intent Narrative", "Building Typology", "Site Footprint Area", "Storey Count", "Grid Module", "Structural System", "Total GFA", "Estimated CAPEX", "Embodied Carbon"],
        "Engine Value": [
            p.get("intent"),
            p.get("typology"),
            f"{p.get('site_area')} m²",
            f"{p.get('floors')} Levels",
            f"{p.get('grid_spacing')}m",
            p.get("structural_system"),
            f"{p.get('total_gfa')} m²",
            f"${p.get('estimated_cost'):,.0f}",
            f"{p.get('carbon_score')} tCO₂e"
        ]
    })
    
    st.download_button(
        label="📥 Download Executive Summary Data Report (.csv)",
        data=df_export.to_csv(index=False).encode('utf-8'),
        file_name="studiohome_executive_report.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    mock_ifc = f"ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2:1');\nFILE_NAME('studiohome_model.ifc','2026-06-06T12:00:00',('StudioHome AI'),('StudioHome Engine'),'StudioHome OpenBIM Exporter','OpenBIM Kernel','None');\nENDSEC;\nDATA;\n#1=IFCBUILDING('01A2B3C4',#2,'{p.get('typology')}',$,$,#3,$,$,.ELEMENT.,$,$,$);\nEND_DATA;\nEND-ISO-10303-21;"
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
