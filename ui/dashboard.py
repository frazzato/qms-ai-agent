import streamlit as st
import pandas as pd
import time
import random

def render_dashboard(doc_data):
    # ─────────────────────────────────────
    # ENTERPRISE CSS OVERRIDES
    # ─────────────────────────────────────
    st.markdown("""
    <style>
    /* Clean Enterprise Hero Banner */
    .enterprise-hero {
        padding: 2rem;
        border-radius: 8px;
        background-color: rgba(26, 115, 232, 0.05); /* Google Blue with low opacity */
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
        background-color: #e6f4ea; /* Google Green light */
        color: #137333; /* Google Green dark */
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Clean formatting for subheaders */
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

    # ─────────────────────────────────────
    # LEFT NAVIGATION (MOBILE RESPONSIVE)
    # ─────────────────────────────────────
    with st.sidebar:
        st.title("☁️ QMS System")
        st.write("---")
        
        # Enterprise-style left navigation using native radio buttons
        nav_selection = st.radio(
            "Navigation",
            ["Dashboard", "Audit Workspace", "CAPA Management", "Risk Matrices", "Training Hub"],
            label_visibility="hidden"
        )
        
        st.write("---")
        st.caption(f"System Health: **{random.randint(95, 99)}%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

    # If the user clicks something else in the sidebar, we can route them.
    # For now, we will assume they are on the Dashboard.
    if nav_selection != "Dashboard":
        st.info(f"Navigating to {nav_selection}... (Connect your routing logic here)")
        return

    # ─────────────────────────────────────
    # HERO SECTION
    # ─────────────────────────────────────
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

    # ─────────────────────────────────────
    # KPI METRICS (Streamlit Native)
    # ─────────────────────────────────────
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

    st.write("") # Spacer

    # ─────────────────────────────────────
    # AI MODULES (Enterprise Cards)
    # ─────────────────────────────────────
    st.markdown('<div class="section-header">AI Capabilities</div>', unsafe_allow_html=True)

    # Row 1 of modules
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📋 Gap Analysis")
            st.write("Clause coverage mapping against AS9100 & ISO 9001 requirements.")
            st.write("") # Spacer
            if st.button("Launch Analysis", key="btn_gap", type="primary", use_container_width=True):
                st.success("Routing to Gap Analysis...")
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🛠️ CAPA Generator")
            st.write("AI-assisted root cause analysis & corrective action reports.")
            st.write("") 
            if st.button("Open CAPA", key="btn_capa", use_container_width=True):
                st.success("Routing to CAPA...")

    with col3:
        with st.container(border=True):
            st.markdown("### ✅ Audit Checklist")
            st.write("Auto-generated internal audit checklists structured by clause.")
            st.write("") 
            if st.button("Build Checklist", key="btn_audit", use_container_width=True):
                st.success("Routing to Checklists...")

    # Row 2 of modules
    col4, col5, col6 = st.columns(3)
    
    with col4:
        with st.container(border=True):
            st.markdown("### ⚠️ Risk Matrix")
            st.write("Likelihood × severity calculation matrix with AI mitigations.")
            st.write("") 
            if st.button("Assess Risks", key="btn_risk", use_container_width=True):
                st.success("Routing to Risk Matrix...")

    with col5:
        with st.container(border=True):
            st.markdown("### 🎓 Smart Training")
            st.write("Generative training modules with automated knowledge checks.")
            st.write("") 
            if st.button("Manage Training", key="btn_train", use_container_width=True):
                st.success("Routing to Training...")
                
    with col6:
        # Empty column for grid alignment, or add a 6th tool here!
        pass 

    st.write("") # Spacer

    # ─────────────────────────────────────
    # DATA TABLE (Document Register)
    # ─────────────────────────────────────
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
