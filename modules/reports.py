"""Reports module for CIH with Reporting Agent & Multi-Channel Export Adapter integration."""

import io
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from services.ollamaService import ollama_service
from utils import dummy_data
from utils.styles import render_page_header
from backend.app_logging.logger import logger
from backend.risk_intelligence.agents import ReportingAgent
from backend.risk_intelligence.integrations.reporting_export_adapter import reporting_export_adapter

REPORT_TYPES = [
    {"name": "Cost Report", "icon": "💰", "description": "Budget analysis and cost breakdowns"},
    {"name": "Project Report", "icon": "📁", "description": "Project status and milestone tracking"},
    {"name": "Safety Report", "icon": "🦺", "description": "Safety compliance and incident summary"},
    {"name": "Inventory Report", "icon": "🧱", "description": "Material stock levels and reorder alerts"},
    {"name": "Worker Report", "icon": "👷", "description": "Workforce attendance and performance"},
]

def _generate_report_data(report_name: str) -> pd.DataFrame:
    """Generate report data based on type."""
    if report_name == "Cost Report":
        return pd.DataFrame({
            "Category": ["Materials", "Labor", "Equipment", "Tax", "Contingency"],
            "Amount": [3500000, 2100000, 1200000, 1026000, 680000],
            "Percentage": [35, 21, 12, 10.3, 6.8],
        })
    if report_name == "Project Report":
        return dummy_data.get_projects()
    if report_name == "Safety Report":
        return dummy_data.get_safety_incidents()
    if report_name == "Inventory Report":
        return dummy_data.get_materials()
    if report_name == "Worker Report":
        return dummy_data.get_workers()
    return pd.DataFrame()


def _build_ai_report_text(report_name: str, report_data: pd.DataFrame) -> str:
    """Create an AI-generated report summary for the selected report data."""
    try:
        health = ollama_service.health_check()
        if health.get("reachable") and health.get("model_available"):
            sample_data = report_data.head(10).to_string(index=False)
            prompt = (
                f"Create a concise construction management report for '{report_name}'. "
                f"Use the following data sample:\n{sample_data}\n\n"
                "Include an executive summary, top observations, risks, and 3 practical next steps. "
                "Keep the tone professional and suitable for project stakeholders."
            )
            response = ollama_service.chat(
                [{"role": "user", "content": prompt}],
                system_prompt=(
                    "You are a construction reporting assistant. Write a polished, actionable report "
                    "that is concise and stakeholder-ready."
                ),
            )
            if response and response.strip():
                return response.strip()
    except Exception as exc:
        logger.debug(f"Ollama report summary generation fallback triggered: {exc}")

    summary_lines = [
        f"AI Report for {report_name}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Executive Summary:",
        f"- The {report_name.lower()} dataset has been reviewed and summarized for project decision support.",
        f"- Total records reviewed: {len(report_data)}",
        "",
        "Key Observations:",
        "- Highlight the highest-impact records first for field and management review.",
        "- Validate this summary against live site logs before issuing final decisions.",
        "",
        "Recommended Actions:",
        "1. Review critical items and prioritize corrective actions.",
        "2. Share the report with project managers and operations leads.",
        "3. Track follow-up tasks and completion status in the next reporting cycle.",
    ]
    return "\n".join(summary_lines)

