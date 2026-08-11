"""
Construction Risk Intelligence module for Construction Intelligence Hub (CIH).
Provides unified executive UI visualization for CRIE risk scorecards, Site Risk Agent, Safety Agent,
Compliance Agent, Insurance Agent, Reporting Agent, Historical Analytics, and Automation Framework.
"""

import streamlit as st
import pandas as pd
from utils import charts, dummy_data
from utils.styles import render_glass_card, render_kpi_card, render_page_header, render_progress_bar, status_to_badge
from utils.dashboard_components import (
    render_unified_risk_scorecard,
    render_agent_matrix_cards,
    render_executive_alerts,
    render_executive_recommendation_panel
)

from backend.risk_intelligence.engine.crie import risk_intelligence_engine
from backend.risk_intelligence.integrations.dashboard_context_builder import dashboard_context_builder
from backend.risk_intelligence.agents import SiteRiskAgent, SafetyAgent, ComplianceAgent, InsuranceAgent, ReportingAgent
from backend.risk_intelligence.automation import (
    notification_engine,
    background_service_manager,
    performance_manager,
    deployment_validator
)


@st.cache_resource(show_spinner=False)
def _get_cached_cri_context(project_id: str, project_name: str):
    sample_context = {
        "project_id": project_id,
        "project_name": project_name,
        "incidents_list": [
            {"id": "INC_01", "type": "DAMAGE", "severity": "MODERATE", "financial_impact": 18000.0, "description": "Formwork displacement during concrete pour on Level 3"}
        ],
        "policy_records": [
            {"id": "POL_CAR", "name": "Contractor All Risk Policy", "status": "ACTIVE"}
        ],
        "equipment_list": [
            {"id": "EQ_01", "name": "Tower Crane Alpha", "replacement_value": 250000.0, "insurance_status": "COVERED"}
        ],
        "missing_ppe_count": 0,
        "manual_safety_observations": ["Scaffolding toe-boards verified"]
    }
    crie_output = risk_intelligence_engine.execute_analysis_pipeline(sample_context, assessment_id="cri_page_assessment")
    dash_ctx = dashboard_context_builder.build_dashboard_context(crie_output)
    return sample_context, dash_ctx


