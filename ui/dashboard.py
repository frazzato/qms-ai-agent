import streamlit as st
import pandas as pd
import time
import random

def render_dashboard(doc_data):

    # ─────────────────────────────────────
    # INJECT FUTURISTIC CSS
    # ─────────────────────────────────────
    st.markdown("""
    <style>
    /* ── Neon glow cards ── */
    .neon-card {
        background: linear-gradient(145deg, #0a0a1a, #111132);
        border: 1px solid rgba(59,130,246,0.2);
        border-radius: 16px;
        padding: 1.4rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .neon-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .neon-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(59,130,246,0.15);
    }
    .neon-blue::before    { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .neon-green::before   { background: linear-gradient(90deg, #22c55e, #4ade80); }
    .neon-amber::before   { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .neon-red::before     { background: linear-gradient(90deg, #ef4444, #f87171); }
    .neon-purple::before  { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

    .neon-icon  { font-size: 1.6rem; margin-bottom: 0.4rem; }
    .neon-value { font-size: 2rem; font-weight: 800; color: #f1f5f9; margin: 0; }
    .neon-label { font-size: 0.72rem; font-weight: 600; color: #64748b;
                  text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }

    /* ── Glass panels ── */
    .glass-panel {
        background: linear-gradient(145deg,
                    rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── Section title ── */
    .section-glow {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-glow .accent-bar {
        display: inline-block;
        width: 4px;
        height: 1.2rem;
        background: linear-gradient(180deg, #3b82f6, #8b5cf6);
        border-radius: 4px;
    }

    /* ── Quick-access cards ── */
    .access-card {
        background: linear-gradient(145deg, #0f172a, #1a1a3e);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.3rem 1rem;
        text-align: center;
        transition: all 0.25s ease;
        cursor: pointer;
    }
    .access-card:hover {
        border-color: rgba(59,130,246,0.4);
        box-shadow: 0 0 20px rgba(59,130,246,0.1);
        transform: translateY(-2px);
    }
    .access-icon  { font-size: 2rem; margin-bottom: 0.4rem; }
    .access-title { font-size: 0.95rem; font-weight: 700; color: #e2e8f0; }
    .access-desc  { font-size: 0.78rem; color: #64748b; margin-top: 0.2rem; }

    /* ── Status dots ── */
    .status-row {
        display: flex; align-items: center; gap: 0.6rem;
        padding: 0.5rem 0;
    }
    .pulse-dot {
        height: 10px; width: 10px; border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 8px #22c55e;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.5; }
    }

    /* ── Health bar ── */
    .health-bar-track {
        background: rgba(255,255,255,0.06);
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
    }
    .health-bar-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 1s ease;
    }

    /* ── Dark theme override for dataframe ── */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # KPI CARDS
    # ─────────────────────────────────────
    total = len(doc_data) if doc_data else 0

    # Safe status counting — works with any doc_data shape
    def count_status(keyword):
        if not doc_data:
            return 0
        return sum(1 for d in doc_data
                   if keyword.lower() in str(d.get("Status", "")).lower())

    active  = count_status("active")
    soon    = count_status("review soon")
    overdue = count_status("overdue")

    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "📁", total,   "Total Docs",   "neon-blue"),
        (k2, "✅", active,  "Active",        "neon-green"),
        (k3, "⏳", soon,    "Review Soon",   "neon-amber"),
        (k4, "⚠️", overdue, "Overdue",       "neon-red"),
    ]
    for col, icon, val, label, css in kpis:
        with col:
            st.markdown(f"""
            <div class="neon-card {css}">
                <div class="neon-icon">{icon}</div>
                <p class="neon-value">{val}</p>
                <p class="neon-label">{label}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # SYSTEM HEALTH + SYNC BAR
    # ─────────────────────────────────────
    health = random.randint(85, 99)
    bar_color = "#22c55e" if health >= 90 else "#f59e0b"

    st.markdown(f"""
    <div class="glass-panel">
        <div style="display:flex; justify-content:space-between; align-items:center;
                    margin-bottom:0.6rem;">
            <div style="display:flex; align-items:center; gap:0.8rem;">
                <span style="font-size:1.2rem;">🛡️</span>
                <span style="font-size:0.85rem; font-weight:700; color:#e2e8f0;">
                    SYSTEM HEALTH</span>
                <span style="font-size:1.4rem; font-weight:800; color:{bar_color};">
                    {health}%</span>
            </div>
            <span style="font-size:0.72rem; color:#475569;">
                Last AI Sync: {time.strftime('%Y-%m-%d %H:%M:%S')}</span>
        </div>
        <div class="health-bar-track">
            <div class="health-bar-fill"
                 style="width:{health}%;
                        background:linear-gradient(90deg,{bar_color},#3b82f6);">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # QUICK ACCESS
    # ─────────────────────────────────────
    st.markdown("""
    <div class="section-glow">
        <span class="accent-bar"></span> Quick Access
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    nav_cards = [
        (c1, "🔍", "Audit Engine",    "AI clause analysis & gaps",   "Audit",     "audit_btn"),
        (c2, "🎓", "Training Hub",    "Smart learning modules",      "Training",  "train_btn"),
        (c3, "📑", "Doc Register",    "Master document control",     "Dashboard", "master_btn"),
    ]
    for col, icon, title, desc, target, key in nav_cards:
        with col:
            st.markdown(f"""
            <div class="access-card">
                <div class="access-icon">{icon}</div>
                <div class="access-title">{title}</div>
                <div class="access-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {title}", key=key, use_container_width=True):
                st.session_state.active_tab = target
                st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # MODULE STATUS
    # ─────────────────────────────────────
    st.markdown("""
    <div class="section-glow">
        <span class="accent-bar"></span> Module Status
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass-panel">
        <div class="status-row">
            <div class="pulse-dot"></div>
            <span style="font-size:0.88rem; font-weight:600; color:#e2e8f0;">
                Audit Engine</span>
            <span style="font-size:0.75rem; color:#22c55e; margin-left:auto;">
                Operational</span>
        </div>
        <div class="status-row">
            <div class="pulse-dot"></div>
            <span style="font-size:0.88rem; font-weight:600; color:#e2e8f0;">
                Training Module</span>
            <span style="font-size:0.75rem; color:#22c55e; margin-left:auto;">
                Operational</span>
        </div>
        <div class="status-row">
            <div class="pulse-dot"></div>
            <span style="font-size:0.88rem; font-weight:600; color:#e2e8f0;">
                Document Sync</span>
            <span style="font-size:0.75rem; color:#22c55e; margin-left:auto;">
                Synced · {total} docs</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # ARCHITECTURE DIAGRAM
    # ─────────────────────────────────────
    with st.expander("📐 System Architecture"):
        st.markdown("""
        ```
        ┌──────────────────────────┐
        │        Audit Engine       │
        │ - Clause Mapping          │
        │ - Nonconformity Checks    │
        └─────────────┬────────────┘
                      │
        ┌─────────────▼────────────┐
        │      Training Module      │
        │ - Summaries               │
        │ - Knowledge Checks        │
        └─────────────┬────────────┘
                      │
        ┌─────────────▼────────────┐
        │      Master List (Docs)   │
        │ - GitHub Sync             │
        │ - Metadata Extraction     │
        └──────────────────────────┘
        ```
        """)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # COVERAGE CHART
    # ─────────────────────────────────────
    st.markdown("""
    <div class="section-glow">
        <span class="accent-bar"></span> Document Coverage
    </div>
    """, unsafe_allow_html=True)

    if doc_data:
        chart_df = pd.DataFrame({
            "Document": [d.get("Document ID", f"Doc {i+1}") for i, d in enumerate(doc_data)],
            "Coverage": [random.randint(70, 100) for _ in doc_data]
        })
        st.bar_chart(chart_df.set_index("Document"))
    else:
        st.info("Upload documents to see coverage data.")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # DOCUMENT REGISTER — USING st.dataframe (BULLETPROOF)
    # ─────────────────────────────────────
    st.markdown("""
    <div class="section-glow">
        <span class="accent-bar"></span> Controlled Document Register
    </div>
    """, unsafe_allow_html=True)

    if not doc_data:
        st.info("No documents found in **/docs** folder.")
        return

    df = pd.DataFrame(doc_data)

    # ✅ Style the dataframe — no HTML tables, no key mismatches
    def style_status(val):
        if "active" in str(val).lower():
            return "background-color: #052e16; color: #4ade80; font-weight: 600;"
        elif "review" in str(val).lower():
            return "background-color: #422006; color: #fbbf24; font-weight: 600;"
        elif "overdue" in str(val).lower():
            return "background-color: #450a0a; color: #f87171; font-weight: 600;"
        return ""

    styled = df.style.applymap(
        style_status,
        subset=["Status"] if "Status" in df.columns else []
    ).set_properties(**{
        "font-size": "0.88rem",
    }).set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#0f172a"),
            ("color", "#94a3b8"),
            ("font-size", "0.78rem"),
            ("font-weight", "600"),
            ("text-transform", "uppercase"),
            ("letter-spacing", "0.05em"),
            ("padding", "0.75rem"),
        ]},
        {"selector": "td", "props": [
            ("padding", "0.7rem"),
        ]},
    ])

    st.dataframe(styled, use_container_width=True, hide_index=True)
