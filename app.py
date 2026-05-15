import streamlit as st
from services.document_service import scan_documents
from ui.dashboard import render_dashboard
from ui.chat import render_chat
from ui.training import render_training

st.set_page_config(page_title="QMS Smart Repository", page_icon="📑", layout="wide")

st.title("📑 AS9100 / ISO 9001 Smart Repository")
st.markdown("Intelligent document control, auditing, and training agent.")
st.divider()

# Load documents
doc_data, available_files = scan_documents()

# -----------------------------------------
# SESSION-STATE NAVIGATION (REPLACES TABS)
# -----------------------------------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

tab = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Audit", "Training"],
    index=["Dashboard", "Audit", "Training"].index(st.session_state.active_tab)
)

# -----------------------------------------
# ROUTING
# -----------------------------------------
if tab == "Dashboard":
    render_dashboard(doc_data)

elif tab == "Audit":
    render_chat(available_files)       # ✅ CHANGED — was render_chat()

elif tab == "Training":
    render_training(available_files)
