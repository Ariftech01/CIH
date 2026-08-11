"""Executive dashboard module for CIH with CRIE Risk Intelligence integration."""

import streamlit as st
from utils import charts, dummy_data
from utils.styles import render_glass_card, render_kpi_card, render_page_header, render_progress_bar
from utils.dashboard_components import (
    render_unified_risk_scorecard,
    render_agent_matrix_cards,
    render_executive_alerts,
    render_executive_recommendation_panel
)
from backend.analytics.analytics_engine import analytics_engine
from backend.risk_intelligence.engine.crie import risk_intelligence_engine
from backend.risk_intelligence.integrations.dashboard_context_builder import dashboard_context_builder

from backend.workflow.project_workflow import project_workflow

@st.cache_resource(show_spinner=False)
def _get_cached_dashboard_context(project_id: str = "proj_exec_01", project_name: str = "Commercial Infrastructure Hub"):
    sample_context = {
        "project_id": project_id,
        "project_name": project_name,
        "incidents_list": [
            {"id": "INC_01", "type": "DAMAGE", "severity": "MODERATE", "financial_impact": 15000.0, "description": f"Formwork inspection completed for {project_name}"}
        ],
        "policy_records": [
            {"id": "POL_CAR", "name": "Contractor All Risk", "status": "ACTIVE"}
        ],
        "equipment_list": [
            {"id": "EQ_01", "name": "Tower Crane Alpha", "replacement_value": 250000.0, "insurance_status": "COVERED"}
        ]
    }
    crie_output = risk_intelligence_engine.execute_analysis_pipeline(sample_context, assessment_id=f"exec_dash_{project_id}")
    return dashboard_context_builder.build_dashboard_context(crie_output)


