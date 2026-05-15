import streamlit as st
from services.training_service import generate_training_module  # ✅ your original import

def render_training(files):

    if not files:
        st.markdown("""
        <div style="background:#f8fafc; border:1px dashed #cbd5e1;
                    border-radius:12px; padding:2.5rem; text-align:center;
                    color:#94a3b8; margin-top:1rem;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📑</div>
            <div style="font-size:0.95rem;">No documents available for training.<br>
                 Add files to the <b>docs/</b> folder to get started.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ─────────────────────────────────────
    # DOCUMENT SELECTOR + GENERATE BUTTON
    # ─────────────────────────────────────
    sel_col, btn_col = st.columns([3, 1])

    with sel_col:
        doc = st.selectbox(
            "Select Document:",
            files,
            label_visibility="collapsed",
            format_func=lambda f: f"📄  {f}",
        )
    with btn_col:
        generate = st.button("Generate Training Module ✨",
                             type="primary", use_container_width=True)

    if generate:
        with st.spinner(f"Building training module for **{doc}**..."):
            st.session_state["training_data"] = generate_training_module(doc)

    # ─────────────────────────────────────
    # TRAINING MODULE OUTPUT
    # ─────────────────────────────────────
    if "training_data" in st.session_state:
        data = st.session_state["training_data"]

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Section 1: Summary ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#eff6ff,#f8fafc);
                    border:1px solid #bfdbfe; border-left:4px solid #3b82f6;
                    border-radius:12px; padding:1.3rem 1.5rem; margin-bottom:1rem;
                    box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.6rem;">
                <span style="font-size:1.2rem;">⚡</span>
                <span style="font-size:1rem; font-weight:700; color:#1e40af;">
                    1 · The 30-Second Summary</span>
            </div>
            <div style="font-size:0.9rem; color:#1e293b; line-height:1.7;">
                {data['summary']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Section 2: Importance ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#f0fdf4,#f8fafc);
                    border:1px solid #bbf7d0; border-left:4px solid #22c55e;
                    border-radius:12px; padding:1.3rem 1.5rem; margin-bottom:1rem;
                    box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.6rem;">
                <span style="font-size:1.2rem;">🎯</span>
                <span style="font-size:1rem; font-weight:700; color:#166534;">
                    2 · Why It Is Important</span>
            </div>
            <div style="font-size:0.9rem; color:#1e293b; line-height:1.7;">
                {data['importance']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Section 3: Audit Trap ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fef9c3,#fffbeb);
                    border:1px solid #fde68a; border-left:4px solid #f59e0b;
                    border-radius:12px; padding:1.3rem 1.5rem; margin-bottom:1rem;
                    box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.6rem;">
                <span style="font-size:1.2rem;">⚠️</span>
                <span style="font-size:1rem; font-weight:700; color:#854d0e;">
                    3 · The Audit Trap</span>
            </div>
            <div style="font-size:0.9rem; color:#1e293b; line-height:1.7;">
                <strong>Watch Out:</strong> {data['trap']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Section 4: Knowledge Check ──
        st.markdown(f"""
        <div style="background:#fff; border:1px solid #e2e8f0;
                    border-left:4px solid #8b5cf6; border-radius:12px;
                    padding:1.3rem 1.5rem; margin-bottom:0.5rem;
                    box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.3rem;">
                <span style="font-size:1.2rem;">🧠</span>
                <span style="font-size:1rem; font-weight:700; color:#6d28d9;">
                    4 · Knowledge Check</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Quiz (Streamlit widgets — must be outside HTML) ──
        user_answer = st.radio(
            data["question"],
            data["options"],
            index=None,
            key="training_quiz",
        )

        submit_col, _ = st.columns([1, 3])
        with submit_col:
            submitted = st.button("Submit Answer ✅", type="primary",
                                  use_container_width=True)

        if submitted:
            if user_answer is None:
                st.info("☝️ Please select an answer first.")
            else:
                letters = ["A", "B", "C", "D"]
                selected_letter = letters[data["options"].index(user_answer)]

                if selected_letter == data["answer"]:
                    st.markdown(f"""
                    <div style="background:#dcfce7; border:1px solid #bbf7d0;
                                border-radius:10px; padding:1rem 1.2rem;
                                margin-top:0.5rem; display:flex;
                                align-items:center; gap:0.6rem;">
                        <span style="font-size:1.5rem;">🎉</span>
                        <span style="font-size:0.95rem; font-weight:600; color:#166534;">
                            Correct! ({selected_letter})</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:#fee2e2; border:1px solid #fecaca;
                                border-radius:10px; padding:1rem 1.2rem;
                                margin-top:0.5rem; display:flex;
                                align-items:center; gap:0.6rem;">
                        <span style="font-size:1.5rem;">❌</span>
                        <span style="font-size:0.95rem; font-weight:600; color:#991b1b;">
                            Incorrect — the correct answer was: {data['answer']}</span>
                    </div>
                    """, unsafe_allow_html=True)
