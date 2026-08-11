import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def render():
    st.markdown("## 🤝 Inter-District Diplomacy & Trust Network")
    st.markdown("Manage bilateral trade treaties, territorial compacts, and geopolitical trust matrices between regional districts.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    nations = ["North Tech District", "Metro Core Hub", "East Maritime Port", "Silicon Eco-Valley", "South Resilient Zone"]
    matrix = np.random.uniform(0.3, 1.0, (len(nations), len(nations)))
    np.fill_diagonal(matrix, 1.0)
    
    df_diplomacy = pd.DataFrame(matrix, columns=nations, index=nations)
    
    fig = px.imshow(df_diplomacy, text_auto=True, title="Inter-District Diplomatic Trust Matrix", template="plotly_dark", color_continuous_scale="Blues")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=350, margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
