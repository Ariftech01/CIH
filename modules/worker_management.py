import pandas as pd
import streamlit as st

from utils import charts, dummy_data
from utils.styles import render_kpi_card, render_page_header, status_to_badge
from backend.services.worker_service import worker_service


def render() -> None:
    """Render worker management page."""
    render_page_header("Worker Management", "Workforce tracking, attendance, and performance")

    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_proj_id = active_proj.id if active_proj else st.session_state.get("active_project_id")
    db_workers = worker_service.get_project_workers(active_proj_id) if active_proj_id else []
    if db_workers:
        w_rows = []
        for w in db_workers:
            w_rows.append({
                "Employee ID": f"EMP-{w.id[:4].upper()}",
                "Name": w.worker_name,
                "Role": w.designation or "Mason",
                "Department": "Civil Construction",
                "Status": "Present" if w.attendance == "PRESENT" else "On Leave",
                "Performance": 4.5,
                "Wage (₹)": w.daily_wage
            })
        workers = pd.DataFrame(w_rows)
    else:
        workers = dummy_data.get_workers(project_id=active_proj_id)
    present = len(workers[workers["Status"] == "Present"])
    absent = len(workers[workers["Status"] == "Absent"])
    on_leave = len(workers[workers["Status"] == "On Leave"])
    avg_performance = workers["Performance"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Workers", str(len(workers)), "👷")
    with col2:
        render_kpi_card("Present Today", str(present), "✅", delta=f"{present/len(workers)*100:.0f}% attendance", delta_color="#22C55E")
    with col3:
        render_kpi_card("On Leave", str(on_leave), "🏖️")
    with col4:
        render_kpi_card("Avg Performance", f"{avg_performance:.1f}/5.0", "⭐", delta="Above target", delta_color="#22C55E")

    tab1, tab2 = st.tabs(["📋 Employee Directory", "📊 Analytics"])

    with tab1:
        st.markdown("#### Workforce Directory")
        display_df = workers.copy()
        display_df["Performance"] = display_df["Performance"].apply(lambda x: f"{'⭐' * int(x)}{'☆' * (5 - int(x))} ({x})")
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=450)

        st.markdown("#### Status Overview")
        status_cols = st.columns(3)
        for col, (status, count) in zip(status_cols, [("Present", present), ("Absent", absent), ("On Leave", on_leave)]):
            with col:
                badge_type = "success" if status == "Present" else "danger" if status == "Absent" else "warning"
                st.markdown(
                    f'<div class="cih-kpi-card"><div class="cih-kpi-label">{status}</div>'
                    f'<div class="cih-kpi-value">{count}</div>'
                    f'<div style="margin-top:0.5rem;">{status_to_badge(status)}</div></div>',
                    unsafe_allow_html=True,
                )

    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            attendance_df = dummy_data.get_attendance_data(workers)
            st.plotly_chart(charts.create_attendance_chart(attendance_df), use_container_width=True)
        with col_b:
            dept_df = dummy_data.get_worker_distribution(workers)
            st.plotly_chart(charts.create_department_pie(dept_df), use_container_width=True)

        role_dist = workers.groupby("Role").size().reset_index(name="Count").sort_values("Count", ascending=True)
        fig = charts.create_worker_bar_chart(role_dist.rename(columns={"Role": "Department"}))
        fig.update_layout(title=dict(text="Role Distribution", font=dict(color="#FFFFFF", size=14)))
        st.plotly_chart(fig, use_container_width=True)
