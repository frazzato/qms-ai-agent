import streamlit as st
import pandas as pd
import time
import random
import os
import re
import datetime
from dateutil.relativedelta import relativedelta
from docx import Document

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
# YOUR CUSTOM QMS PARSING ENGINE
# ─────────────────────────────────────
DOCS_DIR = "docs" # Make sure you have a folder named 'repo' with your .docx files
REVIEW_CYCLE_MONTHS = 6

def _is_key_value_table(rows) -> bool:
    known_labels = [
        "version", "revision", "approved by", "prepared by",
        "reviewed by", "document number", "revision date",
        "effective date", "field", "doc number", "document id",
    ]
    label_hits = 0
    for row in rows:
        cells = [c.text.strip().lower() for c in row.cells]
        if len(cells) >= 2 and cells[0]:
            for label in known_labels:
                if label in cells[0]:
                    label_hits += 1
                    break
    return label_hits >= 2

def _is_revision_table(first_row: list) -> bool:
    headers_lower = [h.lower() for h in first_row]
    rev_keywords = ["version", "revision", "rev", "rev."]
    date_keywords = ["date", "effective date"]
    has_rev  = any(kw in h for h in headers_lower for kw in rev_keywords)
    has_date = any(kw in h for h in headers_lower for kw in date_keywords)
    return has_rev and has_date

def _clean_revision(raw: str) -> str:
    if not raw: return "—"
    text = raw.strip()
    text = re.sub(r'^(?:revision|version|ver|rev)\.?\s*', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'^[vV](?=\d)', '', text).strip()
    return text if text else "—"

def _find_col(headers: list, keywords: list):
    for i, h in enumerate(headers):
        for kw in keywords:
            if kw in h: return i
    return None

def _parse_date(text: str):
    if not text: return None
    text = text.strip()
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y", "%d-%b-%Y", "%d %B %Y", "%b. %d, %Y", "%m-%d-%Y"]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None

def _parse_key_value_table(rows, meta: dict):
    FIELD_MAP = [
        ("revision date", "approval_date"), ("effective date", "approval_date"), ("date approved", "approval_date"),
        ("approval authority", "approved_by"), ("document number", "doc_number"), ("document id", "doc_number"),
        ("doc number", "doc_number"), ("approved by", "approved_by"), ("authorized by", "approved_by"),
        ("reviewed by", "reviewed_by"), ("prepared by", "prepared_by"),
        ("version", "revision"), ("revision", "revision"), ("rev", "revision"),
    ]
    for row in rows:
        cells = [c.text.strip() for c in row.cells]
        if len(cells) < 2 or not cells[0]: continue
        label = cells[0].lower().rstrip(":")
        value = cells[1].strip()
        if not value: continue
        for key_pattern, meta_key in FIELD_MAP:
            if key_pattern in label:
                if meta_key == "approval_date":
                    parsed = _parse_date(value)
                    if parsed: meta[meta_key] = parsed
                elif meta_key == "revision":
                    meta[meta_key] = _clean_revision(value)
                else:
                    meta[meta_key] = value
                break

def _parse_revision_table(rows, headers: list, meta: dict):
    headers_lower = [h.lower() for h in headers]
    ver_idx  = _find_col(headers_lower, ["version", "revision", "rev", "rev."])
    date_idx = _find_col(headers_lower, ["date", "effective date", "revision date"])
    if len(rows) < 2: return
    last_row = [c.text.strip() for c in rows[-1].cells]
    if ver_idx is not None and not meta["revision"]:
        val = last_row[ver_idx] if ver_idx < len(last_row) else ""
        if val: meta["revision"] = _clean_revision(val)
    if date_idx is not None and not meta["approval_date"]:
        val = last_row[date_idx] if date_idx < len(last_row) else ""
        parsed = _parse_date(val)
        if parsed: meta["approval_date"] = parsed

def _extract_docx_metadata(filepath: str) -> dict:
    meta = {"revision": None, "approved_by": None, "approval_date": None, "reviewed_by": None, "prepared_by": None, "doc_number": None}
    try:
        doc = Document(filepath)
    except Exception:
        return meta
    for table in doc.tables:
        rows = table.rows
        if len(rows) < 2: continue
        first_row = [cell.text.strip() for cell in rows[0].cells]
        if _is_key_value_table(rows):
            _parse_key_value_table(rows, meta)
        elif _is_revision_table(first_row):
            _parse_revision_table(rows, first_row, meta)
    return meta

def _calculate_status(next_review: datetime.date) -> str:
    today = datetime.date.today()
    days_until = (next_review - today).days
    if days_until < 0: return "Overdue"
    elif days_until <= 30: return "Review Soon"
    return "Active"

@st.cache_data(ttl=60)
def scan_documents():
    docs = []
    files = []
    if not os.path.exists(DOCS_DIR):
        return docs, files
    for file in sorted(os.listdir(DOCS_DIR)):
        if file.startswith('.') or file == ".keep": continue
        files.append(file)
        filepath = os.path.join(DOCS_DIR, file)
        name_no_ext = file.rsplit('.', 1)[0]
        ext = file.rsplit('.', 1)[-1].upper() if '.' in file else "N/A"
        
        if " - " in name_no_ext:
            doc_id, title = name_no_ext.split(" - ", 1)
            title = re.sub(r'\s*[Rr]ev\s*[A-Za-z0-9]+', '', title).strip() or title
        else:
            doc_id, title = "N/A", name_no_ext

        stat = os.stat(filepath)
        file_mod_date = datetime.date.fromtimestamp(stat.st_mtime)

        if ext == "DOCX":
            meta = _extract_docx_metadata(filepath)
        else:
            meta = {"revision": None, "approved_by": None, "approval_date": None, "doc_number": None}

        if meta.get("doc_number"): doc_id = meta["doc_number"]
        revision      = meta.get("revision")      or "—"
        approved_by   = meta.get("approved_by")   or "—"
        approval_date = meta.get("approval_date") or file_mod_date
        next_review   = approval_date + relativedelta(months=REVIEW_CYCLE_MONTHS)
        status        = _calculate_status(next_review)

        docs.append({
            "Document ID":   doc_id,
            "Title":         title,
            "Format":        ext,
            "Revision":      revision,
            "Approved By":   approved_by,
            "Approval Date": approval_date.strftime('%Y-%m-%d'),
            "Next Review":   next_review.strftime('%Y-%m-%d'),
            "Status":        status,
        })
    return docs, files

