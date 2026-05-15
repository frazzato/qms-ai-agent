import os
import streamlit as st
from docx import Document
from config.settings import DOCS_DIR
from services.ai_service import (
    ask_groq, analyze_gaps, generate_capa,
    generate_checklist, assess_risk
)


def _read_repo_docx(filename: str) -> str:
    """Read text from a .docx file in the docs/ repository ONLY."""
    filepath = os.path.join(DOCS_DIR, filename)

    if not os.path.exists(filepath):
        return ""

    # Security: block path traversal
    real_path = os.path.realpath(filepath)
    repo_path = os.path.realpath(DOCS_DIR)
    if not real_path.startswith(repo_path):
        return ""

    try:
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception:
        return ""


def _get_docx_files(files: list) -> list:
    """Filter to only .docx files in the repository."""
    return [f for f in files if f.lower().endswith(".docx")]


def render_chat(available_files: list):

    docx_files = _get_docx_files(available_files)

    # ── Mode selector ──
    st.markdown("""
    <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                border-bottom:2px solid #3b82f6; display:inline-block;
                padding-bottom:0.3rem; margin-bottom:0.8rem;">
        🔍 Select Audit Mode
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Audit Mode",
        ["💬 Ask Anything", "📋 Gap Analysis", "🛠️ CAPA Generator",
         "✅ Checklist Builder", "⚠️ Risk Assessment"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODE 1: FREE CHAT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if mode == "💬 Ask Anything":
        _render_free_chat()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODE 2: GAP ANALYSIS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif mode == "📋 Gap Analysis":
        st.markdown("""
        <div style="background:linear-gradient(145deg,
                    rgba(59,130,246,0.05), rgba(139,92,246,0.05));
                    border:1px solid rgba(59,130,246,0.15);
                    border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <strong>📋 Select a controlled document</strong>
            from your repository and the AI will identify which
            AS9100/ISO 9001 clauses are covered, missing, or weak.
        </div>
        """, unsafe_allow_html=True)

        if not docx_files:
            st.warning("No .docx documents found in the repository.")
            return

        sel_col, std_col = st.columns([2, 1])

        with sel_col:
            selected_doc = st.selectbox(
                "Select Document:",
                docx_files,
                format_func=lambda f: f"📄 {f}",
                key="gap_doc",
            )

        with std_col:
            standard = st.selectbox(
                "Standard:",
                ["AS9100 Rev D", "ISO 9001:2015", "Both"],
                key="gap_std",
            )

        if selected_doc and st.button("Run Gap Analysis 🔍", type="primary",
                                       use_container_width=True):
            doc_text = _read_repo_docx(selected_doc)
            if not doc_text:
                st.error("Could not read document content.")
                return

            with st.spinner(f"Analyzing **{selected_doc}** against {standard}..."):
                result = analyze_gaps(doc_text, standard)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#eff6ff,#f8fafc);
                        border:1px solid #bfdbfe; border-left:4px solid #3b82f6;
                        border-radius:12px; padding:1.3rem 1.5rem; margin-top:1rem;">
                <div style="display:flex; align-items:center; gap:0.5rem;
                            margin-bottom:0.6rem;">
                    <span style="font-size:1.2rem;">📋</span>
                    <span style="font-size:1rem; font-weight:700; color:#1e40af;">
                        Gap Analysis: {selected_doc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODE 3: CAPA GENERATOR
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif mode == "🛠️ CAPA Generator":
        st.markdown("""
        <div style="background:linear-gradient(145deg,
                    rgba(239,68,68,0.05), rgba(249,115,22,0.05));
                    border:1px solid rgba(239,68,68,0.15);
                    border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <strong>🛠️ Describe an audit finding</strong>
            against a controlled document and the AI will generate
            a complete CAPA with root cause analysis.
        </div>
        """, unsafe_allow_html=True)

        # Optional: link finding to a specific doc
        if docx_files:
            related_doc = st.selectbox(
                "Related Document (optional):",
                ["— None —"] + docx_files,
                format_func=lambda f: f"📄 {f}" if f != "— None —" else f,
                key="capa_doc",
            )
        else:
            related_doc = "— None —"

        finding = st.text_area(
            "Audit Finding:",
            placeholder="e.g. Calibration records for CMM were not available "
                        "for the last 3 months...",
            height=120,
        )

        clause = st.text_input(
            "Related Clause (optional):",
            placeholder="e.g. 7.1.5 Monitoring and Measuring Resources",
        )

        if finding and st.button("Generate CAPA 🛠️", type="primary",
                                  use_container_width=True):
            # Optionally include doc context
            doc_context = ""
            if related_doc != "— None —":
                doc_text = _read_repo_docx(related_doc)
                if doc_text:
                    doc_context = (f"\n\nRELATED DOCUMENT ({related_doc}):\n"
                                   f"{doc_text[:3000]}")

            enhanced_finding = finding + doc_context

            with st.spinner("Generating corrective actions..."):
                result = generate_capa(enhanced_finding, clause)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#fef2f2,#f8fafc);
                        border:1px solid #fecaca; border-left:4px solid #ef4444;
                        border-radius:12px; padding:1.3rem 1.5rem; margin-top:1rem;">
                <div style="display:flex; align-items:center; gap:0.5rem;
                            margin-bottom:0.6rem;">
                    <span style="font-size:1.2rem;">🛠️</span>
                    <span style="font-size:1rem; font-weight:700; color:#991b1b;">
                        CAPA Report</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODE 4: CHECKLIST BUILDER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif mode == "✅ Checklist Builder":
        st.markdown("""
        <div style="background:linear-gradient(145deg,
                    rgba(34,197,94,0.05), rgba(16,185,129,0.05));
                    border:1px solid rgba(34,197,94,0.15);
                    border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <strong>✅ Generate an audit checklist</strong>
            for a specific clause, optionally linked to a controlled
            procedure in your repository.
        </div>
        """, unsafe_allow_html=True)

        cl_col, proc_col = st.columns(2)

        with cl_col:
            clause = st.text_input(
                "Clause or Topic:",
                placeholder="e.g. 8.5.1 Control of Production",
                key="check_clause",
            )

        with proc_col:
            process_area = st.text_input(
                "Process Area (optional):",
                placeholder="e.g. Welding, Assembly",
                key="check_process",
            )

        # Optionally base checklist on a specific doc
        if docx_files:
            ref_doc = st.selectbox(
                "Reference Document (optional):",
                ["— None —"] + docx_files,
                format_func=lambda f: f"📄 {f}" if f != "— None —" else f,
                key="check_doc",
            )
        else:
            ref_doc = "— None —"

        if clause and st.button("Generate Checklist ✅", type="primary",
                                 use_container_width=True):
            doc_context = ""
            if ref_doc != "— None —":
                doc_text = _read_repo_docx(ref_doc)
                if doc_text:
                    doc_context = doc_text[:3000]

            enhanced_clause = clause
            if doc_context:
                enhanced_clause += (f"\n\nBased on this controlled procedure "
                                    f"({ref_doc}):\n{doc_context}")

            with st.spinner("Building audit checklist..."):
                result = generate_checklist(enhanced_clause, process_area)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#f0fdf4,#f8fafc);
                        border:1px solid #bbf7d0; border-left:4px solid #22c55e;
                        border-radius:12px; padding:1.3rem 1.5rem; margin-top:1rem;">
                <div style="display:flex; align-items:center; gap:0.5rem;
                            margin-bottom:0.6rem;">
                    <span style="font-size:1.2rem;">✅</span>
                    <span style="font-size:1rem; font-weight:700; color:#166534;">
                        Audit Checklist: {clause}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODE 5: RISK ASSESSMENT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif mode == "⚠️ Risk Assessment":
        st.markdown("""
        <div style="background:linear-gradient(145deg,
                    rgba(245,158,11,0.05), rgba(251,191,36,0.05));
                    border:1px solid rgba(245,158,11,0.15);
                    border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <strong>⚠️ Select a process or procedure</strong>
            from your repository and the AI will generate a full
            risk assessment with likelihood × severity matrix.
        </div>
        """, unsafe_allow_html=True)

        # Option A: pick a repo doc
        # Option B: type a process manually
        input_method = st.radio(
            "Input method:",
            ["📄 Select from Repository", "✏️ Describe Manually"],
            horizontal=True,
            key="risk_method",
        )

        process_text = ""
        process_label = ""

        if input_method == "📄 Select from Repository":
            if not docx_files:
                st.warning("No .docx documents found in the repository.")
                return

            risk_doc = st.selectbox(
                "Select Document:",
                docx_files,
                format_func=lambda f: f"📄 {f}",
                key="risk_doc",
            )
            process_label = risk_doc
            context = st.text_area(
                "Additional Context (optional):",
                placeholder="e.g. New supplier, critical aerospace parts...",
                height=80,
                key="risk_ctx_doc",
            )

            if st.button("Assess Risk ⚠️", type="primary",
                          use_container_width=True):
                doc_text = _read_repo_docx(risk_doc)
                if not doc_text:
                    st.error("Could not read document content.")
                    return
                process_text = f"Based on this procedure ({risk_doc}):\n{doc_text[:4000]}"

        else:
            process = st.text_input(
                "Process / Activity:",
                placeholder="e.g. First Article Inspection, Supplier Receiving",
                key="risk_process",
            )
            context = st.text_area(
                "Additional Context (optional):",
                placeholder="e.g. New supplier, high-value aerospace parts...",
                height=80,
                key="risk_ctx_manual",
            )
            process_label = process

            if process and st.button("Assess Risk ⚠️", type="primary",
                                      use_container_width=True):
                process_text = process

        if process_text:
            with st.spinner("Analyzing risks..."):
                result = assess_risk(process_text, context if context else "")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#fffbeb,#f8fafc);
                        border:1px solid #fde68a; border-left:4px solid #f59e0b;
                        border-radius:12px; padding:1.3rem 1.5rem; margin-top:1rem;">
                <div style="display:flex; align-items:center; gap:0.5rem;
                            margin-bottom:0.6rem;">
                    <span style="font-size:1.2rem;">⚠️</span>
                    <span style="font-size:1rem; font-weight:700; color:#854d0e;">
                        Risk Assessment: {process_label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(result)


def _render_free_chat():
    """Original chat with enterprise styling."""

    if "audit_messages" not in st.session_state:
        st.session_state.audit_messages = [
            {"role": "assistant",
             "content": "Hello — I'm your **AS9100 / ISO 9001 Audit Agent**. "
                        "Ask me about procedures, clauses, or request audit checklists."}
        ]

    st.markdown("""
    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;
                padding:0.5rem; margin-bottom:1rem; min-height:200px;">
    """, unsafe_allow_html=True)

    for msg in st.session_state.audit_messages:
        is_user   = msg["role"] == "user"
        alignment = "flex-end" if is_user else "flex-start"
        bg        = "#3b82f6" if is_user else "#ffffff"
        fg        = "#ffffff" if is_user else "#0f172a"
        border    = "none"    if is_user else "1px solid #e2e8f0"
        avatar    = "👤"      if is_user else "🛡️"
        radius    = "14px 14px 4px 14px" if is_user else "14px 14px 14px 4px"
        direction = "row-reverse" if is_user else "row"

        st.markdown(f"""
        <div style="display:flex; justify-content:{alignment}; margin:0.6rem 0.5rem;">
            <div style="display:flex; align-items:flex-start; gap:0.5rem;
                        max-width:80%; flex-direction:{direction};">
                <div style="font-size:1.3rem; margin-top:0.2rem;">{avatar}</div>
                <div style="background:{bg}; color:{fg}; border:{border};
                            border-radius:{radius}; padding:0.8rem 1rem;
                            font-size:0.9rem; line-height:1.55;
                            box-shadow:0 1px 3px rgba(0,0,0,0.06);">
                    {msg['content']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col_input, col_btn = st.columns([6, 1])
    with col_input:
        user_input = st.text_input(
            "Ask the audit agent…",
            placeholder="e.g. What is the procedure for controlling nonconforming outputs?",
            label_visibility="collapsed",
            key="audit_input",
        )
    with col_btn:
        send = st.button("Send ➤", use_container_width=True, type="primary")

    if send and user_input:
        st.session_state.audit_messages.append(
            {"role": "user", "content": user_input}
        )

        prompt = f"""
        You are an elite AS9100 and ISO 9001 QMS Auditor.
        Answer the following user query strictly using standard quality management principles.
        User Query: {user_input}
        """

        with st.spinner("Analyzing compliance standards..."):
            response = ask_groq(prompt)

        st.session_state.audit_messages.append(
            {"role": "assistant", "content": response}
        )
        st.rerun()
