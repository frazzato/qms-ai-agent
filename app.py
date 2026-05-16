import streamlit as st
import time
import random
import os

# 1. IMPORT YOUR CLEAN UI MODULES
from ui.dashboard import render_dashboard
from ui.chat import render_ai_application
from ui.training import render_training_hub

# 2. IMPORT CONFIG & MAP EXACT FILE SERVICE PATH
from config.settings import DOCS_DIR
from services.document_service import scan_documents  # <-- CORRECT INTERFACE PATH MATCH

st.set_page_config(page_title="QMS System", layout="wide")

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# Fetch perfectly extracted records
doc_data, available_files = scan_documents()

# ─────────────────────────────────────
# 3. MAIN ROUTING
# ─────────────────────────────────────
def main():
    with st.sidebar:
        st.title("☁️ QMS System")
        st.write("---")
        
        selected = st.radio(
            "Navigation",
            ["Dashboard", "AI Capabilities", "Training Hub"],
            index=["Dashboard", "AI Capabilities", "Training Hub"].index(st.session_state.active_tab),
            label_visibility="hidden"
        )
        
        if selected != st.session_state.active_tab:
            st.session_state.active_tab = selected
            st.rerun()

        st.write("---")
        st.caption("System Health: **98%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

    if st.session_state.active_tab == "Dashboard":
        render_dashboard(doc_data) 
    
    elif st.session_state.active_tab == "AI Capabilities":
        render_ai_application(available_files)
    
    elif st.session_state.active_tab == "Training Hub":
        render_training_hub(available_files)

if __name__ == "__main__":
    main()
