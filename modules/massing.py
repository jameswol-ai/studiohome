import streamlit as st
import pandas as pd
import random

def render():
    st.header("Spatial Massing Viewer")
    st.write("Inspect volumetric massing blocks and proportional height distributions across the project site.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        num_blocks = st.slider("Active Massing Blocks", 1, 10, 5)
        massing_data = []
        for i in range(num_blocks):
            massing_data.append({
                "Block ID": f"Block-{chr(65+i)}",
                "Footprint Area (m²)": random.randint(200, 900),
                "Height (m)": random.randint(12, 65),
                "Floor Count": random.randint(4, 20),
                "Program Type": random.choice(["Residential", "Office", "Retail", "Amenity"])
            })
        df_massing = pd.DataFrame(massing_data)
        st.dataframe(df_massing, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
