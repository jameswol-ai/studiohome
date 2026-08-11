import streamlit as st
import random

def render():
    st.header("Civilization Consciousness Monitor")
    st.write("Real-time telemetry tracking collective civic sentiment, pressure gradients, and innovation momentum.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        cs = st.session_state.civilization_state
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Civic Stability", f"{cs['stability']*100:.1f}%")
        c2.metric("Conflict Pressure", f"{cs['conflict']*100:.1f}%")
        c3.metric("Innovation Drive", f"{cs['innovation']*100:.1f}%")
        c4.metric("Cultural Synergy", f"{cs['culture_score']*100:.1f}%")
        
        if st.button("Pulse Consciousness Update", use_container_width=True):
            st.session_state.civilization_state["stability"] = min(1.0, max(0.1, cs['stability'] + random.uniform(-0.05, 0.05)))
            st.session_state.civilization_state["innovation"] = min(1.0, max(0.1, cs['innovation'] + random.uniform(-0.03, 0.06)))
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
