import os
import streamlit as st
from docx import Document
from config.settings import DOCS_DIR

# Import YOUR custom AI functions
from services.ai_service import (
    ask_groq, analyze_gaps, generate_capa,
    generate_checklist, assess_risk
)

def _read_repo_docx(filename: str) -> str:
    """Read text from a .docx file in the docs/ repository ONLY."""
    filepath = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(filepath): return ""
    real_path = os.path.realpath(filepath)
    repo_path = os.path.realpath(DOCS_DIR)
    if not real_path.startswith(repo_path): return ""
    try:
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception:
        return ""

def _get_docx_files() -> list:
    if not os.path.exists(DOCS_DIR): return []
    return [f for f in os.listdir(DOCS_DIR) if f.lower().endswith(".docx")]

def render_ai_application(*args, **kwargs):
    st.title("🤖 AI Application Workspace")
    st.write("---")

    docx_files = _get_docx_files()
    col_left, col_right = st.columns([1, 2.5])
    run_engine = False
    
    with col_left:
        st.markdown("### ⚙️ Engine Settings")
        mode = st.selectbox("Select AI Module", ["📋 Gap Analysis", "🛠️ CAPA Generator", "✅ Checklist Builder", "⚠️ Risk Assessment", "💬 Ask Anything"])
        st.write("")

        if mode == "📋 Gap Analysis":
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
            clause = st.text_input("Clause or Topic:", placeholder="e.g. 8.5.1 Control of Production")
            process_area = st.text_input("Process Area (optional):")
            ref_doc = st.selectbox("Reference Document (optional):", ["— None —"] + docx_files, format_func=lambda f: f"📄 {f}" if f != "— None —" else f)
            st.write("")
            run_engine = st.button("Generate Checklist ✅", type="primary", use_container_width=True)

        elif mode == "⚠️ Risk Assessment":
            input_method = st.radio("Input method:", ["📄 Select from Repository", "✏️ Describe Manually"])
            if input_method == "📄 Select from Repository":
                risk_doc = st.selectbox("Select Document:", docx_files, format_func=lambda f: f"📄 {f}")
                context = st.text_area("Additional Context (optional):", height=80)
            else:
                process = st.text_input("Process / Activity:", placeholder="e.g. First Article Inspection")
                context = st.text_area("Additional Context (optional):", height=80)
            st.write("")
            run_engine = st.button("Assess Risk ⚠️", type="primary", use_container_width=True)
            
        elif mode == "💬 Ask Anything":
            st.info("The Chat interface is active in the main workspace.")

        st.write("")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.rerun()

    with col_right:
        st.markdown("### 📊 Output Generation")
        with st.container(border=True, height=650):
            
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

                user_input = st.chat_input("Ask the audit agent…")
                if user_input:
                    st.session_state.audit_messages.append({"role": "user", "content": user_input})
                    with st.spinner("Analyzing compliance standards..."):
                        response = ask_groq(f"You are an elite AS9100 QMS Auditor. Answer: {user_input}")
                    st.session_state.audit_messages.append({"role": "assistant", "content": response})
                    st.rerun()

            elif mode == "📋 Gap Analysis" and run_engine:
                doc_text = _read_repo_docx(selected_doc)
                with st.spinner(f"Analyzing {selected_doc}..."):
                    result = analyze_gaps(doc_text, standard)
                st.markdown(result)

            elif mode == "🛠️ CAPA Generator" and run_engine:
                doc_context = ""
                if related_doc != "— None —":
                    doc_context = f"\n\nRELATED DOCUMENT:\n{_read_repo_docx(related_doc)[:3000]}"
                with st.spinner("Generating corrective actions..."):
                    result = generate_capa(finding + doc_context, clause)
                st.markdown(result)

            elif mode == "✅ Checklist Builder" and run_engine:
                doc_context = ""
                if ref_doc != "— None —":
                    doc_context = f"\n\nBASED ON:\n{_read_repo_docx(ref_doc)[:3000]}"
                with st.spinner("Building audit checklist..."):
                    result = generate_checklist(clause + doc_context, process_area)
                st.markdown(result)

            elif mode == "⚠️ Risk Assessment" and run_engine:
                if input_method == "📄 Select from Repository":
                    process_text = f"Based on {risk_doc}:\n{_read_repo_docx(risk_doc)[:4000]}"
                else:
                    process_text = process
                with st.spinner("Analyzing risks..."):
                    result = assess_risk(process_text, context)
                st.markdown(result)
