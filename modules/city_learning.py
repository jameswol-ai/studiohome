import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.markdown("## 📈 City Learning Curve & Reward Analytics")
    st.markdown("Track the cumulative optimization trajectory and reward convergence of the multi-agent urban policy network.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    rl = st.session_state.rl_engine
    if rl.history:
        fig = px.line(y=rl.history, labels={"index": "Simulation Episode", "value": "Policy Reward"}, 
                      title="Cumulative Policy Convergence Curve", template="plotly_dark", height=320)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ No learning history available yet. Execute simulation steps in the 'RL City' panel to initialize telemetry.")
    st.markdown('</div>', unsafe_allow_html=True)
