import streamlit as st
import plotly.express as px
import pandas as pd
import random

def render():
    st.markdown("## Civilization Consciousness & Neural Pulse Monitor")
    st.markdown("Real-time telemetry tracking collective civic sentiment, pressure gradients, cultural synergy, and neural innovation momentum.")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    cs = st.session_state.civilization_state
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Civic Stability", f"{cs['stability']*100:.1f}%", "Optimal")
    c2.metric("Conflict Pressure", f"{cs['conflict']*100:.1f}%", "Controlled")
    c3.metric("Innovation Drive", f"{cs['innovation']*100:.1f}%", "Surging")
    c4.metric("Cultural Synergy", f"{cs['culture_score']*100:.1f}%", "High")
    radar_df = pd.DataFrame({"Metric": ["Civic Stability", "Innovation Drive", "Cultural Synergy", "Resource Resilience", "Diplomatic Trust"], "Score": [cs['stability'], cs['innovation'], cs['culture_score'], 0.85, 0.79]})
    fig = px.line_polar(radar_df, r="Score", theta="Metric", line_close=True, range_r=[0, 1], title="Collective Civilization Equilibrium Radar", template="plotly_white", height=340)
    fig.update_traces(fill="toself", line_color="#000000")
    fig.update_layout(paper_bgcolor="#D40000", plot_bgcolor="#D40000", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    if st.button("Pulse Consciousness Synchronization & Harmonization", use_container_width=True):
        st.session_state.civilization_state["stability"] = min(1.0, max(0.3, cs['stability'] + random.uniform(-0.02, 0.06)))
        st.session_state.civilization_state["innovation"] = min(1.0, max(0.3, cs['innovation'] + random.uniform(0.01, 0.08)))
        st.session_state.civilization_state["conflict"] = max(0.05, min(0.5, cs['conflict'] + random.uniform(-0.05, 0.02)))
        st.success("Consciousness matrix successfully synchronized across all district nodes!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
