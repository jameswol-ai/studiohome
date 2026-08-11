import streamlit as st
import numpy as np
import pandas as pd

def render():
    st.header("Inter-District Diplomacy Network")
    st.write("Manage trade treaties, territorial pacts, and diplomatic trust matrices between regional factions.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        nations = ["North District", "Metro Core", "East Port", "Silicon Valley", "South Eco-Zone"]
        matrix = np.random.uniform(0.2, 1.0, (len(nations), len(nations)))
        np.fill_diagonal(matrix, 1.0)
        df_diplomacy = pd.DataFrame(matrix, columns=nations, index=nations)
        st.dataframe(df_diplomacy, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