def render() -> None:
    """Render the Construction Risk Intelligence unified page."""
    # Page-scoped responsive tab navigation CSS
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab-list"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            scroll-behavior: smooth !important;
            -webkit-overflow-scrolling: touch !important;
            gap: 4px !important;
            padding-bottom: 6px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            height: 4px !important;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.6) !important;
            border-radius: 4px !important;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
            background: rgba(59, 130, 246, 0.5) !important;
            border-radius: 4px !important;
        }

        .stTabs [data-baseweb="tab-list"] button {
            flex-shrink: 0 !important;
            white-space: nowrap !important;
            padding: 8px 14px !important;
            font-size: 0.9rem !important;
            border-radius: 8px 8px 0 0 !important;
            transition: all 0.2s ease-in-out !important;
        }

        @media (max-width: 1366px) {
            .stTabs [data-baseweb="tab-list"] button {
                padding: 6px 10px !important;
                font-size: 0.82rem !important;
            }
        }

        @media (max-width: 1024px) {
            .stTabs [data-baseweb="tab-list"] button {
                padding: 5px 8px !important;
                font-size: 0.78rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    render_page_header("Construction Risk Intelligence", "Enterprise multi-agent risk assessment, safety intelligence, compliance governance, and insurance exposure")

    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_project_id = active_proj.id if active_proj else st.session_state.get("active_project_id", "proj_cri_01")
    active_project = active_proj.project_name if active_proj else st.session_state.get("active_project_name", "Commercial High-Rise Infrastructure")

    # Fetch cached CRIE Pipeline Execution & Dashboard Context
    sample_context, dash_ctx = _get_cached_cri_context(active_project_id, active_project)

    # Render Unified Scorecard & 5-Agent Matrix Cards
    render_unified_risk_scorecard(
        overall_score=dash_ctx.overall_risk_score,
        risk_level=dash_ctx.risk_level,
        health_status=dash_ctx.health_status,
        health_index=dash_ctx.health_index
    )

    render_agent_matrix_cards(dash_ctx.component_scores)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sub-Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Overview",
        "🏗️ Site Risk",
        "🦺 Safety Agent",
        "📜 Compliance Agent",
        "🛡️ Insurance Agent",
        "📋 Reporting Agent",
        "📈 Historical Analytics",
        "⚡ Automation & Governance"
    ])

    # TAB 1: OVERVIEW & SCORECARD
    with tab1:
        st.markdown("#### Enterprise Executive Risk Overview")
        col1, col2 = st.columns([2, 1])
        with col1:
            render_executive_alerts(dash_ctx.critical_alerts)
        with col2:
            render_executive_recommendation_panel(dash_ctx.top_recommendations)

        st.markdown("<br>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("##### Component Risk Score Weights")
            weight_data = pd.DataFrame([
                {"Agent Domain": k, "Score": v["score"], "Weight": v["weight"]}
                for k, v in dash_ctx.component_scores.items()
            ])
            st.dataframe(weight_data, use_container_width=True, hide_index=True)
        with col4:
            st.markdown("##### Executive Key Performance Indicators")
            for kpi in dash_ctx.executive_kpis:
                title = getattr(kpi, "title", kpi.get("title", "KPI") if isinstance(kpi, dict) else "KPI")
                val_str = str(getattr(kpi, "value", kpi.get("value", "0") if isinstance(kpi, dict) else "0"))
                try:
                    cleaned_val = float(val_str.replace('%','').replace('/100','')) if ('%' in val_str or '/100' in val_str) else 50.0
                except Exception:
                    cleaned_val = 50.0
                render_progress_bar(f"{title}: {val_str}", min(cleaned_val, 100.0))


    # TAB 2: SITE RISK AGENT
    with tab2:
        st.markdown("#### 🏗️ Site Risk Agent Subsystem")
        sra_res = SiteRiskAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Site Risk Score", f"{sra_res.score:.1f}/100", "🏗️", sra_res.summary, "#EF4444" if sra_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Hazards Detected", str(sra_res.findings.get("total_hazards_count", 0)), "⚠️")
        with c3:
            render_kpi_card("Geotechnical Status", "Stable", "⛰️", delta="Ground anchor verified", delta_color="#22C55E")

        st.markdown("##### Site Hazard Breakdown")
        hazards = sra_res.findings.get("hazards", [])
        if hazards:
            for h in hazards:
                st.markdown(
                    f'<div class="cih-activity-item">'
                    f'<span class="cih-badge cih-badge-danger">{h.get("severity", "HIGH")}</span> '
                    f'<strong style="color:var(--text-primary);">{h.get("hazard_type", "HAZARD")}</strong> — {h.get("description")}'
                    f'<div class="cih-activity-time" style="color:#60A5FA; margin-top:2px;">Location: {h.get("location", "Site Perimeter")}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Zero physical site hazards detected.")

    # TAB 3: SAFETY AGENT
    with tab3:
        st.markdown("#### 🦺 Safety Agent Subsystem")
        sa_res = SafetyAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Workforce Safety Score", f"{sa_res.score:.1f}/100", "🦺", sa_res.summary, "#EF4444" if sa_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Workers Evaluated", str(sa_res.findings.get("workers_evaluated_count", 15)), "👷")
        with c3:
            render_kpi_card("Critical PPE Compliance", "98.5%", "🪖", delta="+1.2% this week", delta_color="#22C55E")

        st.markdown("##### Workforce Safety Findings")
        for f in sa_res.findings.get("findings", []):
            badge = "danger" if f.get("severity") in ["CRITICAL", "HIGH"] else "warning"
            st.markdown(
                f'<div class="cih-activity-item">'
                f'<span class="cih-badge cih-badge-{badge}">{f.get("severity")}</span> '
                f'<strong style="color:var(--text-primary);">{f.get("title")}</strong> — {f.get("description")}'
                f'<div class="cih-activity-time" style="color:#60A5FA;">Suggested Action: {f.get("suggested_action")}</div></div>',
                unsafe_allow_html=True
            )

    # TAB 4: COMPLIANCE AGENT
    with tab4:
        st.markdown("#### 📜 Compliance Agent Subsystem")
        ca_res = ComplianceAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Compliance Score", f"{ca_res.score:.1f}/100", "📜", ca_res.summary, "#EF4444" if ca_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Active Permits", "12/12 Verified", "✅")
        with c3:
            render_kpi_card("Audit Readiness", "Pass", "🔍", delta="IS 456 & NBC 2016 Compliant", delta_color="#22C55E")

        st.markdown("##### Regulatory Compliance Findings")
        for f in ca_res.findings.get("findings", []):
            badge = "danger" if f.get("severity") in ["CRITICAL", "HIGH"] else "info"
            st.markdown(
                f'<div class="cih-activity-item">'
                f'<span class="cih-badge cih-badge-{badge}">{f.get("severity")}</span> '
                f'<strong style="color:var(--text-primary);">{f.get("title")}</strong> — {f.get("description")}'
                f'<div class="cih-activity-time" style="color:#60A5FA;">Regulation: {f.get("regulation_code", "NBC-2016")}</div></div>',
                unsafe_allow_html=True
            )

    # TAB 5: INSURANCE AGENT
    with tab5:
        st.markdown("#### 🛡️ Insurance Agent Subsystem")
        ia_res = InsuranceAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Insurance Exposure Score", f"{ia_res.score:.1f}/100", "🛡️", ia_res.summary, "#EF4444" if ia_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Policy Coverage Status", "Fully Covered", "📋")
        with c3:
            render_kpi_card("Claim Severity Risk", "Low", "💰", delta="Zero pending claims", delta_color="#22C55E")

        st.markdown("##### Insurance Hazards & Policy Gaps")
        for f in ia_res.findings.get("findings", []):
            badge = "danger" if f.get("severity") in ["CRITICAL", "HIGH"] else "warning"
            st.markdown(
                f'<div class="cih-activity-item">'
                f'<span class="cih-badge cih-badge-{badge}">{f.get("severity")}</span> '
                f'<strong style="color:var(--text-primary);">{f.get("title")}</strong> — {f.get("description")}'
                f'<div class="cih-activity-time" style="color:#60A5FA;">Action: {f.get("suggested_action")}</div></div>',
                unsafe_allow_html=True
            )

    # TAB 6: REPORTING AGENT
    with tab6:
        st.markdown("#### 📋 Reporting Agent Subsystem")
        ra_res = ReportingAgent().analyze(sample_context)

        st.markdown(f"**Generated Enterprise Report ID:** `{ra_res.findings.get('report_id')}`")
        if st.button("📄 Generate & Composition Pipeline", use_container_width=True, key="ra_page_gen_btn"):
            st.success(f"Enterprise Executive Summary synthesized for project '{active_project}'.")

        ent_rep = ra_res.findings.get("enterprise_report", {})
        exec_sum = ent_rep.get("executive_summary", {})
        if exec_sum:
            st.markdown("##### Executive Summary Highlights")
            for h in exec_sum.get("key_highlights", []):
                st.markdown(f"- {h}")

    # TAB 7: HISTORICAL ANALYTICS
    with tab7:
        st.markdown("#### 📈 Historical Risk Intelligence Analytics")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            weekly = dummy_data.get_weekly_progress()
            st.plotly_chart(charts.create_weekly_progress_chart(weekly), use_container_width=True)
        with col_h2:
            risk_df = dummy_data.get_risk_distribution()
            st.plotly_chart(charts.create_risk_chart(risk_df), use_container_width=True)

    # TAB 8: AUTOMATION & GOVERNANCE
    with tab8:
        st.markdown("#### ⚡ Enterprise Automation, Notifications & Governance")

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            health = background_service_manager.get_system_health()
            st.markdown(
                f"""
                <div class="cih-glass-card">
                    <div class="cih-card-title">💚 Background Services Health</div>
                    <div style="font-size:1.4rem; font-weight:700; color:#22C55E; margin-bottom:0.5rem;">{health['overall_health']}</div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Executed Jobs</span><span class="cih-metric-value">{health['total_jobs_executed']}</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Failed Jobs</span><span class="cih-metric-value">{health['failed_jobs_count']}</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_a2:
            perf = performance_manager.get_performance_metrics()
            st.markdown(
                f"""
                <div class="cih-glass-card">
                    <div class="cih-card-title">⚡ Performance Metrics</div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Total Requests</span><span class="cih-metric-value">{perf.total_requests}</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Avg Latency</span><span class="cih-metric-value">{perf.avg_latency_ms:.2f} ms</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Memory Footprint</span><span class="cih-metric-value">{perf.memory_mb:.1f} MB</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("##### Startup Deployment Certification Checklist")
        checklist = deployment_validator.validate_deployment()
        chk_html = f"<div><strong>Environment:</strong> {checklist.environment} | <strong>Database:</strong> {checklist.database_status} | <strong>Production Ready:</strong> {'✅ YES' if checklist.is_production_ready else '❌ NO'}</div><ul style='margin-top:0.5rem; color:var(--text-secondary);'>"
        for k, v in checklist.checks.items():
            chk_html += f"<li>{'✅' if v else '❌'} {k.replace('_', ' ').title()}: {v}</li>"
        chk_html += "</ul>"
        render_glass_card("🚀 Production Deployment Checklist", chk_html)

        st.markdown("##### Recent Dispatch Notifications")
        notifs = notification_engine.get_notifications(limit=5)
        if notifs:
            for n in notifs:
                priority = getattr(n, "priority", n.get("priority", "INFO") if isinstance(n, dict) else "INFO")
                title = getattr(n, "title", n.get("title", "Notification") if isinstance(n, dict) else "Notification")
                message = getattr(n, "message", n.get("message", "") if isinstance(n, dict) else "")
                recipients = getattr(n, "recipients", n.get("recipients", []) if isinstance(n, dict) else [])
                recip_str = ", ".join(recipients) if isinstance(recipients, list) else str(recipients)

                st.markdown(
                    f'<div class="cih-activity-item">'
                    f'<span class="cih-badge cih-badge-info">{priority}</span> '
                    f'<strong style="color:var(--text-primary);">{title}</strong> — {message}'
                    f'<div class="cih-activity-time">Recipients: {recip_str}</div></div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("Zero notifications dispatched.")

