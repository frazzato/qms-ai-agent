import streamlit as st
import pandas as pd
from datetime import datetime

def render_dashboard(doc_data):

    # ── KPI Row ──
    total   = len(doc_data) if doc_data else 0
    controlled = sum(1 for d in doc_data if d.get("status") == "controlled")   if doc_data else 0
    pending    = sum(1 for d in doc_data if d.get("status") == "pending")      if doc_data else 0
    overdue    = sum(1 for d in doc_data if d.get("status") == "overdue")      if doc_data else 0

    k1, k2, k3, k4 = st.columns(4)
    for col, (val, label, icon, color) in zip(
        [k1, k2, k3, k4],
        [
            (total,      "Total Documents",     "📁", "#3b82f6"),
            (controlled, "Controlled",          "✅", "#22c55e"),
            (pending,    "Pending Review",      "⏳", "#f59e0b"),
            (overdue,    "Overdue / Non-Conf.", "⚠️",  "#ef4444"),
        ],
    ):
        col.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fff, #f8fafc);
            border: 1px solid #e2e8f0;
            border-top: 3px solid {color};
            border-radius: 12px;
            padding: 1.2rem 1rem;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: transform 0.2s, box-shadow 0.2s;
        ">
            <div style="font-size:1.4rem;">{icon}</div>
            <div style="font-size:1.8rem; font-weight:700; color:#0f172a;">{val}</div>
            <div style="font-size:0.78rem; font-weight:500; color:#64748b;
                        text-transform:uppercase; letter-spacing:0.05em;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Document Table ──
    if doc_data:
        st.markdown("""
        <div style="font-size:1.05rem; font-weight:600; color:#0f172a;
                    border-bottom:2px solid #3b82f6; display:inline-block;
                    padding-bottom:0.3rem; margin-bottom:0.8rem;">
            📄 Document Register
        </div>
        """, unsafe_allow_html=True)

        STATUS_STYLE = {
            "controlled": ("✅ Controlled", "#dcfce7", "#166534"),
            "pending":    ("⏳ Pending",    "#fef9c3", "#854d0e"),
            "overdue":    ("⚠️ Overdue",    "#fee2e2", "#991b1b"),
        }

        rows_html = ""
        for d in doc_data:
            label, bg, fg = STATUS_STYLE.get(
                d.get("status", ""), ("❔ Unknown", "#f1f5f9", "#475569")
            )
            badge = (f'<span style="background:{bg}; color:{fg}; padding:0.2rem 0.65rem;'
                     f' border-radius:20px; font-size:0.75rem; font-weight:600;">'
                     f'{label}</span>')

            rows_html += f"""
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:0.7rem 1rem; font-weight:500;">{d.get('name','—')}</td>
                <td style="padding:0.7rem 1rem; color:#64748b;">{d.get('type','—')}</td>
                <td style="padding:0.7rem 1rem; color:#64748b;">{d.get('revision','—')}</td>
                <td style="padding:0.7rem 1rem;">{badge}</td>
                <td style="padding:0.7rem 1rem; color:#94a3b8; font-size:0.85rem;">
                    {d.get('last_modified','—')}</td>
            </tr>"""

        st.markdown(f"""
        <div style="background:#fff; border:1px solid #e2e8f0; border-radius:12px;
                    overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr style="background:#f8fafc; border-bottom:2px solid #e2e8f0;">
                        <th style="padding:0.75rem 1rem; text-align:left; font-size:0.78rem;
                                   font-weight:600; color:#64748b; text-transform:uppercase;
                                   letter-spacing:0.05em;">Document</th>
                        <th style="padding:0.75rem 1rem; text-align:left; font-size:0.78rem;
                                   font-weight:600; color:#64748b; text-transform:uppercase;">Type</th>
                        <th style="padding:0.75rem 1rem; text-align:left; font-size:0.78rem;
                                   font-weight:600; color:#64748b; text-transform:uppercase;">Rev</th>
                        <th style="padding:0.75rem 1rem; text-align:left; font-size:0.78rem;
                                   font-weight:600; color:#64748b; text-transform:uppercase;">Status</th>
                        <th style="padding:0.75rem 1rem; text-align:left; font-size:0.78rem;
                                   font-weight:600; color:#64748b; text-transform:uppercase;">Modified</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("Upload documents to the **docs/** folder to populate the register.")
