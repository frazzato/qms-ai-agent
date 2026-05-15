import streamlit as st
from services.training_service import generate_training_plan  # adjust to your service

def render_training(available_files):

    # ── Two-column layout ──
    col_left, col_right = st.columns([1, 2])

    # ── LEFT: Document selector ──
    with col_left:
        st.markdown("""
        <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                    border-bottom:2px solid #3b82f6; display:inline-block;
                    padding-bottom:0.3rem; margin-bottom:0.8rem;">
            📂 Select Documents
        </div>
        """, unsafe_allow_html=True)

        if not available_files:
            st.warning("No documents found in **docs/** folder.")
            return

        selected = []
        for f in available_files:
            ext = f.rsplit(".", 1)[-1].lower() if "." in f else ""
            icon_map = {"pdf": "📕", "docx": "📘", "xlsx": "📗", "txt": "📄"}
            icon = icon_map.get(ext, "📄")

            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0;
                        border-radius:8px; padding:0.5rem 0.75rem;
                        margin-bottom:0.4rem; display:flex;
                        align-items:center; gap:0.5rem;">
                <span style="font-size:1.1rem;">{icon}</span>
                <span style="font-size:0.85rem; color:#334155; flex:1;
                             overflow:hidden; text-overflow:ellipsis;
                             white-space:nowrap;">{f}</span>
            </div>
            """, unsafe_allow_html=True)

            if st.checkbox(f"Include", key=f"train_{f}", label_visibility="collapsed"):
                selected.append(f)

    # ── RIGHT: Training plan output ──
    with col_right:
        st.markdown("""
        <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                    border-bottom:2px solid #3b82f6; display:inline-block;
                    padding-bottom:0.3rem; margin-bottom:0.8rem;">
            🎓 Training Plan Generator
        </div>
        """, unsafe_allow_html=True)

        # Role input
        role = st.text_input(
            "Target Role",
            placeholder="e.g. CNC Machine Operator, Quality Inspector…",
        )

        generate = st.button("Generate Training Plan ✨",
                             type="primary", use_container_width=True,
                             disabled=not selected)

        if generate and selected:
            with st.spinner("Building competency-based plan…"):
                # 🔁 Replace with your actual service call
                plan = generate_training_plan(selected, role)

            # ── Render result in a styled card ──
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#eff6ff,#f8fafc);
                        border:1px solid #bfdbfe; border-radius:12px;
                        padding:1.5rem; margin-top:1rem;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                <div style="display:flex; align-items:center; gap:0.5rem;
                            margin-bottom:0.8rem;">
                    <span style="font-size:1.3rem;">📋</span>
                    <span style="font-size:1rem; font-weight:600; color:#1e40af;">
                        Generated Training Plan</span>
                </div>
                <div style="font-size:0.9rem; color:#1e293b; line-height:1.7;
                            white-space:pre-wrap;">{plan}</div>
            </div>
            """, unsafe_allow_html=True)

        elif not selected:
            st.markdown("""
            <div style="background:#f8fafc; border:1px dashed #cbd5e1;
                        border-radius:12px; padding:2.5rem; text-align:center;
                        color:#94a3b8; margin-top:1rem;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">📑</div>
                <div style="font-size:0.9rem;">Select one or more documents
                     on the left, then click <b>Generate</b></div>
            </div>
            """, unsafe_allow_html=True)
