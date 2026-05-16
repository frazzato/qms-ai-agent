import streamlit as st
import pandas as pd
import time
import random

# ─────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────
st.set_page_config(page_title="QMS System", layout="wide")

# ─────────────────────────────────────
# STATE MANAGEMENT
# ─────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# ─────────────────────────────────────
# YOUR DATA LOADING LOGIC GOES HERE
# ─────────────────────────────────────
# Replace this function with your actual logic that reads your repository!
def get_my_real_documents():
    # Example of what your data structure should look like based on your request:
    return [
        {"ID": "DOC-001", "Title": "Quality Manual", "Revision": "B", "Approval": "J. Smith", "Date": "2023-10-15", "Status": "Active"},
        {"ID": "DOC-002", "Title": "Risk Management", "Revision": "A", "Approval": "A. Doe", "Date": "2023-11-01", "Status": "Review Soon"},
        {"ID": "DOC-003", "Title": "Internal Audit Report", "Revision": "C", "Approval": "M. Lee", "Date": "2024-01-10", "Status": "Active"},
    ]

doc_data = get_my_real_documents()

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
    .hero-title { margin-top: 0; margin-bottom: 0.5rem; font-size: 1.75rem; font-weight: 600; }
    .hero-subtitle { font-size: 1rem; opacity: 0.8; max-width: 700px; line-height: 1.5; }
    .badge {
        display: inline-block; background-color: #e6f4ea; color: #137333;
        padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; font-weight: 600; margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; margin-top: 1rem;
        padding-bottom: 0.5rem; border-bottom: 1px solid rgba(128, 128, 128, 0.2);
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
        if not doc_data: return 0
        return sum(1 for d in doc_data if keyword.lower() in str(d.get("Status", "")).lower())

    active = count_status("active")
    soon = count_status("review")
    overdue = count_status("overdue")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Documents", total)
    m2.metric("Active & Compliant", active, delta="Operational", delta_color="normal")
    m3.metric("Review Imminent", soon, delta="- Action Needed", delta_color="off")
    m4.metric("Overdue Elements", overdue, delta="- High Priority", delta_color="inverse")

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

    # --- FIXED DATA TABLE ---
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
                "ID": st.column_config.TextColumn("Doc ID", width="small"),
                "Title": st.column_config.TextColumn("Document Title", width="large"),
                "Revision": st.column_config.TextColumn("Rev", width="small"),
                "Approval": st.column_config.TextColumn("Approval", width="medium"),
                "Date": st.column_config.TextColumn("Date", width="medium"),
                "Status": st.column_config.TextColumn("Current Status", width="medium"),
            },
        )

# ─────────────────────────────────────
# PAGE 2: AI APPLICATION WORKSPACE
# ─────────────────────────────────────
def render_ai_application():
    st.title("🤖 AI Application Workspace")
    st.write("---")

    col_left, col_right = st.columns([1, 2.5])

    # Left Control Panel
    with col_left:
        st.markdown("### ⚙️ Engine Settings")
        
        # This dropdown lets the user pick which tool they are using on this page
        st.selectbox("Select AI Module", ["Gap Analysis", "CAPA Generator", "Audit Checklist", "Risk Assessment"])
        
        st.write("")
        st.file_uploader("Upload Reference Document (PDF, DOCX)", type=["pdf", "docx"])
        
        st.write("")
        st.text_area("Additional Context / Prompt", placeholder="Enter specific focus areas for the AI...")
        
        st.write("")
        # This is where you will eventually attach your actual Python backend code
        if st.button("Run AI Engine", type="primary", use_container_width=True):
            st.success("AI Engine processing... (Connect your backend logic here!)")

        st.write("")
        st.write("")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    # Right Results Panel
    with col_right:
        st.markdown("### 📊 Output Generation")
        with st.container(border=True, height=500):
            st.info("Awaiting input... Upload a document and click 'Run AI Engine' to generate QMS assets.")
            # Your generated Markdown, dataframes, or AI text will render here

# ─────────────────────────────────────
# PAGE 3: TRAINING HUB
# ─────────────────────────────────────
def render_training_hub():
    st.title("🎓 Smart Training Hub")
    st.write("---")
    st.info("Training module interface goes here.")
    if st.button("← Back to Dashboard"):
        st.session_state.active_tab = "Dashboard"
        st.rerun()

# ─────────────────────────────────────
# MAIN APP ROUTING (The Engine)
# ─────────────────────────────────────
def main():
    with st.sidebar:
        st.title("☁️ QMS System")
        st.write("---")
        
        selected = st.radio(
            "Navigation",
            ["Dashboard", "AI Application", "Training Hub"],
            index=["Dashboard", "AI Application", "Training Hub"].index(st.session_state.active_tab),
            label_visibility="hidden"
        )
        
        if selected != st.session_state.active_tab:
            st.session_state.active_tab = selected
            st.rerun()

        st.write("---")
        st.caption(f"System Health: **{random.randint(95, 99)}%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

    # Route traffic based on the active tab
    if st.session_state.active_tab == "Dashboard":
        render_dashboard(doc_data)
    elif st.session_state.active_tab == "AI Application":
        render_ai_application()
    elif st.session_state.active_tab == "Training Hub":
        render_training_hub()

if __name__ == "__main__":
    main()
