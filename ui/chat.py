import streamlit as st
from services.ai_service import ask_groq  # ✅ your original import

def render_chat():

    # ── Chat history ──
    if "audit_messages" not in st.session_state:
        st.session_state.audit_messages = [
            {"role": "assistant",
             "content": "Hello — I'm your **AS9100 / ISO 9001 Audit Agent**. "
                        "Ask me about procedures, clauses, or request audit checklists."}
        ]

    # ── Styled message container ──
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

    # ── Input bar ──
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

    # ── Handle send — uses YOUR original Groq logic ──
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
