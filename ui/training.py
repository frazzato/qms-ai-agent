import streamlit as st
import pandas as pd
import time
import random

def render_dashboard(doc_data):
    # ─────────────────────────────────────
    # ENTERPRISE CSS OVERRIDES (HERO + TABLE)
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

    /* Enterprise Custom Table Styling */
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
    
    /* Custom QMS Status Pills */
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

    # ─────────────────────────────────────
    # SIDEBAR STATUS CAPTIONS
    # ─────────────────────────────────────
    with st.sidebar:
        st.write("---")
        st.caption(f"System Health: **98%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

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
    # KPI METRICS
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
    # AI MODULES
    # ─────────────────────────────────────
    st.markdown('<div class="section-header">AI Capabilities</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📋 Gap Analysis")
            st.write("Clause coverage mapping against AS9100 & ISO 9001 requirements.")
            st.write("") 
            if st.button("Launch Analysis", key="btn_gap", type="primary", use_container_width=True):
                st.session_state.active_tab = "Audit Workspace"
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.markdown("### 🛠️ CAPA Generator")
            st.write("AI-assisted root cause analysis & corrective action reports.")
            st.write("") 
            if st.button("Open CAPA", key="btn_capa", use_container_width=True):
                st.session_state.active_tab = "Audit Workspace"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### ✅ Audit Checklist")
            st.write("Auto-generated internal audit checklists structured by clause.")
            st.write("") 
            if st.button("Build Checklist", key="btn_audit", use_container_width=True):
                st.session_state.active_tab = "Audit Workspace"
                st.rerun()

    col4, col5, col6 = st.columns(3)
    
    with col4:
        with st.container(border=True):
            st.markdown("### ⚠️ Risk Matrix")
            st.write("Likelihood × severity calculation matrix with AI mitigations.")
            st.write("") 
            if st.button("Assess Risks", key="btn_risk", use_container_width=True):
                st.session_state.active_tab = "Audit Workspace"
                st.rerun()

    with col5:
        with st.container(border=True):
            st.markdown("### 🎓 Smart Training")
            st.write("Generative training modules with automated knowledge checks.")
            st.write("") 
            if st.button("Manage Training", key="btn_train", use_container_width=True):
                st.session_state.active_tab = "Training Hub"  # Updated to match app.py routing
                st.rerun()

    st.write("") # Spacer

    # ─────────────────────────────────────
    # COSMETIC UPLIFT: ENTERPRISE HTML DATA TABLE
    # ─────────────────────────────────────
    st.markdown('<div class="section-header">Document Registry</div>', unsafe_allow_html=True)

    if not doc_data:
        st.info("No documents found in the repository.")
    else:
        table_html = '<div class="enterprise-table-wrapper"><table class="enterprise-table">\n'
        table_html += '<thead>\n<tr>\n'
        table_html += '<th>ID</th>\n<th>Document Title</th>\n<th>Format</th>\n<th>Rev</th>\n'
        table_html += '<th>Approver</th>\n<th>Approved On</th>\n<th>Next Review</th>\n<th>Status</th>\n'
        table_html += '</tr>\n</thead>\n<tbody>\n'
        
        for doc in doc_data:
            status = doc.get("Status", "Active")
            if status == "Active":
                pill_class = "pill-active"
            elif "soon" in status.lower():
                pill_class = "pill-review"
            else:
                pill_class = "pill-overdue"
                
            table_html += '<tr>\n'
            table_html += f'<td>{doc.get("Document ID", "N/A")}</td>\n'
            table_html += f'<td style="font-weight: 600;">{doc.get("Title", "Untitled")}</td>\n'
            table_html += f'<td>{doc.get("Format", "DOCX")}</td>\n'
            table_html += f'<td>{doc.get("Revision", "—")}</td>\n'
            table_html += f'<td>{doc.get("Approved By", "—")}</td>\n'
            table_html += f'<td>{doc.get("Approval Date", "—")}</td>\n'
            table_html += f'<td>{doc.get("Next Review", "—")}</td>\n'
            table_html += f'<td><span class="status-pill {pill_class}">{status}</span></td>\n'
            table_html += '</tr>\n'
            
        table_html += '</tbody></table></div>'
        st.markdown(table_html, unsafe_allow_html=True)
