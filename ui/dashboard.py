import streamlit as st
import pandas as pd
import time
import random

def render_dashboard(doc_data):

    # ─────────────────────────────────────
    # SYSTEM HEALTH + LAST AI SYNC
    # ─────────────────────────────────────
    health_score = random.randint(82, 99)

    h1, h2, h3 = st.columns([2, 1, 1])
    with h1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);
                    border-radius:12px; padding:1.2rem 1.5rem; color:#e2e8f0;">
            <div style="font-size:0.78rem; font-weight:600; text-transform:uppercase;
                        letter-spacing:0.05em; color:#94a3b8; margin-bottom:0.4rem;">
                System Health
            </div>
            <div style="display:flex; align-items:center; gap:1rem;">
                <div style="font-size:2rem; font-weight:700; color:{'#22c55e' if health_score >= 90 else '#f59e0b'};">
                    {health_score}%
                </div>
                <div style="flex:1; background:#334155; border-radius:6px; height:10px; overflow:hidden;">
                    <div style="width:{health_score}%; height:100%;
                                background:linear-gradient(90deg,#22c55e,#3b82f6);
                                border-radius:6px; transition:width 0.5s ease;">
                    </div>
                </div>
            </div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:0.5rem;">
                Last AI Sync: {time.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with h2:
        st.markdown(f"""
        <div style="background:#fff; border:1px solid #e2e8f0; border-top:3px solid #22c55e;
                    border-radius:12px; padding:1.2rem; text-align:center;
