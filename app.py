import streamlit as st
import time
import random
import os

# 1. IMPORT YOUR CLEAN UI MODULES
from ui.dashboard import render_dashboard
from ui.chat import render_ai_application
from ui.training import render_training_hub

# 2. IMPORT CONFIG & YOUR ROBUST PARSING ENGINE DIRECTLY
from config.settings import DOCS_DIR
from services.ai_service import scan_documents  # <-- CONNECTS DIRECTLY TO YOUR ENGINE!

st.set_page_config(page_title="QMS System", layout="wide")

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# Fetch perfectly extracted, metadata-parsed records directly from your pipeline
doc_data, available_files = scan_documents()

# ─────────────────────────────────────
# 3. MAIN ROUTING (The Traffic Cop)
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

    # Pass the deeply parsed, real document metadata arrays down to the layout templates
    if st.session_state.active_tab == "Dashboard":
        render_dashboard(doc_data) 
    
    elif st.session_state.active_tab == "AI Capabilities":
        render_ai_application(available_files)
    
    elif st.session_state.active_tab == "Training Hub":
        render_training_hub(available_files)

if __name__ == "__main__":
    main()
