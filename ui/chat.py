import os
import streamlit as st
from docx import Document
from config.settings import DOCS_DIR

# Import YOUR custom AI functions
from services.ai_service import (
    ask_groq, analyze_gaps, generate_capa,
    generate_checklist
)

def _read_repo_docx(filename: str) -> str:
    """Read text from a .docx file in the docs/ repository ONLY."""
    filepath = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(filepath): 
        return ""
    
    real_path = os.path.realpath(filepath)
    repo_path = os.path.realpath(DOCS_DIR)
    if not real_path.startswith(repo_path): 
        return ""
    
    try:
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception:
        return ""

def render_ai_application(docx_files, *args, **kwargs):
    st.title("🤖 AI Application Workspace")
    st.write("---")

    col_left, col_right = st.columns([1, 2.5])
    run_engine = False
    
    with col_left:
        st.markdown("### ⚙️ Engine Settings")
        # Dropdown options matching your clean 4-module layout
        mode = st.selectbox("Select AI Module", ["📋 Gap Analysis", "🛠️ CAPA Generator", "✅ Checklist Builder", "💬 Ask Anything"])
        st.write("")

        selected_doc = None
        related_doc = "— None —"
        ref_doc = "— None —"
        finding = ""
        clause = ""
        process_area = ""

        if mode == "📋 Gap Analysis":
            if not docx_files:
                st.warning("No documents found in repository.")
            else:
                selected_doc = st.selectbox("Select Document:", docx_files, format_func=lambda f: f"📄 {f}")
            standard = st.selectbox("Standard:", ["AS9100 Rev D", "ISO 9001:2015", "Both"])
            st.write("")
            run_engine = st.button("Run Gap Analysis 🔍", type="primary", use_container_width=True)

        elif mode == "🛠️ CAPA Generator":
            related_doc = st.selectbox("Related Document (optional):", ["— None —"] + docx_files, format_func=lambda f: f"📄 {f}" if f != "— None —" else f)
            finding = st.text_area("Audit Finding:", placeholder="e.g. Calibration records for CMM missing...", height=120)
            clause = st.text_input("Related Clause (optional):")
            st.write("")
            run_engine = st.button("Generate CAPA 🛠️", type="primary", use_container_width=True)

        elif mode == "✅ Checklist Builder":
            clause = st.text_input("Clause or Topic:", placeholder="e.g. 5.2.1 Establishing the quality policy")
            process_area = st.text_input("Process Area (optional):")
            ref_doc = st.selectbox("Reference Document (optional):", ["— None —"] + docx_files, format_func=lambda f: f"📄 {f}" if f != "— None —" else f)
            st.write("")
            run_engine = st.button("Generate Checklist ✅", type="primary", use_container_width=True)
            
        elif mode == "💬 Ask Anything":
            st.info("The Chat interface is active in the main workspace.")

        st.write("")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    with col_right:
        st.markdown("### 📊 Output Generation")
        with st.container(border=True, height=650):
            
            # ──────────────────────────────────────────
            # MODE 1: ASK ANYTHING
            # ──────────────────────────────────────────
            if mode == "💬 Ask Anything":
                if "audit_messages" not in st.session_state:
                    st.session_state.audit_messages = [{"role": "assistant", "content": "Hello — I'm your **AS9100 / ISO 9001 Audit Agent**. Ask me anything."}]
                
                st.markdown('<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:0.5rem; margin-bottom:1rem; height:450px; overflow-y:auto;">', unsafe_allow_html=True)
                for msg in st.session_state.audit_messages:
                    is_user = msg["role"] == "user"
                    bg = "#3b82f6" if is_user else "#ffffff"
                    fg = "#ffffff" if is_user else "#0f172a"
                    direction = "row-reverse" if is_user else "row"
                    st.markdown(f'<div style="display:flex; justify-content:{"flex-end" if is_user else "flex-start"}; margin:0.6rem 0.5rem;"><div style="display:flex; align-items:flex-start; gap:0.5rem; max-width:80%; flex-direction:{direction};"><div style="background:{bg}; color:{fg}; border-radius:14px; padding:0.8rem 1rem; box-shadow:0 1px 3px rgba(0,0,0,0.06);">{msg["content"]}</div></div></div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                col_input, col_btn = st.columns([6, 1])
                with col_input:
                    user_input = st.text_input("Ask the audit agent…", label_visibility="collapsed", key="chat_input_box")
                with col_btn:
                    send = st.button("Send ➤", use_container_width=True, type="primary")

                if send and user_input:
                    st.session_state.audit_messages.append({"role": "user", "content": user_input})
                    with st.spinner("Analyzing compliance standards..."):
                        try:
                            response = ask_groq(f"You are an elite AS9100 QMS Auditor. Answer: {user_input}")
                            st.session_state.audit_messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            st.error(f"Groq API Error: {str(e)}")
                    st.rerun()

            # ──────────────────────────────────────────
            # MODE 2: GAP ANALYSIS
            # ──────────────────────────────────────────
            elif mode == "📋 Gap Analysis" and run_engine:
                if not selected_doc:
                    st.error("No document selected.")
                else:
                    doc_text = _read_repo_docx(selected_doc)
                    with st.spinner(f"Analyzing {selected_doc}..."):
                        try:
                            result = analyze_gaps(doc_text, standard)
                            st.markdown(result)
                        except Exception as e:
                            st.error(f"Groq API Error: {str(e)}")

            # ──────────────────────────────────────────
            # MODE 3: CAPA GENERATOR
            # ──────────────────────────────────────────
            elif mode == "🛠️ CAPA Generator" and run_engine:
                doc_context = ""
                if related_doc != "— None —":
                    doc_context = f"\n\nRELATED DOCUMENT:\n{_read_repo_docx(related_doc)[:3000]}"
                with st.spinner("Generating corrective actions..."):
                    try:
                        result = generate_capa(finding + doc_context, clause)
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Groq API Error: {str(e)}")

         # ──────────────────────────────────────────
            # MODE 4: CHECKLIST BUILDER (CLAUSE-MATCHING CORES)
            # ──────────────────────────────────────────
            elif mode == "✅ Checklist Builder" and run_engine:
                final_doc_context = ""
                if ref_doc != "— None —":
                    final_doc_context = _read_repo_docx(ref_doc)
                
                # Hardened to look up standard requirements internally, then cross-reference your text
                direct_override_prompt = f"""You are an elite Lead QMS Auditor specializing in AS9100 Rev D and ISO 9001:2015.
                
                CONTEXT: The user has requested an internal audit checklist for a specific target clause. You know the exact text and rules of the official AS9100/ISO standard internally.
                
                TARGET SPECIFIC CLAUSE NUMBER / TOPIC: 
                {clause}
                
                PROCESS AREA: 
                {process_area if process_area else "General Operations"}
                
                REFERENCE COMPANY PROCEDURE TEXT (COMPARE AGAINST THIS):
                {final_doc_context[:4000] if final_doc_context else "No reference document provided. Base the checklist strictly on standard requirements."}
                
                INSTRUCTIONS:
                1. Recall your internal standard library for Clause {clause}.
                2. Cross-reference the provided Company Procedure Text. 
                3. Create a numbered internal audit checklist specifically designed to verify if the company's process actually fulfills Clause {clause}.
                4. For each question, detail the objective evidence required and notice if there are obvious gaps based on what was read in the procedure text.
                
                Format the output as a highly professional, clean Markdown audit checklist."""
                
                with st.spinner(f"Retrieving standard data and analyzing compliance for Clause {clause}..."):
                    try:
                        result = ask_groq(direct_override_prompt)
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Groq API Error: {str(e)}")
