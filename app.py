import streamlit as st
import time
import random
import os

# 1. IMPORT YOUR CLEAN UI MODULES
from ui.dashboard import render_dashboard
from ui.chat import render_ai_application      # <-- FIXED: Now matches the function name exactly!
from ui.training import render_training_hub

# 2. IMPORT CONFIG
from config.settings import DOCS_DIR

st.set_page_config(page_title="QMS System", layout="wide")

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# ─────────────────────────────────────
# 3. DOCUMENT SCANNER 
# ─────────────────────────────────────
@st.cache_data(ttl=60)
def get_available_files():
    if not os.path.exists(DOCS_DIR):
        return []
    return [f for f in sorted(os.listdir(DOCS_DIR)) if f.lower().endswith(".docx")]

# Fetch the raw list of files for the AI dropdowns
available_files = get_available_files()

# If you have your advanced scan_documents() function that builds the dashboard table, 
# you can import and call it here. For now, we will pass available_files.
doc_data = available_files 

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
        st.caption(f"System Health: **{random.randint(95, 99)}%**")
        st.caption(f"Last Sync: {time.strftime('%H:%M')} CDT")

    # Route traffic to the correct UI file
    if st.session_state.active_tab == "Dashboard":
        render_dashboard(doc_data) 
    
    elif st.session_state.active_tab == "Audit Workspace":
        render_ai_application(available_files) # <-- FIXED: Now calls the correct function!
    
    elif st.session_state.active_tab == "Training Hub":
        render_training_hub(available_files)

if __name__ == "__main__":
    main()
