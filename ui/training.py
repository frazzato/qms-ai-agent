import os
import streamlit as st
from docx import Document
from config.settings import DOCS_DIR
from services.ai_service import generate_training_module

def _read_repo_docx(filename: str) -> str:
    filepath = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(filepath): 
        return ""
    try:
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception: 
        return ""

def render_training_hub(docx_files, *args, **kwargs):
    st.title("🎓 Smart Training Hub")
    st.write("---")

    col1, col2 = st.columns([1, 2.5])
    run_engine = False

    with col1:
        st.markdown("### 📚 Module Configuration")
        
        # 1. Target Clause Input
        clause_input = st.text_input("Target Clause / Topic:", placeholder="e.g., 8.5.1 Control of Production")
        
        # 2. Reference Document Selection
        if not docx_files:
            st.warning("No documents found in repository.")
            selected_doc = None
        else:
            selected_doc = st.selectbox("Reference Document (optional):", ["— None —"] + docx_files)
        
        # 3. Assessment Type Selection
        assessment_type = st.selectbox("Assessment Type:", ["5-Question Multiple Choice Quiz", "3 Short Answer Scenarios", "True/False Verification Check"])
        
        st.write("")
        if clause_input:
            run_engine = st.button("Generate Training Content 🚀", type="primary", use_container_width=True)
        else:
            st.button("Generate Training Content 🚀", type="primary", use_container_width=True, disabled=True)

        st.write("")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    with col2:
        st.markdown("### 📝 Interactive Training View")
        with st.container(border=True, height=650):
            
            # If the button is clicked, trigger your custom generator function
            if run_engine:
                doc_context = ""
                if selected_doc and selected_doc != "— None —":
                    doc_context = _read_repo_docx(selected_doc)
                
                with st.spinner(f"Compiling AS9100 training module for {clause_input}..."):
                    try:
                        # Calls your function perfectly with its 3 string arguments
                        st.session_state.text_training_output = generate_training_module(
                            clause=clause_input,
                            doc_context=doc_context,
                            assessment_type=assessment_type
                        )
                    except Exception as e:
                        st.error(f"Error generating training module. Verify services/ai_service.py has this function. Details: {e}")
            
            # Render the resulting Markdown content smoothly
            if "text_training_output" in st.session_state:
                st.markdown(st.session_state.text_training_output)
            else:
                st.info("Provide a target clause on the left and click 'Generate' to compile your custom training block.")
