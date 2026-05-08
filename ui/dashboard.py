# -----------------------------
# CLICKABLE CARDS (3 ONLY)
# -----------------------------
st.markdown("""
<style>
    .pillar-card {
        padding: 20px;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        font-size: 20px;
        text-align: center;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .pillar-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    }
    .audit  { background: #50C878; }
    .train  { background: #F5A623; }
    .master { background: #9B59B6; }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="pillar-card audit">🕵️ Audit Engine</div>', unsafe_allow_html=True)
    if st.button("Go to Audit", key="audit_btn", use_container_width=True):
        st.session_state.active_tab = "Audit"
        st.experimental_rerun()

with col2:
    st.markdown('<div class="pillar-card train">🎓 Training Module</div>', unsafe_allow_html=True)
    if st.button("Go to Training", key="train_btn", use_container_width=True):
        st.session_state.active_tab = "Training"
        st.experimental_rerun()

with col3:
    st.markdown('<div class="pillar-card master">📑 Master List</div>', unsafe_allow_html=True)
    if st.button("Stay on Dashboard", key="master_btn", use_container_width=True):
        st.session_state.active_tab = "Dashboard"
        st.experimental_rerun()



    
