import streamlit as st
import pandas as pd

def render():
    st.header("City Learning Curve Analytics")
    st.write("Track the cumulative optimization trajectory and reward convergence of the urban policy engine.")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        rl = st.session_state.rl_engine
        if rl.history:
            st.line_chart(pd.Series(rl.history, name="Policy Reward Convergence"))
        else:
            st.info("Run urban simulation steps from the 'RL City' panel to generate learning trajectory records.")
        st.markdown('</div>', unsafe_allow_html=True)
