import streamlit as st
import json
import pandas as pd

def render():
    st.header("BIM & CAD Export Suite")
    st.write("Export verified design models, metadata reports, and spatial interchange files.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if "generated" in st.session_state:
            concept_data = st.session_state.generated
            json_str = json.dumps(concept_data, indent=2)
            st.download_button(
                label="Download Complete Concept Spec (.json)",
                data=json_str,
                file_name="studiohome_concept.json",
                mime="application/json",
                use_container_width=True
            )
            
            df_export = pd.DataFrame({
                "Parameter": ["Primary Typology", "Site Area", "Estimated Floors", "Grid Spacing", "Structural System", "Estimated Cost", "Embodied Carbon"],
                "Value": [
                    concept_data.get("typology", "Commercial"),
                    st.session_state.get("site_area", 1000.0), 
                    concept_data.get("floors"), 
                    concept_data.get("grid_spacing"), 
                    concept_data.get("structural_system"), 
                    concept_data.get("estimated_cost"),
                    concept_data.get("carbon_score")
                ]
            })
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Executive Summary Report (.csv)",
                data=csv_data,
                file_name="studiohome_summary.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No active design concept found. Generate a concept in the 'AI Brain' panel first.")
        
        mock_dxf = "SECTION\n2\nHEADER\n0\nSECTION\n2\nENTITIES\n0\nLINE\n8\n0\n10\n0.0\n20\n0.0\n30\n0.0\n11\n10.0\n21\n10.0\n31\n0.0\n0\nENDSEC\n0\nEOF"
        st.download_button(
            label="Download OpenBIM / CAD Geometry (.dxf)",
            data=mock_dxf,
            file_name="studiohome_model.dxf",
            mime="application/dxf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
