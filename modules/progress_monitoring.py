"""Progress and Project Health monitoring module for CIH with ProjectHealthEngine integration."""

import streamlit as st
from utils import charts, dummy_data
from utils.styles import render_kpi_card, render_page_header, render_progress_bar, status_to_badge
from backend.services.task_service import task_service
from backend.risk_intelligence.engine.project_health_engine import project_health_engine

def render() -> None:
    """Render progress monitoring & Project Health page."""
    render_page_header("Progress & Project Health Monitoring", "Track milestones, project health index, operational performance, and construction timelines")

    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_proj_id = active_proj.id if active_proj else st.session_state.get("active_project_id", "proj_health_01")
    milestones = dummy_data.get_progress_milestones(project_id=active_proj_id)
    if active_proj_id:
        db_tasks = task_service.get_project_tasks(active_proj_id)
        if db_tasks:
            import pandas as pd
            m_rows = []
            for t in db_tasks:
                m_rows.append({
                    "Milestone": t.task_name,
                    "Start": "2026-01-15",
                    "End": str(t.due_date) if t.due_date else "2026-06-30",
                    "Progress": t.completion_percentage,
                    "Status": "Completed" if t.status == "COMPLETED" else ("In Progress" if t.status == "IN_PROGRESS" else "Pending")
                })
            milestones = pd.DataFrame(m_rows)

    overall_progress = milestones["Progress"].mean()
    completed = len(milestones[milestones["Status"] == "Completed"])
    in_progress = len(milestones[milestones["Status"] == "In Progress"])

    # Compute Project Health Index from ProjectHealthEngine
    health_res = project_health_engine.calculate_project_health(
        overall_risk_score=25.0,
        component_scores={"Site": {"score": 20.0}, "Safety": {"score": 15.0}},
        schedule_delay_days=0,
        cost_overrun_pct=2.5
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Overall Progress", f"{overall_progress:.0f}%", "📈")
    with col2:
        render_kpi_card("Project Health Index", f"{health_res['health_index']:.1f}%", "💚", f"Status: {health_res['status']}", "#22C55E")
    with col3:
        render_kpi_card("Milestones Done", f"{completed}/{len(milestones)}", "✅")
    with col4:
        render_kpi_card("On Schedule", "Yes", "⏱️", delta="2 days ahead", delta_color="#22C55E")

    tab1, tab2, tab3 = st.tabs(["📊 Overview & Health", "📅 Milestones", "📈 Trends"])

    with tab1:
        st.markdown("#### Project Completion & Health Breakdown")
        render_progress_bar("Overall Project Completion", overall_progress)

        for _, row in milestones.iterrows():
            badge = status_to_badge(row["Status"])
            st.markdown(
                f'<div style="margin:0.5rem 0;">{badge} <strong style="color:var(--text-primary);">{row["Milestone"]}</strong></div>',
                unsafe_allow_html=True,
            )
            render_progress_bar(f'{row["Start"]} → {row["End"]}', row["Progress"])

        st.plotly_chart(charts.create_gantt_placeholder(milestones), use_container_width=True)

    with tab2:
        st.markdown("#### Milestone Tracker")
        display_df = milestones.copy()
        display_df["Progress"] = display_df["Progress"].apply(lambda x: f"{x}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        for _, row in milestones.iterrows():
            st.markdown(
                f"""
                <div class="cih-glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="cih-card-title">{row['Milestone']}</span>
                        {status_to_badge(row['Status'])}
                    </div>
                    <div class="cih-metric-row">
                        <span class="cih-metric-label">Timeline</span>
                        <span class="cih-metric-value">{row['Start']} → {row['End']}</span>
                    </div>
                    <div class="cih-metric-row">
                        <span class="cih-metric-label">Progress</span>
                        <span class="cih-metric-value">{row['Progress']}%</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            weekly = dummy_data.get_weekly_progress()
            st.plotly_chart(charts.create_weekly_progress_chart(weekly), use_container_width=True)
        with col_b:
            monthly = dummy_data.get_monthly_progress()
            st.plotly_chart(charts.create_monthly_progress_chart(monthly), use_container_width=True)
