import streamlit as st
import pandas as pd
import time

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
    .enterprise-table-wrapper {
        width: 100%;
        overflow-x: auto;
        border-radius: 8px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    .enterprise-table {
        width: 100%;
        border-collapse: collapse;
        font-family: inherit;
        font-size: 0.88rem;
        text-align: left;
    }
    .enterprise-table th {
        background-color: rgba(26, 115, 232, 0.08);
        color: #1a73e8;
        font-weight: 600;
        padding: 12px 16px;
        border-bottom: 2px solid rgba(26, 115, 232, 0.2);
        white-space: nowrap;
    }
    .enterprise-table td {
        padding: 12px 16px;
        border-bottom: 1px solid rgba(128, 128, 128, 0.1);
        color: inherit;
        vertical-align: middle;
    }
    .enterprise-table tr:hover {
        background-color: rgba(128, 128, 128, 0.05);
    }
    .status-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    .pill-active { background-color: #e6f4ea; color: #137333; }
    .pill-review { background-color: #fef7e0; color: #b06000; }
    .pill-overdue { background-color: #fce8e6; color: #c5221f; }
    </style>
    """, unsafe_allow_html=True)

    total = len(doc_data) if doc_data else 0

    with st.sidebar:
        st.write("---")
        st.caption("System Health: **98%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

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
        if not doc_data: return 0
        return sum(1 for d in doc_data if keyword.lower() in str(d.get("Status", "")).lower())

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Documents", total)
    m2.metric("Active & Compliant", count_status("active"), delta="Operational", delta_color="normal")
    m3.metric("Review Imminent", count_status("review soon"), delta="- Action Needed", delta_color="off")
    m4.metric("Overdue Elements", count_status("overdue"), delta="- High Priority", delta_color="inverse")

    st.markdown('<div class="section-header">AI Capabilities</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📋 Gap Analysis")
            st.write("Clause coverage mapping against AS9100 & ISO 9001 requirements.")
            st.write("") 
            if st.button("Launch Analysis", key="btn_gap", type="primary", use_container_width=True):
                st.session_state.active_tab = "AI Capabilities"
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🛠️ CAPA Generator")
            st.write("AI-assisted root cause analysis & corrective action reports.")
            st.write("") 
            if st.button("Open CAPA", key="btn_capa", use_container_width=True):
                st.session_state.active_tab = "AI Capabilities"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### ✅ Audit Checklist")
            st.write("Auto-generated internal audit checklists structured by clause.")
            st.write("") 
            if st.button("Build Checklist", key="btn_audit", use_container_width=True):
                st.session_state.active_tab = "AI Capabilities"
                st.rerun()

    col4, col5, col6 = st.columns(3)
    with col4:
        with st.container(border=True):
            st.markdown("### ⚠️ Risk Matrix")
            st.write("Likelihood × severity calculation matrix with AI mitigations.")
            st.write("") 
            if st.button("Assess Risks", key="btn_risk", use_container_width=True):
                st.session_state.active_tab = "AI Capabilities"
                st.rerun()

    with col5:
        with st.container(border=True):
            st.markdown("### 🎓 Smart Training")
            st.write("Generative training modules with automated knowledge checks.")
            st.write("") 
            if st.button("Manage Training", key="btn_train", use_container_width=True):
                st.session_state.active_tab = "Training Hub"
                st.rerun()

    st.markdown('<div class="section-header">Document Registry</div>', unsafe_allow_html=True)
    if not doc_data:
        st.info("No documents found in the repository.")
    else:
        table_html = '<div class="enterprise-table-wrapper"><table class="enterprise-table"><thead><tr><th>ID</th><th>Document Title</th><th>Format</th><th>Rev</th><th>Approver</th><th>Approved On</th><th>Next Review</th><th>Status</th></tr></thead><tbody>'
        for doc in doc_data:
            status = doc.get("Status", "Active")
            pill_class = "pill-active" if status == "Active" else "pill-review" if "soon" in status.lower() else "pill-overdue"
            table_html += f'<tr><td>{doc.get("Document ID", "N/A")}</td><td style="font-weight: 600;">{doc.get("Title", "Untitled")}</td><td>{doc.get("Format", "DOCX")}</td><td>{doc.get("Revision", "—")}</td><td>{doc.get("Approved By", "—")}</td><td>{doc.get("Approval Date", "—")}</td><td>{doc.get("Next Review", "—")}</td><td><span class="status-pill {pill_class}">{status}</span></td></tr>'
        st.markdown(table_html + '</tbody></table></div>', unsafe_allow_html=True)