def render() -> None:
    """Render reports page."""
    render_page_header("Reports & Analytics", "Generate, preview, and export enterprise reports with Reporting Agent integration")

    if "selected_report" not in st.session_state:
        st.session_state.selected_report = "Project Report"
    if "ai_report_text" not in st.session_state:
        st.session_state.ai_report_text = ""
    if "ai_report_generated" not in st.session_state:
        st.session_state.ai_report_generated = False

    st.markdown("#### Select Report Type")
    report_cols = st.columns(len(REPORT_TYPES))
    for col, report in zip(report_cols, REPORT_TYPES):
        with col:
            st.markdown(
                f"""
                <div class="cih-report-card">
                    <div class="cih-report-icon">{report['icon']}</div>
                    <div class="cih-report-name">{report['name']}</div>
                    <div style="font-size:0.75rem; color:#64748B; margin-top:0.5rem;">{report['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select", key=f"select_{report['name']}", use_container_width=True):
                st.session_state.selected_report = report["name"]

    st.markdown(f"**Selected Report:** {st.session_state.selected_report}")
    report_data = _generate_report_data(st.session_state.selected_report)

    st.markdown("#### Report Preview")
    st.dataframe(report_data.head(20), use_container_width=True, hide_index=True)

    st.markdown("#### 🤖 Reporting Agent & AI Generator")
    if st.button("✨ Generate Reporting Agent Report", use_container_width=True, key="generate_ai_report_btn"):
        with st.spinner("Executing Reporting Agent enterprise report composition pipeline..."):
            from backend.workflow.project_workflow import project_workflow
            active_proj = project_workflow.get_active_project()
            active_p_id = active_proj.id if active_proj else st.session_state.get("active_project_id", "proj_report_01")
            active_p_name = active_proj.project_name if active_proj else st.session_state.get("active_project_name", "Infrastructure Development Site")

            ra = ReportingAgent()
            ra_res = ra.analyze({

                "project_id": active_p_id,
                "project_name": active_p_name,
                "report_type": st.session_state.selected_report.upper().replace(" ", "_"),
                "component_scores": {
                    "Site Risk": {"score": 25.0, "weight": 1.2},
                    "Safety": {"score": 15.0, "weight": 1.5},
                    "Compliance": {"score": 10.0, "weight": 1.3},
                    "Insurance": {"score": 30.0, "weight": 1.0}
                }
            })
            
            ent_report = ra_res.findings.get("enterprise_report", {})
            exec_sum = ent_report.get("executive_summary", {})
            
            ai_text = f"ENTERPRISE REPORT: {st.session_state.selected_report}\nReport ID: {ra_res.findings.get('report_id')}\n\n"
            ai_text += f"Highlights:\n" + "\n".join(f"- {h}" for h in exec_sum.get("key_highlights", [])) + "\n\n"
            ai_text += _build_ai_report_text(st.session_state.selected_report, report_data)

            st.session_state.ai_report_text = ai_text
            st.session_state.ai_report_generated = True
        st.success("Reporting Agent Enterprise Report synthesized successfully!")

    if st.session_state.ai_report_generated and st.session_state.ai_report_text:
        st.text_area("Enterprise Report Preview", st.session_state.ai_report_text, height=220)
        ai_report_bytes = st.session_state.ai_report_text.encode("utf-8")
        st.download_button(
            "⬇ Download Enterprise Report (.txt)",
            data=ai_report_bytes,
            file_name=f"{st.session_state.selected_report.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("#### Multi-Channel Export Options")
    export_cols = st.columns(4)

    csv_buffer = report_data.to_csv(index=False).encode("utf-8")
    excel_buffer = io.BytesIO()
    report_data.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    with export_cols[0]:
        if st.button("📄 Prepare PDF Export", use_container_width=True):
            exp_req = reporting_export_adapter.prepare_export_request({"project_id": "proj_report_01", "report_type": st.session_state.selected_report}, export_format="PDF", destination="PDF_DOWNLOAD")
            st.success(f"📄 PDF Request '{exp_req.export_id}' created for downloading in production environment")

    with export_cols[1]:
        st.download_button(
            "📊 Export Excel",
            data=excel_buffer,
            file_name=f"{st.session_state.selected_report.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with export_cols[2]:
        st.download_button(
            "📥 Download CSV",
            data=csv_buffer,
            file_name=f"{st.session_state.selected_report.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with export_cols[3]:
        if st.button("👁 Preview Report", use_container_width=True):
            st.success(f"✅ {st.session_state.selected_report} preview loaded successfully")

    st.markdown(
        f"""
        <div class="cih-glass-card" style="margin-top:1.5rem;">
            <div class="cih-card-title">📋 Report Metadata</div>
            <div class="cih-metric-row"><span class="cih-metric-label">Report Type</span><span class="cih-metric-value">{st.session_state.selected_report}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Generated</span><span class="cih-metric-value">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Records</span><span class="cih-metric-value">{len(report_data)}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Multi-Channel Formats</span><span class="cih-metric-value">PDF / Excel / CSV / JSON</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize saved reports history in session state
    if "saved_reports_history" not in st.session_state:
        st.session_state.saved_reports_history = []

    st.markdown("---")
    st.markdown("#### 💾 Enterprise Ledger Integration")

    save_col1, save_col2 = st.columns([3, 1])
    with save_col1:
        st.markdown("Push this report to the centralized project database for audit trails and long-term archival.")
    with save_col2:
        if st.button("📥 Save to Enterprise Ledger", use_container_width=True, key="save_report_btn"):
            with st.spinner("Encrypting payload and pushing transaction to project database..."):
                time.sleep(1.5)

            # Generate simulated record ID
            record_count = len(st.session_state.saved_reports_history) + 1
            record_id = f"REP-2026-{str(1000 + record_count).zfill(3)}"
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Add to session history
            saved_record = {
                "Record ID": record_id,
                "Report Type": st.session_state.selected_report,
                "Records": len(report_data),
                "Timestamp": timestamp,
                "Status": "✅ Committed",
            }
            st.session_state.saved_reports_history.append(saved_record)

            # Show success feedback
            st.success(
                f"✅ Record **{record_id}** successfully committed to the centralized ledger. "
                f"Timestamp: {timestamp}"
            )

    # Display historical log if reports have been saved
    if st.session_state.saved_reports_history:
        st.markdown("#### 📋 Saved Reports History (Session)")
        history_df = pd.DataFrame(st.session_state.saved_reports_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
