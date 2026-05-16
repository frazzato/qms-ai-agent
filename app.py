import streamlit as st
import pandas as pd
import time
import random

# ─────────────────────────────────────
# PAGE CONFIGURATION (Must be first)
# ─────────────────────────────────────
st.set_page_config(page_title="QMS System", layout="wide")

# ─────────────────────────────────────
# STATE MANAGEMENT (The Traffic Cop)
# ─────────────────────────────────────
# This ensures the app remembers which page we are on
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# ─────────────────────────────────────
# MOCK DATA
# ─────────────────────────────────────
# Replace this with your actual document loading logic later
doc_data = [
    {"Document ID": "DOC-001", "Title": "Quality Manual", "Status": "Active"},
    {"Document ID": "DOC-002", "Title": "Risk Management Procedure", "Status": "Review Soon"},
    {"Document ID": "DOC-003", "Title": "Internal Audit Report", "Status": "Active"},
]

# ─────────────────────────────────────
# PAGE 1: DASHBOARD
# ─────────────────────────────────────
def render_dashboard(doc_data):
    st.markdown("""
    <style>
    .enterprise-hero {
        padding: 2rem;
        border-radius: 8px;
        background-color: rgba(26, 115, 232, 0.05);
        border: 1px solid rgba(26, 115, 232, 0.2);
        border-left: 6px solid #1a73e8;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 1.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        margin-top: 0;
    }
    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.8;
        max-width: 700px;
        line-height: 1.5;
    }
    .badge {
        display: inline-block;
        background-color: #e6f4ea;
        color: #137333;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        margin-top: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    total = len(doc_data) if doc_data else 0

    st.markdown(f"""
    <div class="enterprise-hero">
        <div class="badge">● SYSTEM ACTIVE</div>
        <h1 class="hero-title">AS9100 Rev D Intelligence Hub</h1>
        <div class="hero-subtitle">
            Your compliance engine is currently managing <strong>{total} controlled documents</strong>. 
            AI modules are continuously monitoring clause coverage, assessing risks, and preparing internal audit data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">System Overview</div>', unsafe_allow_html=True)
    
    def count_status(keyword):
        if not doc_data:
            return 0
        return sum(1 for d in doc_data if keyword.lower() in str(d.get("Status", "")).lower())

    active = count_status("active")
    soon = count_status("review soon")
    overdue = count_status("overdue")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Documents", total)
    m2.metric("Active & Compliant", active, delta="Operational", delta_color="normal")
    m3.metric("Review Imminent", soon, delta="- Action Needed", delta_color="off")
    m4.metric("Overdue Elements", overdue, delta="- High Priority", delta_color="inverse")

    st.write("") 

    st.markdown('<div class="section-header">AI Capabilities</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📋 Gap Analysis")
            st.write("Clause coverage mapping against AS9100 & ISO 9001 requirements.")
            st.write("") 
            if st.button("Launch Analysis", key="btn_gap", type="primary", use_container_width=True):
                st.session_state.active_tab = "AI Application"
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🛠️ CAPA Generator")
            st.write("AI-assisted root cause analysis & corrective action reports.")
            st.write("") 
            if st.button("Open CAPA", key="btn_capa", use_container_width=True):
                st.session_state.active_tab = "AI Application"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### ✅ Audit Checklist")
            st.write("Auto-generated internal audit checklists structured by clause.")
            st.write("") 
            if st.button("Build Checklist", key="btn_audit", use_container_width=True):
                st.session_state.active_tab = "AI Application"
                st.rerun()

    col4, col5, col6 = st.columns(3)
    
    with col4:
        with st.container(border=True):
            st.markdown("### ⚠️ Risk Matrix")
            st.write("Likelihood × severity calculation matrix with AI mitigations.")
            st.write("") 
            if st.button("Assess Risks", key="btn_risk", use_container_width=True):
                st.session_state.active_tab = "AI Application"
                st.rerun()

    with col5:
        with st.container(border=True):
            st.markdown("### 🎓 Smart Training")
            st.write("Generative training modules with automated knowledge checks.")
            st.write("") 
            if st.button("Manage Training", key="btn_train", use_container_width=True):
                st.session_state.active_tab = "Training Hub"
                st.rerun()

    st.write("") 

    st.markdown('<div class="section-header">Document Registry</div>', unsafe_allow_html=True)

    if not doc_data:
        st.info("No documents found in the repository.")
    else:
        df = pd.DataFrame(doc_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Document ID": st.column_config.TextColumn("ID", width="small"),
                "Title":       st.column_config.TextColumn("Document Title", width="large"),
                "Status":      st.column_config.TextColumn("Current Status", width="medium"),
            },
        )

# ─────────────────────────────────────
# PAGE 2: AI APPLICATION (MOCK)
# ─────────────────────────────────────
def render_ai_application():
    st.title("🤖 AI Application Workspace")
    st.info("You have successfully routed to the AI Application page!")
    st.write("Your AI tools (Gap Analysis, CAPA, Audit, Risk) will run here.")
    if st.button("← Back to Dashboard"):
        st.session_state.active_tab = "Dashboard"
        st.rerun()

# ─────────────────────────────────────
# PAGE 3: TRAINING HUB (MOCK)
# ─────────────────────────────────────
def render_training_hub():
    st.title("🎓 Smart Training Hub")
    st.info("You have successfully routed to the Training page!")
    st.write("Your AI generated training modules will appear here.")
    if st.button("← Back to Dashboard"):
        st.session_state.active_tab = "Dashboard"
        st.rerun()

# ─────────────────────────────────────
# MAIN APP ROUTING (The Engine)
# ─────────────────────────────────────
def main():
    # 1. Setup the Sidebar Navigation
    with st.sidebar:
        st.title("☁️ QMS System")
        st.write("---")
        
        # This radio button controls AND reads the session state
        selected = st.radio(
            "Navigation",
            ["Dashboard", "AI Application", "Training Hub"],
            index=["Dashboard", "AI Application", "Training Hub"].index(st.session_state.active_tab),
            label_visibility="hidden"
        )
        
        # If user clicks the sidebar, update state and rerun
        if selected != st.session_state.active_tab:
            st.session_state.active_tab = selected
            st.rerun()

        st.write("---")
        st.caption(f"System Health: **97%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

    # 2. Route to the correct page based on the state
    if st.session_state.active_tab == "Dashboard":
        render_dashboard(doc_data)
    elif st.session_state.active_tab == "AI Application":
        render_ai_application()
    elif st.session_state.active_tab == "Training Hub":
        render_training_hub()

# Run the app
if __name__ == "__main__":
    main()
