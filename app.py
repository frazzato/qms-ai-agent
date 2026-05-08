import streamlit as st
from services.document_service import scan_documents
from ui.dashboard import render_dashboard
from ui.chat import render_chat
from ui.training import render_training

st.set_page_config(page_title="QMS Smart Repository", page_icon="📑", layout="wide")

st.title("📑 AS9100 / ISO 9001 Smart Repository")
st.markdown("Intelligent document control, auditing, and training agent.")
st.divider()

doc_data, available_files = scan_documents()

tab1, tab2, tab3 = st.tabs(["📊 Document Master List", "💬 AI Auditor Chat", "🎓 Training & Summaries"])

with tab1:
    render_dashboard(doc_data)

with tab2:
    render_chat()

with tab3:
    render_training(available_files)

