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
        if not docx_files:
            st.warning("No documents found in repository.")
            selected_doc = None
        else:
            selected_doc = st.selectbox("Select Repository Document", docx_files)
        
        st.write("")
        if selected_doc:
            run_engine = st.button("Generate Training Content", type="primary", use_container_width=True)
        else:
            st.button("Generate Training Content", type="primary", use_container_width=True, disabled=True)

        st.write("")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    with col2:
        st.markdown("### 📝 Interactive Training View")
        with st.container(border=True, height=650):
            
            if run_engine and selected_doc:
                doc_context = _read_repo_docx(selected_doc)
                with st.spinner(f"Generating interactive module for {selected_doc}..."):
                    try:
                        st.session_state.training_data = generate_training_module(selected_doc, doc_context)
                    except Exception as e:
                        st.error(f"Failed to generate JSON training block. Error: {e}")
            
            if "training_data" in st.session_state and selected_doc:
                data = st.session_state.training_data
                
                st.markdown(f"#### 📄 {selected_doc}")
                st.write("**Summary:**", data.get("summary", ""))
                st.write("**Why it Matters:**", data.get("importance", ""))
                
                st.markdown(f"""
                <div style="background-color: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 1rem; margin: 1rem 0; border-radius: 4px;">
                    <strong>⚠️ Common Audit Trap:</strong> {data.get("trap", "")}
                </div>
                """, unsafe_allow_html=True)
                
                st.write("---")
                st.markdown("#### 🧠 Knowledge Check")
                st.write(data.get("question", ""))
                
                user_choice = st.radio("Select your answer:", data.get("options", []), index=None, label_visibility="collapsed")
                
                if st.button("Submit Answer"):
                    if not user_choice:
                        st.warning("Please select an answer first.")
                    else:
                        correct_letter = str(data.get("answer", "")).strip()
                        if user_choice.strip().startswith(correct_letter):
                            st.success(f"**Correct!** Great job understanding {selected_doc}.")
                        else:
                            st.error(f"**Incorrect.** The correct answer was **{correct_letter}**.")
            
            elif not run_engine:
                st.info("Select a document on the left and click 'Generate' to build an interactive quiz.")
