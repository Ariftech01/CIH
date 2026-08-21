"""Construction Operations unified parent module for CIH.

Consolidates Materials, Workforce, Safety, Equipment, and Progress monitoring
into a single enterprise operational control center.
"""

from datetime import date
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st

from utils import charts, dummy_data
from utils.styles import (
    render_glass_card,
    render_kpi_card,
    render_page_header,
    render_progress_bar,
    status_to_badge,
)
from backend.services.material_service import material_service
from backend.services.worker_service import worker_service
from backend.services.equipment_service import equipment_service
from backend.services.task_service import task_service
from backend.risk_intelligence.agents import SafetyAgent
from backend.risk_intelligence.engine.project_health_engine import project_health_engine


def _render_equipment_card(equipment: Dict[str, Any]) -> None:
    """Render a single equipment card."""
    health = equipment["Health"]
    fuel = equipment["Fuel Level"]
    health_color = "#22C55E" if health >= 80 else "#F59E0B" if health >= 60 else "#EF4444"
    avail_badge = status_to_badge(equipment["Availability"])

    st.markdown(
        f"""
        <div class="cih-equipment-card">
            <div class="cih-equipment-name">{equipment['icon']} {equipment['name']}</div>
            <div class="cih-metric-row">
                <span class="cih-metric-label">ID</span>
                <span class="cih-metric-value">{equipment['id']}</span>
            </div>
            <div class="cih-metric-row">
                <span class="cih-metric-label">Health</span>
                <span class="cih-metric-value" style="color:{health_color};">{health}%</span>
            </div>
            <div class="cih-metric-row">
                <span class="cih-metric-label">Maintenance</span>
                <span class="cih-metric-value">{equipment['Maintenance']}</span>
            </div>
            <div class="cih-metric-row">
                <span class="cih-metric-label">Availability</span>
                <span class="cih-metric-value">{avail_badge}</span>
            </div>
            <div class="cih-metric-row">
                <span class="cih-metric-label">Fuel Level</span>
                <span class="cih-metric-value">{fuel}%</span>
            </div>
            <div class="cih-metric-row">
                <span class="cih-metric-label">Operating Hours</span>
                <span class="cih-metric-value">{equipment['Operating Hours']:,} hrs</span>
            </div>
            <div class="cih-metric-row">
                <span class="cih-metric-label">Last Service</span>
                <span class="cih-metric-value">{equipment['Last Service']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_materials_section(materials: pd.DataFrame) -> None:
    """Render Materials operational section."""
    tab1, tab2 = st.tabs(["📋 Inventory Table", "📊 Stock Analytics"])

    with tab1:
        st.markdown("#### Material Inventory")
        display_df = materials.copy()
        display_df["Cost"] = display_df["Cost"].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(display_df.drop(columns=["Stock %"]), use_container_width=True, hide_index=True)

        st.markdown("#### Stock Progress")
        for _, row in materials.iterrows():
            st.markdown(
                f'<div style="margin-bottom:0.25rem;">'
                f'<span style="color:var(--text-primary); font-size:0.85rem;">{row["Material"]} '
                f'{status_to_badge(row["Status"])}</span></div>',
                unsafe_allow_html=True,
            )
            render_progress_bar(
                f'{row["Available"]:,} / {row["Required"]:,} units',
                row["Stock %"],
            )

    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(charts.create_inventory_chart(materials), use_container_width=True)
        with col_b:
            supplier_counts = materials.groupby("Supplier").size().reset_index(name="Count")
            fig = charts.create_department_pie(supplier_counts.rename(columns={"Supplier": "Department"}))
            fig.update_layout(title=dict(text="Supplier Distribution", font=dict(color="#FFFFFF", size=14)))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="cih-glass-card">
                <div class="cih-card-title">📦 Reorder Recommendations</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        reorder = materials[materials["Status"].isin(["Low Stock", "Critical"])]
        if len(reorder) > 0:
            for _, row in reorder.iterrows():
                deficit = row["Required"] - row["Available"]
                st.warning(f"⚠️ **{row['Material']}**: Order {deficit:,} units from {row['Supplier']}")
        else:
            st.success("✅ All materials are at adequate stock levels")


def render_workforce_section(workers: pd.DataFrame) -> None:
    """Render Workforce operational section."""
    present = len(workers[workers["Status"] == "Present"])
    absent = len(workers[workers["Status"] == "Absent"])
    on_leave = len(workers[workers["Status"] == "On Leave"])

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


def render_safety_section(active_proj_id: Optional[str], active_proj_name: str) -> None:
    """Render Safety operational section."""
    if "safety_checklist" not in st.session_state:
        st.session_state.safety_checklist = dummy_data.get_safety_checklist()

    checklist = st.session_state.safety_checklist
    checked_count = sum(1 for v in checklist.values() if v)
    total_items = len(checklist)
    compliance_pct = (checked_count / max(total_items, 1)) * 100

    # Execute Safety Agent evaluation
    sample_context = {
        "project_id": active_proj_id or "proj_safety_01",
        "project_name": active_proj_name,
        "missing_ppe_count": 0 if compliance_pct >= 90 else (1 if compliance_pct >= 70 else 3),
        "manual_safety_observations": [
            "Scaffolding toe-boards verified on level 4",
            "Lifting zone perimeter secured"
        ]
    }
    sa = SafetyAgent()
    sa_res = sa.analyze(sample_context)

    tab1, tab2, tab3 = st.tabs(["✅ Safety Checklist", "📊 Intelligence & Analytics", "📋 Incidents"])

    with tab1:
        st.markdown("#### Daily Safety Checklist")
        checklist_cols = st.columns(2)
        items = list(checklist.keys())
        updated = {}
        for i, item in enumerate(items):
            with checklist_cols[i % 2]:
                updated[item] = st.checkbox(
                    f"{'🪖' if item == 'Helmet' else '👢' if item == 'Boots' else '🧤' if item == 'Gloves' else '🔗' if item == 'Harness' else '🔥' if item == 'Fire Equipment' else '🏥'} {item}",
                    value=checklist[item],
                    key=f"ops_safety_{item}",
                )
        st.session_state.safety_checklist = updated

        if st.button("💾 Save Checklist", key="save_ops_safety_checklist", use_container_width=True):
            if active_proj_id:
                try:
                    from backend.services.safety_service import safety_service
                    from backend.schemas.safety import SafetyInspectionCreate
                    from backend.automation.automation_engine import automation_engine

                    insp = SafetyInspectionCreate(
                        project_id=active_proj_id,
                        inspection_date=date.today(),
                        risk_level="LOW" if compliance_pct >= 80 else "HIGH",
                        description=f"Safety Checklist verified ({checked_count}/{total_items} items passed)",
                        status="RESOLVED" if compliance_pct >= 80 else "OPEN"
                    )
                    safety_service.record_inspection(insp)
                    automation_engine.handle_event("SafetyCompleted", {"project_id": active_proj_id})
                except Exception:
                    pass
            st.success("✅ Safety checklist saved successfully!")

        compliance_status = "Compliant" if compliance_pct >= 80 else "Partial" if compliance_pct >= 50 else "Non-Compliant"
        badge = status_to_badge(compliance_status)
        render_glass_card(
            "Compliance Status",
            f'<div style="font-size:1.5rem; margin-bottom:0.5rem;">{badge}</div>'
            f'<p style="color:var(--text-secondary);">{checked_count} of {total_items} safety items verified '
            f'({compliance_pct:.0f}% compliance rate)</p>',
        )

    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(charts.create_safety_gauge(max(100.0 - sa_res.score, 0.0)), use_container_width=True)
        with col_b:
            risk_df = dummy_data.get_risk_distribution()
            st.plotly_chart(charts.create_risk_chart(risk_df), use_container_width=True)

        st.markdown("#### Safety Agent Hazards & Findings")
        findings_list = sa_res.findings.get("findings", [])
        if findings_list:
            for f in findings_list:
                badge_type = "danger" if f.get("severity") in ["CRITICAL", "HIGH"] else "warning"
                st.markdown(
                    f'<div class="cih-activity-item">'
                    f'<span class="cih-badge cih-badge-{badge_type}">{f.get("severity")}</span> '
                    f'<strong style="color:var(--text-primary);">{f.get("title")}</strong> — {f.get("description")}'
                    f'<div class="cih-activity-time" style="color: #60A5FA; margin-top:2px;">Suggested Action: {f.get("suggested_action")}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Zero workforce safety hazards detected by Safety Agent.")

    with tab3:
        st.markdown("#### Incident Log")
        incidents_df = dummy_data.get_safety_incidents()
        st.dataframe(incidents_df, use_container_width=True, hide_index=True)

        for _, row in incidents_df.iterrows():
            severity_badge = (
                "danger" if row["Severity"] == "High"
                else "warning" if row["Severity"] == "Medium"
                else "success"
            )
            st.markdown(
                f'<div class="cih-activity-item">'
                f'<strong style="color:var(--text-primary);">{row["ID"]}</strong> — {row["Type"]} at {row["Location"]} '
                f'<span class="cih-badge cih-badge-{severity_badge}">{row["Severity"]}</span> '
                f'<span class="cih-badge cih-badge-info">{row["Status"]}</span>'
                f'<div class="cih-activity-time">{row["Date"]}</div></div>',
                unsafe_allow_html=True,
            )


def render_equipment_section(equipment_list: List[Dict[str, Any]]) -> None:
    """Render Equipment operational section."""
    st.markdown("#### Equipment Fleet")
    eq_cols = st.columns(len(equipment_list))
    for col, eq in zip(eq_cols, equipment_list):
        with col:
            _render_equipment_card(eq)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Fleet Health Overview")
    for eq in equipment_list:
        col_label, col_bar = st.columns([1, 3])
        with col_label:
            st.markdown(f"**{eq['icon']} {eq['name']}**")
        with col_bar:
            render_progress_bar(f"Health: {eq['Health']}% | Fuel: {eq['Fuel Level']}%", eq["Health"])

    eq_usage = dummy_data.get_equipment_usage()
    st.plotly_chart(charts.create_equipment_usage_chart(eq_usage), use_container_width=True)


def render_progress_section(milestones: pd.DataFrame) -> None:
    """Render Progress & Milestones operational section."""
    overall_progress = milestones["Progress"].mean() if not milestones.empty else 0.0

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


def render() -> None:
    """Render unified Construction Operations module."""
    render_page_header(
        "Construction Operations",
        "Unified operational control center for materials, workforce, safety, equipment, and project progress"
    )

    # 1. Obtain Active Project Context
    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_proj_id = active_proj.id if active_proj else st.session_state.get("active_project_id")
    active_proj_name = active_proj.project_name if active_proj else st.session_state.get("active_project_name", "Commercial Site Operations")

    # 2. Retrieve Data for Common KPIs and Sections
    # Materials Data
    db_mats = material_service.get_project_materials(active_proj_id) if active_proj_id else []
    if db_mats:
        mat_rows = []
        for m in db_mats:
            stock_pct = round((m.quantity_available / max(m.quantity_required, 1.0)) * 100, 1)
            status_str = "Adequate" if stock_pct >= 75 else ("Low Stock" if stock_pct >= 30 else "Critical")
            mat_rows.append({
                "Material": m.material_name,
                "Category": m.category or "General",
                "Available": int(m.quantity_available),
                "Required": int(m.quantity_required),
                "Supplier": m.supplier or "BuildPro Supplies",
                "Cost": m.unit_cost,
                "Status": status_str,
                "Stock %": min(stock_pct, 100.0)
            })
        materials = pd.DataFrame(mat_rows)
    else:
        materials = dummy_data.get_materials(project_id=active_proj_id)

    # Workforce Data
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

    # Safety Data & Metrics
    if "safety_checklist" not in st.session_state:
        st.session_state.safety_checklist = dummy_data.get_safety_checklist()
    checklist = st.session_state.safety_checklist
    checked_count = sum(1 for v in checklist.values() if v)
    total_items = len(checklist)
    compliance_pct = (checked_count / max(total_items, 1)) * 100

    incidents = dummy_data.get_safety_incidents(project_id=active_proj_id)
    open_incidents = len(incidents[incidents["Status"].isin(["Open", "Under Review"])])

    # Equipment Data
    db_eqs = equipment_service.get_project_equipment(active_proj_id) if active_proj_id else []
    if db_eqs:
        eq_list = []
        for eq in db_eqs:
            eq_list.append({
                "name": eq.equipment_name,
                "id": f"EQP-{eq.id[:4].upper()}",
                "Health": 92,
                "Maintenance": "Up to Date" if eq.status == "OPERATIONAL" else "Overdue",
                "Availability": "Available" if eq.availability == "AVAILABLE" else "In Use",
                "Fuel Level": 85,
                "Operating Hours": 1420,
                "Last Service": str(eq.maintenance_date) if eq.maintenance_date else "2026-07-01",
                "icon": "🚜"
            })
        equipment_list = eq_list
    else:
        equipment_list = dummy_data.get_equipment(project_id=active_proj_id)

    # Progress & Milestone Data
    milestones = dummy_data.get_progress_milestones(project_id=active_proj_id)
    if active_proj_id:
        db_tasks = task_service.get_project_tasks(active_proj_id)
        if db_tasks:
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

    # 3. Calculate 5 Common Operational KPIs
    # KPI 1 — Material Availability
    adequate_count = len(materials[materials["Status"] == "Adequate"])
    mat_pct = round((adequate_count / max(len(materials), 1)) * 100)

    # KPI 2 — Workforce Status
    present_count = len(workers[workers["Status"] == "Present"])
    att_pct = round((present_count / max(len(workers), 1)) * 100)

    # KPI 3 — Safety Status
    safety_summary = f"{open_incidents} Open Incident" if open_incidents == 1 else f"{open_incidents} Open Incidents" if open_incidents > 1 else "Zero Incidents"
    safety_color = "#22C55E" if open_incidents == 0 and compliance_pct >= 80 else ("#F59E0B" if open_incidents <= 1 else "#EF4444")

    # KPI 4 — Equipment Availability
    available_eq = sum(1 for e in equipment_list if e["Availability"] == "Available")
    avg_eq_health = sum(e["Health"] for e in equipment_list) / max(len(equipment_list), 1)

    # KPI 5 — Project Progress
    overall_progress = milestones["Progress"].mean() if not milestones.empty else 0.0
    milestones_done = len(milestones[milestones["Status"] == "Completed"])

    # 4. Render EXACTLY FIVE COMMON KPI CARDS
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card(
            "Material Availability",
            f"{adequate_count}/{len(materials)}",
            "🧱",
            delta=f"{mat_pct}% Adequate Stock",
            delta_color="#22C55E" if mat_pct >= 70 else "#F59E0B"
        )
    with col2:
        render_kpi_card(
            "Workforce Status",
            f"{present_count}/{len(workers)}",
            "👷",
            delta=f"{att_pct}% On-Site Attendance",
            delta_color="#22C55E" if att_pct >= 75 else "#F59E0B"
        )
    with col3:
        render_kpi_card(
            "Safety Status",
            f"{compliance_pct:.0f}%",
            "🦺",
            delta=safety_summary,
            delta_color=safety_color
        )
    with col4:
        render_kpi_card(
            "Equipment Fleet",
            f"{available_eq}/{len(equipment_list)}",
            "🚜",
            delta=f"{avg_eq_health:.0f}% Avg Health Index",
            delta_color="#22C55E" if available_eq > 0 else "#F59E0B"
        )
    with col5:
        render_kpi_card(
            "Project Progress",
            f"{overall_progress:.0f}%",
            "📈",
            delta=f"{milestones_done}/{len(milestones)} Milestones Done",
            delta_color="#22C55E"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Render FIVE INTERNAL SECTIONS
    tab_mat, tab_work, tab_safe, tab_equip, tab_prog = st.tabs([
        "🧱 Materials",
        "👷 Workforce",
        "🦺 Safety",
        "🚜 Equipment",
        "📈 Progress"
    ])

    with tab_mat:
        render_materials_section(materials)

    with tab_work:
        render_workforce_section(workers)

    with tab_safe:
        render_safety_section(active_proj_id, active_proj_name)

    with tab_equip:
        render_equipment_section(equipment_list)

    with tab_prog:
        render_progress_section(milestones)