# RUN THE SCANNER
doc_data, raw_files = scan_documents()


# ─────────────────────────────────────
# PAGE 1: DASHBOARD
# ─────────────────────────────────────
def render_dashboard(doc_data):
    st.markdown("""
    <style>
    .enterprise-hero { padding: 2rem; border-radius: 8px; background-color: rgba(26, 115, 232, 0.05); border: 1px solid rgba(26, 115, 232, 0.2); border-left: 6px solid #1a73e8; margin-bottom: 2rem; }
    .hero-title { margin-top: 0; margin-bottom: 0.5rem; font-size: 1.75rem; font-weight: 600; }
    .hero-subtitle { font-size: 1rem; opacity: 0.8; max-width: 700px; line-height: 1.5; }
    .badge { display: inline-block; background-color: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; font-weight: 600; margin-bottom: 1rem; }
    .section-header { font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; margin-top: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(128, 128, 128, 0.2); }
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

    st.markdown('<div class="section-header">Document Registry</div>', unsafe_allow_html=True)

    if not doc_data:
        st.warning("No documents found! Please place your .docx files in the 'repo' folder.")
    else:
        df = pd.DataFrame(doc_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Document ID": st.column_config.TextColumn("ID", width="small"),
                "Title": st.column_config.TextColumn("Document Title", width="large"),
                "Revision": st.column_config.TextColumn("Rev", width="small"),
                "Approved By": st.column_config.TextColumn("Approver", width="medium"),
                "Approval Date": st.column_config.TextColumn("Approved On", width="medium"),
                "Next Review": st.column_config.TextColumn("Next Review", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="medium"),
            },
        )

# ─────────────────────────────────────
# PAGE 2: AI APPLICATION WORKSPACE
# ─────────────────────────────────────
def render_ai_application(doc_data):
    st.title("🤖 AI Application Workspace")
    st.write("---")

    col_left, col_right = st.columns([1, 2.5])

    with col_left:
        st.markdown("### ⚙️ Engine Settings")
        st.selectbox("Select AI Module", ["Gap Analysis", "CAPA Generator", "Audit Checklist", "Risk Assessment"])
        
        st.write("")
        doc_titles = [doc["Title"] for doc in doc_data] if doc_data else ["No documents in repo"]
        selected_doc = st.selectbox("Select QMS Document (From Repo)", doc_titles)
        
        st.write("")
        st.text_area("Additional Context / Prompt", placeholder="Enter specific focus areas for the AI...")
        
        st.write("")
        if st.button("Run AI Engine", type="primary", use_container_width=True):
            if not doc_data:
                st.error("Cannot run engine: No documents in repository.")
            else:
                st.success(f"AI Engine processing {selected_doc}... (Connect backend here)")

        st.write("")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    with col_right:
        st.markdown("### 📊 Output Generation")
        with st.container(border=True, height=500):
            st.info("Awaiting input... Select a repository document and click 'Run AI Engine' to generate QMS assets.")

# ─────────────────────────────────────
# PAGE 3: TRAINING HUB
# ─────────────────────────────────────
def render_training_hub(doc_data):
    st.title("🎓 Smart Training Hub")
    st.write("---")

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown("### 📚 Module Configuration")
        
        st.selectbox("Select Target Standard / Clause", [
            "AS9100 Rev D - 4. Context of the Organization",
            "AS9100 Rev D - 7.1.5 Monitoring and Measuring Resources",
            "AS9100 Rev D - 8.4 Control of Externally Provided Processes",
            "AS9100 Rev D - 10.2 Nonconformity and Corrective Action",
            "ISO 9001:2015 General QMS"
        ])
        
        st.write("")
        doc_titles = [doc["Title"] for doc in doc_data] if doc_data else ["No documents in repo"]
        st.multiselect("Link Repository Documents to Training", doc_titles)
        
        st.write("")
        st.selectbox("Assessment Type", ["Multiple Choice Quiz", "Interactive Scenario", "Read & Acknowledge"])

        st.write("")
        if st.button("Generate Training Content", type="primary", use_container_width=True):
            st.success("Generating AS9100 training materials...")

        st.write("")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    with col2:
        st.markdown("### 📝 Generated Training View")
        with st.container(border=True, height=500):
            st.info("Configure the module on the left to generate AI training content based on your AS9100 clauses and internal documents.")

# ─────────────────────────────────────
# MAIN APP ROUTING
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

    if st.session_state.active_tab == "Dashboard":
        render_dashboard(doc_data)
    elif st.session_state.active_tab == "AI Application":
        render_ai_application(doc_data)
    elif st.session_state.active_tab == "Training Hub":
        render_training_hub(doc_data)

if __name__ == "__main__":
    main()
