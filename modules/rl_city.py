import streamlit as st
import plotly.express as px
import pandas as pd

def render():
    st.markdown("## 🏙️ Reinforcement Learning Urban Growth Engine")
    st.markdown("Simulate multi-agent urban development cycles driven by spatial risk feedback and structural stability models.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    rl = st.session_state.rl_engine
    
    if st.button("🏗️ Execute Urban Growth Simulation Step", use_container_width=True):
        buildings, _, _, failed, stability, reward = rl.step()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Network Stability Index", f"{stability*100:.1f}%")
        c2.metric("Structural Failures", len(failed))
        c3.metric("Policy Reward Score", f"{reward:+.3f}")
        
        st.json(buildings)
        
        if rl.city_state_log:
            df_log = pd.DataFrame(rl.city_state_log)
            fig = px.line(df_log, y=["stability", "reward"], title="Urban Growth Convergence Trajectory", template="plotly_dark", height=280)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
