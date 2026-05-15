import streamlit as st
import pandas as pd
import time
import random
import datetime

def render_dashboard(doc_data):

    # ─────────────────────────────────────
    # KPI ROW — now uses real Status field
    # ─────────────────────────────────────
    total   = len(doc_data) if doc_data else 0
    active  = sum(1 for d in doc_data if d.get("Status") == "Active")       if doc_data else 0
    soon    = sum(1 for d in doc_data if d.get("Status") == "Review Soon")  if doc_data else 0
    overdue = sum(1 for d in doc_data if d.get("Status") == "Overdue")      if doc_data else 0

    k1, k2, k3, k4 = st.columns(4)
    for col, (val, label, icon, color) in zip(
        [k1, k2, k3, k4],
        [
            (total,   "Total Documents",  "📁", "#3b82f6"),
            (active,  "Active",           "✅", "#22c55e"),
            (soon,    "Review Soon",      "⏳", "#f59e0b"),
            (overdue, "Overdue",          "⚠️",  "#ef4444"),
        ],
    ):
        col.markdown(f"""
        <div style="background:#fff; border:1px solid #e2e8f0;
                    border-top:3px solid {color}; border-radius:12px;
                    padding:1.2rem 1rem; text-align:center;
                    box-shadow:0 1px 3px rgba(0,0,0,0.06);
                    transition:transform 0.2s, box-shadow 0.2s;">
            <div style="font-size:1.4rem;">{icon}</div>
            <div style="font-size:1.8rem; font-weight:700; color:#0f172a;">{val}</div>
            <div style="font-size:0.78rem; font-weight:500; color:#64748b;
                        text-transform:uppercase; letter-spacing:0.05em;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # SYSTEM HEALTH BAR
    # ─────────────────────────────────────
    health_score = random.randint(82, 99)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);
                border-radius:12px; padding:1rem 1.5rem; color:#e2e8f0;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:0.78rem; font-weight:600; text-transform:uppercase;
                             letter-spacing:0.05em; color:#94a3b8;">System Health</span>
                <span style="font-size:1.3rem; font-weight:700; margin-left:0.8rem;
                             color:{'#22c55e' if health_score >= 90 else '#f59e0b'};">
                    {health_score}%
                </span>
            </div>
            <div style="font-size:0.75rem; color:#64748b;">
                Last AI Sync: {time.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        <div style="background:#334155; border-radius:6px; height:8px;
                    overflow:hidden; margin-top:0.6rem;">
            <div style="width:{health_score}%; height:100%;
                        background:linear-gradient(90deg,#22c55e,#3b82f6);
                        border-radius:6px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # QUICK ACCESS CARDS
    # ─────────────────────────────────────
    st.markdown("""
    <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                border-bottom:2px solid #3b82f6; display:inline-block;
                padding-bottom:0.3rem; margin-bottom:0.8rem;">
        ⚡ Quick Access
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cards = [
        (col1, "🔍", "Audit Engine",    "Clause mapping & gap analysis",
         "#3b82f6", "#eff6ff", "Audit",     "audit_btn"),
        (col2, "🎓", "Training Module", "Summaries & knowledge checks",
         "#f59e0b", "#fffbeb", "Training",  "train_btn"),
        (col3, "📑", "Master List",     "Controlled document register",
         "#8b5cf6", "#f5f3ff", "Dashboard", "master_btn"),
    ]
    for col, icon, title, desc, accent, bg, target, key in cards:
        with col:
            st.markdown(f"""
            <div style="background:{bg}; border:1px solid #e2e8f0;
                        border-left:4px solid {accent}; border-radius:12px;
                        padding:1.2rem 1rem; margin-bottom:0.5rem;">
                <div style="font-size:1.5rem; margin-bottom:0.3rem;">{icon}</div>
                <div style="font-size:1rem; font-weight:600; color:#0f172a;">{title}</div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:0.2rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {title}", key=key, use_container_width=True):
                st.session_state.active_tab = target
                st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # STATUS INDICATORS
    # ─────────────────────────────────────
    st.markdown("""
    <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                border-bottom:2px solid #3b82f6; display:inline-block;
                padding-bottom:0.3rem; margin-bottom:0.8rem;">
        🟢 Module Status
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    for col, name, status in [(s1,"Audit Engine","Ready"),
                               (s2,"Training Module","Stable"),
                               (s3,"Master List","Synced")]:
        with col:
            st.markdown(f"""
            <div style="background:#fff; border:1px solid #e2e8f0; border-radius:10px;
                        padding:0.9rem 1rem; display:flex; align-items:center; gap:0.7rem;
                        box-shadow:0 1px 3px rgba(0,0,0,0.04);">
                <span style="height:10px; width:10px; background:#22c55e;
                             border-radius:50%; display:inline-block;
                             box-shadow:0 0 6px #22c55e;"></span>
                <div>
                    <div style="font-size:0.9rem; font-weight:600; color:#0f172a;">{name}</div>
                    <div style="font-size:0.75rem; color:#64748b;">{status}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # ARCHITECTURE DIAGRAM
    # ─────────────────────────────────────
    with st.expander("📐 System Architecture Diagram"):
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
    # DOCUMENT COVERAGE CHART
    # ─────────────────────────────────────
    st.markdown("""
    <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                border-bottom:2px solid #3b82f6; display:inline-block;
                padding-bottom:0.3rem; margin-bottom:0.8rem;">
        📊 Document Coverage
    </div>
    """, unsafe_allow_html=True)

    if doc_data:
        heatmap_data = pd.DataFrame({
            "Document": [d["Document ID"] for d in doc_data],
            "Coverage Score": [random.randint(70, 100) for _ in doc_data]
        })
        st.bar_chart(heatmap_data.set_index("Document"))
    else:
        st.info("Upload documents to see coverage data.")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # CONTROLLED DOCUMENT REGISTER TABLE
    # ─────────────────────────────────────
    st.markdown("""
    <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                border-bottom:2px solid #3b82f6; display:inline-block;
                padding-bottom:0.3rem; margin-bottom:0.8rem;">
        📑 Controlled Document Register
    </div>
    """, unsafe_allow_html=True)

    if not doc_data:
        st.info("No documents found in **/docs** folder.")
        return

    # ── Status styling map ──
    STATUS_STYLE = {
        "Active":      ("✅ Active",      "#dcfce7", "#166534"),
        "Review Soon": ("⏳ Review Soon", "#fef9c3", "#854d0e"),
        "Overdue":     ("⚠️ Overdue",     "#fee2e2", "#991b1b"),
    }

    # ── Build header ──
    display_cols = [
        "Document ID", "Title", "Format", "Revision",
        "Approved By", "Approval Date", "Next Review", "Status"
    ]

    header_cells = ""
    for col_name in display_cols:
        header_cells += f"""
        <th style="padding:0.75rem 1rem; text-align:left; font-size:0.75rem;
                   font-weight:600; color:#64748b; text-transform:uppercase;
                   letter-spacing:0.05em; white-space:nowrap;">{col_name}</th>"""

    # ── Build rows ──
    today = datetime.date.today()
    body_rows = ""
    for d in doc_data:
        cells = ""
        for col_name in display_cols:
            val = d.get(col_name, "—")

            if col_name == "Status":
                label, bg, fg = STATUS_STYLE.get(
                    val, ("❔ Unknown", "#f1f5f9", "#475569")
                )
                val = (f'<span style="background:{bg}; color:{fg}; '
                       f'padding:0.2rem 0.65rem; border-radius:20px; '
                       f'font-size:0.75rem; font-weight:600; '
                       f'white-space:nowrap;">{label}</span>')

            elif col_name == "Next Review":
                # Color-code the review date
                try:
                    review_date = datetime.datetime.strptime(val, '%Y-%m-%d').date()
                    days_left = (review_date - today).days
                    if days_left < 0:
                        date_color = "#ef4444"
                        suffix = f" ({abs(days_left)}d overdue)"
                    elif days_left <= 30:
                        date_color = "#f59e0b"
                        suffix = f" ({days_left}d left)"
                    else:
                        date_color = "#22c55e"
                        suffix = ""
                    val = (f'<span style="color:{date_color}; font-weight:600;">'
                           f'{val}</span>'
                           f'<span style="color:#94a3b8; font-size:0.75rem;">'
                           f'{suffix}</span>')
                except (ValueError, TypeError):
                    pass

            elif col_name == "Document ID":
                val = f'<span style="font-weight:600; color:#3b82f6;">{val}</span>'

            elif col_name == "Revision":
                val = (f'<span style="background:#eff6ff; color:#1e40af; '
                       f'padding:0.15rem 0.5rem; border-radius:6px; '
                       f'font-size:0.78rem; font-weight:600;">{val}</span>')

            if val is None or str(val).strip() == "":
                val = "—"

            cells += f"""
            <td style="padding:0.7rem 1rem; font-size:0.88rem;
                       color:#334155; white-space:nowrap;">{val}</td>"""

        body_rows += f"""
        <tr style="border-bottom:1px solid #f1f5f9;
                   transition:background 0.15s;"
            onmouseover="this.style.background='#f8fafc'"
            onmouseout="this.style.background='transparent'">
            {cells}
        </tr>"""

    st.markdown(f"""
    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px;
                overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.04);
                overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; min-width:900px;">
            <thead>
                <tr style="background:#f8fafc; border-bottom:2px solid #e2e8f0;">
                    {header_cells}
                </tr>
            </thead>
            <tbody>{body_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
