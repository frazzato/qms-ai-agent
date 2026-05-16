import streamlit as st
import time
import random
import os
import re
import datetime
from dateutil.relativedelta import relativedelta
from docx import Document

# 1. IMPORT YOUR CLEAN UI MODULES
from ui.dashboard import render_dashboard
from ui.chat import render_ai_application
from ui.training import render_training_hub

# 2. IMPORT CONFIG & SAFELY CHECK FOR SERVICES
from config.settings import DOCS_DIR

try:
    from services.ai_service import _extract_docx_metadata
except ImportError:
    _extract_docx_metadata = None

st.set_page_config(page_title="QMS System", layout="wide")

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

REVIEW_CYCLE_MONTHS = 6

# Helper to safely calculate status
def _calculate_status(next_review: datetime.date) -> str:
    days_until = (next_review - datetime.date.today()).days
    if days_until < 0: return "Overdue"
    elif days_until <= 30: return "Review Soon"
    return "Active"

# ─────────────────────────────────────
# 3. COMPLETE DOCUMENT REGISTRY SCANNER
# ─────────────────────────────────────
@st.cache_data(ttl=60)
def scan_documents():
    docs, files = [], []
    if not os.path.exists(DOCS_DIR): 
        return docs, files
    
    for file in sorted(os.listdir(DOCS_DIR)):
        if file.startswith('.') or file == ".keep": 
            continue
        if not file.lower().endswith(".docx"):
            continue

        files.append(file)
        filepath = os.path.join(DOCS_DIR, file)
        name_no_ext = file.rsplit('.', 1)[0]

        if " - " in name_no_ext:
            doc_id, title = name_no_ext.split(" - ", 1)
            title = re.sub(r'\s*[Rr]ev\s*[A-Za-z0-9]+', '', title).strip() or title
        else: 
            doc_id, title = "N/A", name_no_ext

        # Set fallback modification date
        stat = os.stat(filepath)
        file_mod_date = datetime.date.fromtimestamp(stat.st_mtime)

        # Read layout data from within docx tables if possible
        revision = "—"
        approved_by = "—"
        approval_date = file_mod_date

        try:
            doc = Document(filepath)
            # Basic fallback extraction from paragraphs if metadata service isn't active
            for table in doc.tables:
                if len(table.rows) >= 2:
                    for row in table.rows:
                        cells = [c.text.strip().lower() for c in row.cells]
                        if len(cells) >= 2:
                            if "rev" in cells[0] or "version" in cells[0]:
                                revision = row.cells[1].text.strip()
                            if "approved" in cells[0] or "author" in cells[0]:
                                approved_by = row.cells[1].text.strip()
        except Exception:
            pass

        next_review = approval_date + relativedelta(months=REVIEW_CYCLE_MONTHS)
        status = _calculate_status(next_review)

        docs.append({
            "Document ID": doc_id, 
            "Title": title, 
            "Format": "DOCX", 
            "Revision": revision if revision else "—",
            "Approved By": approved_by if approved_by else "—", 
            "Approval Date": approval_date.strftime('%Y-%m-%d'),
            "Next Review": next_review.strftime('%Y-%m-%d'), 
            "Status": status,
        })
    return docs, files

# Fetch data using your full scanner pipeline
doc_data, available_files = scan_documents()

# ─────────────────────────────────────
# 4. MAIN ROUTING (The Traffic Cop)
# ─────────────────────────────────────
def main():
    with st.sidebar:
        st.title("☁️ QMS System")
        st.write("---")
        
        selected = st.radio(
            "Navigation",
            ["Dashboard", "Audit Workspace", "Training Hub"],
            index=["Dashboard", "Audit Workspace", "Training Hub"].index(st.session_state.active_tab),
            label_visibility="hidden"
        )
        
        if selected != st.session_state.active_tab:
            st.session_state.active_tab = selected
            st.rerun()

        st.write("---")
        st.caption(f"System Health: **98%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

    # Route traffic with correct matching structures
    if st.session_state.active_tab == "Dashboard":
        render_dashboard(doc_data) 
    
    elif st.session_state.active_tab == "Audit Workspace":
        render_ai_application(available_files)
    
    elif st.session_state.active_tab == "Training Hub":
        render_training_hub(available_files)

if __name__ == "__main__":
    main()
