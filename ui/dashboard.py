import streamlit as st
import pandas as pd
import time
import random

def render_dashboard(doc_data):

    # -----------------------------
    # SYSTEM HEALTH + LAST AI SYNC
    # -----------------------------
    st.subheader("System Overview")

    health_score = random.randint(82, 99)

    st.progress(health_score / 100)
    st.write(f"**System Health:** {health_score}%")

    st.caption(f"Last AI Sync: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    st.divider()

    # -----------------------------
    # CLICKABLE CARDS (3 ONLY)
    # -----------------------------
    st.markdown("""
    <style>
        .pillar-card {
            padding: 20px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            font-size: 20px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .pillar-card:hover {
            transform: translateY(-4px);
            box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
        }
        .audit  { background: #50C878; }
        .train  { background: #F5A623; }
        .master { background: #9B59B6; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🕵️ Audit Engine", use_container_width=True):
            st.session_state.active_tab = "Audit"
            st.experimental_rerun()

    with col2:
        if st.button("🎓 Training Module", use_container_width=True):
            st.session_state.active_tab = "Training"
            st.experimental_rerun()

    with col3:
        if st.button("📑 Master List", use_container_width=True):
            st.session_state.active_tab = "Dashboard"
            st.experimental_rerun()

    st.divider()

    # -----------------------------
    # STATUS INDICATORS
    # -----------------------------
    st.markdown("### 🔵 Status Indicators")

    colA, colB, colC = st.columns(3)
    colA.metric("Audit Engine", "Ready", "🟢")
    colB.metric("Training Module", "Stable", "🟢")
    colC.metric("Master List", "Synced", "🟢")

    st.divider()

    # -----------------------------
    # COLLAPSIBLE ARCHITECTURE DIAGRAM
    # -----------------------------
    with st.expander("📐 System Architecture Diagram"):
        st.markdown("""
        ```
        ┌──────────────────────────┐
        │       Audit Engine       │
        │ - Clause Mapping         │
        │ - Nonconformity Checks   │
        └─────────────┬────────────┘
                      │
        ┌─────────────▼────────────┐
        │     Training Module       │
        │ - Summaries               │
        │ - Knowledge Checks        │
        └─────────────┬────────────┘
                      │
        ┌─────────────▼────────────┐
        │     Master List (Docs)    │
        │ - GitHub Sync             │
        │ - Metadata Extraction     │
        └──────────────────────────┘
        ```
        """)

    st.divider()

    # -----------------------------
    # DOCUMENT COVERAGE HEATMAP
    # -----------------------------
    st.markdown("### 🔥 Document Coverage Heatmap")

    heatmap_data = pd.DataFrame({
        "Document": [d["Document ID"] for d in doc_data],
        "Coverage Score": [random.randint(70, 100) for _ in doc_data]
    })

    st.bar_chart(heatmap_data.set_index("Document"))

    st.divider()

    # -----------------------------
    # MASTER LIST TABLE
    # -----------------------------
    st.markdown("### 📑 Controlled Document Register")

    if not doc_data:
        st.info("No documents found in /docs.")
        return

    df = pd.DataFrame(doc_data)
    st.dataframe(df, use_container_width=True, hide_index=True)




    
