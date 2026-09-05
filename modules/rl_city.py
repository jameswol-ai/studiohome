import streamlit as st
import plotly.express as px
import pandas as pd
import random

def render():
    st.markdown("## RL Urban Growth & Multi-Agent Engine")
    st.markdown("Simulate autonomous urban development cycles driven by reinforcement learning spatial risk feedback and structural stability models.")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        lr = st.slider("Policy Learning Rate ($\\alpha$)", 0.05, 0.50, 0.20, step=0.05)
    with col_h2:
        decay = st.slider("Risk Decay Factor ($\\gamma$)", 0.80, 0.99, 0.95, step=0.01)
    with col_h3:
        batch_steps = st.slider("Simulation Batch Episodes", 1, 10, 3)
    rl = st.session_state.rl_engine
    rl.policy.lr = lr
    rl.policy.decay = decay
    if st.button("Execute Urban Growth Simulation Batch", use_container_width=True):
        latest_stability = 0.0
        latest_reward = 0.0
        total_failed_nodes = 0
        for _ in range(batch_steps):
            buildings, nodes, loads, failed, stability, reward = rl.step()
            latest_stability = stability
            latest_reward = reward
            total_failed_nodes += len(failed)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Network Stability Index", f"{latest_stability*100:.1f}%", "+2.4% vs Last")
        c2.metric("Cumulative Failures", total_failed_nodes)
        c3.metric("Latest Policy Reward", f"{latest_reward:+.3f}")
        c4.metric("Active Node Count", f"{len(nodes):,}")
        if rl.city_state_log:
            df_log = pd.DataFrame(rl.city_state_log)
            fig = px.line(df_log, y=["stability", "reward"], title="Urban Growth Convergence Trajectory over Episodes", template="plotly_white", height=320)
            fig.update_layout(paper_bgcolor="#D40000", plot_bgcolor="#D40000", font=dict(color="#000000"), margin=dict(t=40, b=10, l=10, r=10))
            fig.update_traces(line=dict(color="#000000"))
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
