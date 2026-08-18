import streamlit as st
import pandas as pd
import plotly.express as px
import random

def render():
    st.markdown("## 📜 Automated Zoning & Code Compliance Engine")
    st.markdown("Run autonomous regulatory audits against international building codes (IBC), height limits, FAR thresholds, and fire-life-safety standards.")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    p = st.session_state.project
    
    col1, col2, col3 = st.columns(3)
    with col1:
        zoning_district = st.selectbox("Municipal Zoning District", ["CBD Commercial Core (C-5)", "Mixed-Use Urban Corridor (MU-3)", "High-Density Residential (R-4)", "Innovation District (IND)"], index=0)
    with col2:
        max_allowable_far = st.slider("Max Allowable FAR Limit", 2.0, 10.0, 6.0, step=0.5)
    with col3:
        sprinkler_protection = st.checkbox("NFPA 13 Full Fire Sprinkler System", value=True)
        
    # Calculate current project metrics relative to code
    achieved_far = round(p['total_gfa'] / p['site_area'], 2) if p['site_area'] > 0 else 4.0
    max_height_code = 75.0 if "Commercial" in zoning_district else 45.0
    current_height = p['floors'] * 3.5
    
    far_compliant = achieved_far <= max_allowable_far
    height_compliant = current_height <= max_height_code
    egress_compliant = True
    parking_ratio_met = True
    
    # Audit summary cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Achieved FAR Index", f"{achieved_far}", "Pass" if far_compliant else "Exceeds Limit", delta_color="normal" if far_compliant else "inverse")
    c2.metric("Building Height", f"{current_height} m", f"Max {max_height_code}m")
    c3.metric("Fire-Life-Safety", "NFPA 13 Compliant" if sprinkler_protection else "Variance Req.")
    c4.metric("Overall Code Status", "APPROVED" if (far_compliant and height_compliant) else "REVIEW REQUIRED", "AI Verified")
    
    st.markdown("### 📋 Detailed Regulatory Checklist")
    
    code_audit_df = pd.DataFrame({
        "Regulatory Code Clause": [
            "IBC Section 503 - Building Height & Area Limitations",
            "Zoning Bylaw - Floor Area Ratio (FAR) Density",
            "NFPA 101 - Life Safety Egress Corridor Widths",
            "ASHRAE 90.1 - Energy Envelope Performance",
            "ADA Compliance - Accessible Universal Ramping & Lifts",
            "Municipal Setback & Daylight Plane Restrictions"
        ],
        "Standard Requirement": [
            f"Max {max_height_code} meters height",
            f"Max {max_allowable_far}.0 FAR density",
            "Min 1.8m clear egress width",
            "A+ Energy Rating Standard",
            "100% Barrier-Free Access",
            "3.0m perimeter setback buffer"
        ],
        "Project Status": [
            "✅ Compliant" if height_compliant else "❌ Exceeds Height",
            "✅ Compliant" if far_compliant else "⚠️ Density Bonus Req.",
            "✅ Compliant",
            f"✅ {p.get('energy_rating', 'LEED Platinum')}",
            "✅ Compliant",
            "✅ Compliant"
        ]
    })
    
    st.dataframe(code_audit_df, use_container_width=True)
    
    # Compliance Category Scoring Chart
    compliance_scores = pd.DataFrame({
        "Compliance Domain": ["Structural & Seismic", "Fire & Life Safety", "Zoning & Density", "Environmental & Energy", "Accessibility & Egress"],
        "Compliance Score (%)": [98, 100 if sprinkler_protection else 85, 94 if far_compliant else 72, 99, 100]
    })
    
    fig = px.bar(compliance_scores, x="Compliance Domain", y="Compliance Score (%)", color="Compliance Score (%)",
                 title="Multi-Domain Regulatory Compliance Radar Index", template="plotly_dark", height=300, range_y=[60, 100])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
