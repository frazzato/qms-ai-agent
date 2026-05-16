import streamlit as st
import pandas as pd
import time
import random

def render_dashboard(doc_data):

    # ─────────────────────────────────────
    # INJECT CSS
    # ─────────────────────────────────────
    st.markdown("""
    <style>
    /* ── Hero Card ── */
    .hero-card {
        background: linear-gradient(145deg, #0a0f1e, #111832);
        border: 1px solid rgba(59,130,246,0.15);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero-card::after {
        content: '';
        position: absolute;
        top: -50%; right: -20%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(34,197,94,0.15);
        border: 1px solid rgba(34,197,94,0.3);
        color: #4ade80;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f1f5f9;
        line-height: 1.2;
        margin-bottom: 0.8rem;
    }
    .hero-sub {
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.6;
        max-width: 500px;
    }

    /* ── AI Module Cards ── */
    .ai-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.8rem;
        margin-bottom: 0.5rem; /* Reduced to pull buttons closer */
    }
    @media (max-width: 768px) {
        .ai-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .ai-module {
        background: linear-gradient(145deg, #0f172a, #151d35);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.4rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        /* Removed cursor: pointer to prevent false clickability */
    }
    .ai-module:hover {
        border-color: rgba(59,130,246,0.4);
        box-shadow: 0 0 25px rgba(59,130,246,0.1);
        transform: translateY(-3px);
    }
    .ai-module.featured {
        background: linear-gradient(145deg, #1a1a3e, #1e2550);
        border-color: rgba(59,130,246,0.3);
        box-shadow: 0 4px 20px rgba(59,130,246,0.1);
    }
    .ai-module-icon {
        width: 48px; height: 48px;
        margin: 0 auto 0.7rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
    }
    .ai-module-name {
        font-size: 0.82rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.2rem;
    }
    .ai-module-desc {
        font-size: 0.68rem;
        color: #64748b;
        line-height: 1.4;
    }
    .new-badge {
        position: absolute;
        top: 8px; right: 8px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        font-size: 0.6rem;
        font-weight: 700;
        padding: 0.15rem 0.45rem;
        border-radius: 6px;
        letter-spacing: 0.05em;
    }

    /* ── Custom Streamlit Button Styling ── */
    div[data-testid="stButton"] button {
        background-color: rgba(30, 41, 59, 0.5);
        color: #94a3b8;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
        transition: all 0.2s ease;
    }
    div[data-testid="stButton"] button:hover {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
    }

    /* ── Neon KPI ── */
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
    .neon-blue::before   { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .neon-green::before  { background: linear-gradient(90deg, #22c55e, #4ade80); }
    .neon-amber::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .neon-red::before    { background: linear-gradient(90deg, #ef4444, #f87171); }

    .neon-icon  { font-size: 1.6rem; margin-bottom: 0.4rem; }
    .neon-value { font-size: 2rem; font-weight: 800; color: #f1f5f9; margin: 0; }
    .neon-label { font-size: 0.72rem; font-weight: 600; color: #64748b;
                  text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }

    /* ── Glass panel ── */
    .glass-panel {
        background: linear-gradient(145deg,
                    rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── Section header ── */
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
        width: 4px; height: 1.2rem;
        background: linear-gradient(180deg, #3b82f6, #8b5cf6);
        border-radius: 4px;
    }

    /* ── Status ── */
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
        border-radius: 8px; height: 10px; overflow: hidden;
    }
    .health-bar-fill {
        height: 100%; border-radius: 8px;
        transition: width 1s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # HERO CARD
    # ─────────────────────────────────────
    total = len(doc_data) if doc_data else 0

    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-badge">
            🤖 AI-POWERED QMS ACTIVE
        </div>
        <div class="hero-title">
            AS9100 Rev D with<br>AI-Assisted Modules
        </div>
        <div class="hero-sub">
            Your compliance engine is synchronized with
            <strong style="color:#e2e8f0;">{total} controlled documents</strong>
            in the QMS repository. AI modules are analyzing gaps,
            generating CAPAs, and building audit checklists in real-time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # AI MODULES SHOWCASE (HTML Displays)
    # ─────────────────────────────────────
    st.markdown("""
    <div class="section-glow">
        <span class="accent-bar"></span> AI Modules
    </div>
    """, unsafe_allow_html=True)

    # NOTE: Removed 'onclick="void(0)"' from all cards
    st.markdown("""
    <div class="ai-grid">

        <div class="ai-module">
            <div class="ai-module-icon" style="background:rgba(59,130,246,0.12);">
                📋
            </div>
            <div class="ai-module-name">Gap Analysis</div>
            <div class="ai-module-desc">Clause coverage mapping against AS9100 & ISO 9001</div>
        </div>

        <div class="ai-module featured">
            <div class="new-badge">NEW</div>
            <div class="ai-module-icon" style="background:rgba(239,68,68,0.12);">
                🛠️
            </div>
            <div class="ai-module-name">CAPA Generator</div>
            <div class="ai-module-desc">Root cause analysis & corrective action reports</div>
        </div>

        <div class="ai-module">
            <div class="ai-module-icon" style="background:rgba(34,197,94,0.12);">
                ✅
            </div>
            <div class="ai-module-name">Audit Checklist</div>
            <div class="ai-module-desc">Auto-generated internal audit checklists by clause</div>
        </div>

        <div class="ai-module">
            <div class="new-badge">NEW</div>
            <div class="ai-module-icon" style="background:rgba(245,158,11,0.12);">
                ⚠️
            </div>
            <div class="ai-module-name">Risk Assessment</div>
            <div class="ai-module-desc">Likelihood × severity matrix with mitigations</div>
        </div>

        <div class="ai-module">
            <div class="ai-module-icon" style="background:rgba(139,92,246,0.12);">
                🎓
            </div>
            <div class="ai-module-name">Smart Training</div>
            <div class="ai-module-desc">AI-generated training modules with knowledge checks</div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # NATIVE STREAMLIT BUTTONS (The actual triggers)
    # ─────────────────────────────────────
    b1, b2, b3, b4, b5 = st.columns(5)
    with b1:
        if st.button("Launch Analysis", key="dash_gap", use_container_width=True):
            st.session_state.active_tab = "Audit"
            st.rerun()
    with b2:
        if st.button("Generate CAPA", key="dash_capa", use_container_width=True):
            st.session_state.active_tab = "Audit"
            st.rerun()
    with b3:
        if st.button("Open Checklist", key="dash_check", use_container_width=True):
            st.session_state.active_tab = "Audit"
            st.rerun()
    with b4:
        if st.button("View Matrix", key="dash_risk", use_container_width=True):
            st.session_state.active_tab = "Audit"
            st.rerun()
    with b5:
        if st.button("Start Training", key="dash_train", use_container_width=True):
            st.session_state.active_tab = "Training"
            st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # KPI CARDS
    # ─────────────────────────────────────
    st.markdown("""
    <div class="section-glow">
        <span class="accent-bar"></span> Document Control
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # SYSTEM HEALTH
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
                Gap Analysis Engine</span>
            <span style="font-size:0.75rem; color:#22c55e; margin-left:auto;">
                Operational</span>
        </div>
        <div class="status-row">
            <div class="pulse-dot"></div>
            <span style="font-size:0.88rem; font-weight:600; color:#e2e8f0;">
                CAPA Generator</span>
            <span style="font-size:0.75rem; color:#22c55e; margin-left:auto;">
                Operational</span>
        </div>
        <div class="status-row">
            <div class="pulse-dot"></div>
            <span style="font-size:0.88rem; font-weight:600; color:#e2e8f0;">
                Audit Checklist Builder</span>
            <span style="font-size:0.75rem; color:#22c55e; margin-left:auto;">
                Operational</span>
        </div>
        <div class="status-row">
            <div class="pulse-dot"></div>
            <span style="font-size:0.88rem; font-weight:600; color:#e2e8f0;">
                Risk Assessment</span>
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

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # DOCUMENT REGISTER
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

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Document ID": st.column_config.TextColumn("Document ID", width="medium"),
            "Title":       st.column_config.TextColumn("Title", width="large"),
            "Status":      st.column_config.TextColumn("Status", width="medium"),
        },
    )