def render() -> None:
    """Render the unified executive dashboard."""
    render_page_header("Executive Dashboard", "Real-time enterprise overview of construction operations & risk intelligence")

    active_proj = project_workflow.get_active_project()
    active_id = active_proj.id if active_proj else st.session_state.get("active_project_id", "proj_exec_01")
    active_name = active_proj.project_name if active_proj else st.session_state.get("active_project_name", "Commercial Infrastructure Hub")

    projects = dummy_data.get_projects()
    workers = dummy_data.get_workers(project_id=active_id)
    kpis = dummy_data.get_dashboard_kpis(projects, workers, project_id=active_id)

    # Blend PostgreSQL Analytics Engine KPIs
    db_kpis = analytics_engine.get_dashboard_kpis(project_id=active_id)
    if db_kpis.get("total_projects", 0) > 0:
        kpis["total_projects"] = db_kpis["total_projects"]
        kpis["active_projects"] = db_kpis["active_projects"]
        kpis["completed_projects"] = db_kpis["completed_projects"]
        if db_kpis.get("total_workers", 0) > 0:
            kpis["workers"] = db_kpis["total_workers"]
        if db_kpis.get("total_equipment", 0) > 0:
            kpis["equipment"] = db_kpis["total_equipment"]

    # 1. Fetch CRIE Unified Risk Intelligence & Build Dashboard Context (cached per active project)
    dash_ctx = _get_cached_dashboard_context(active_id, active_name)

    # 2. Render Unified CRIE Scorecard & 5-Agent Matrix
    render_unified_risk_scorecard(
        overall_score=dash_ctx.overall_risk_score,
        risk_level=dash_ctx.risk_level,
        health_status=dash_ctx.health_status,
        health_index=dash_ctx.health_index
    )

    render_agent_matrix_cards(dash_ctx.component_scores)

    st.markdown("<br>", unsafe_allow_html=True)

    # Top KPI Cards
    kpi_cols = st.columns(4)
    kpi_data = [
        ("Total Projects", str(kpis["total_projects"]), "📊", f"+{kpis['active_projects']} active", "#3B82F6"),
        ("Active Projects", str(kpis["active_projects"]), "🏗️", "Currently in progress", "#22C55E"),
        ("Completed Projects", str(kpis["completed_projects"]), "✅", "Delivered on record", "#60A5FA"),
        ("Budget Utilization", f"{kpis['budget_utilization']}%", "💰", "Of total allocated budget", "#F59E0B"),
    ]
    for col, (label, value, icon, delta, color) in zip(kpi_cols, kpi_data):
        with col:
            render_kpi_card(label, value, icon, delta, color)

    kpi_cols2 = st.columns(4)
    kpi_data2 = [
        ("Workers On Site", str(kpis["workers"]), "👷", "Present today", "#22C55E"),
        ("Equipment Units", str(kpis["equipment"]), "🚜", "Fleet tracked", "#3B82F6"),
        ("Safety Score", f"{kpis['safety_score']}%", "🦺", "+2.5% vs last month", "#22C55E"),
        ("Avg Completion", f"{kpis['project_completion']}%", "📈", "Across all projects", "#60A5FA"),
    ]
    for col, (label, value, icon, delta, color) in zip(kpi_cols2, kpi_data2):
        with col:
            render_kpi_card(label, value, icon, delta, color)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        timeline_df = dummy_data.get_timeline_data(project_id=active_id)
        st.plotly_chart(charts.create_timeline_chart(timeline_df), use_container_width=True)
    with col2:
        budget_df = dummy_data.get_budget_allocation(project_id=active_id)
        st.plotly_chart(charts.create_budget_pie_chart(budget_df), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        status_df = dummy_data.get_project_status_counts(projects)
        st.plotly_chart(charts.create_status_donut_chart(status_df), use_container_width=True)
    with col4:
        worker_dist = dummy_data.get_worker_distribution(workers)
        st.plotly_chart(charts.create_worker_bar_chart(worker_dist), use_container_width=True)

    # Equipment & Material
    col5, col6 = st.columns(2)
    with col5:
        eq_usage = dummy_data.get_equipment_usage(project_id=active_id)
        st.plotly_chart(charts.create_equipment_usage_chart(eq_usage), use_container_width=True)
    with col6:
        materials = dummy_data.get_materials(project_id=active_id)
        st.plotly_chart(charts.create_inventory_chart(materials), use_container_width=True)

    # Executive Alerts, Recommendations & Activities
    col7, col8, col9 = st.columns(3)

    with col7:
        render_executive_alerts(dash_ctx.critical_alerts)

    with col8:
        render_executive_recommendation_panel(dash_ctx.top_recommendations)

    with col9:
        notifications = dummy_data.get_notifications()
        notif_html = ""
        icon_map = {"warning": "⚠️", "info": "ℹ️", "success": "✅", "danger": "🚨"}
        for n in notifications:
            badge = n["type"] if n["type"] in ("success", "warning", "danger") else "info"
            notif_html += (
                f'<div class="cih-activity-item">'
                f'{icon_map.get(n["type"], "ℹ️")} '
                f'<span class="cih-badge cih-badge-{badge}">{n["type"].upper()}</span><br>'
                f'<span class="cih-activity-text">{n["message"]}</span></div>'
            )
        render_glass_card("🔔 Enterprise Notifications", notif_html)

    # Quick Actions & System Health
    st.markdown("<br>", unsafe_allow_html=True)
    col10, col11 = st.columns([1, 1])

    with col10:
        st.markdown(
            """
            <div class="cih-glass-card">
                <div class="cih-card-title">⚡ Quick Actions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        qa_cols = st.columns(3)
        actions = [
            ("➕ New Project", "create_project"),
            ("📊 Generate Report", "reports"),
            ("🦺 Safety Audit", "safety"),
        ]
        for col, (label, _) in zip(qa_cols, actions):
            with col:
                st.button(label, key=f"qa_{label}", use_container_width=True)

    with col11:
        st.markdown(
            """
            <div class="cih-glass-card">
                <div class="cih-card-title">💚 System Health</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        systems = [
            ("CRIE Risk Engine", 100, "Operational"),
            ("Safety Agent", 99.8, "Operational"),
            ("Compliance Agent", 100, "Operational"),
            ("Insurance Agent", 98.5, "Operational"),
            ("Reporting Agent", 100, "Operational"),
        ]
        for name, uptime, status in systems:
            render_progress_bar(f"{name} — {status}", uptime)
