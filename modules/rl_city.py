import streamlit as st

def render():
    st.header("Reinforcement Learning City Engine")
    st.write("Simulate multi-agent urban development growth cycles using spatial risk feedback loops.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        rl = st.session_state.rl_engine
        if st.button("Execute Urban Growth Step", use_container_width=True):
            buildings, _, _, failed, stability, reward = rl.step()
            c1, c2, c3 = st.columns(3)
            c1.metric("Network Stability Index", round(stability, 3))
            c2.metric("Structural Failures", len(failed))
            c3.metric("Policy Reward", round(reward, 3))
            st.json(buildings)
        st.markdown('</div>', unsafe_allow_html=True)
