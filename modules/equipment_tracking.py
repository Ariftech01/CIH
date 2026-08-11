"""Equipment tracking module for CIH."""

import streamlit as st

from utils import dummy_data
from utils.styles import render_kpi_card, render_page_header, render_progress_bar, status_to_badge
from backend.services.equipment_service import equipment_service


def _render_equipment_card(equipment: dict) -> None:
    """Render a single equipment card."""
    health = equipment["Health"]
    fuel = equipment["Fuel Level"]
    health_color = "#22C55E" if health >= 80 else "#F59E0B" if health >= 60 else "#EF4444"
    avail_badge = status_to_badge(equipment["Availability"])
    maint_badge = status_to_badge("Maintenance" if equipment["Maintenance"] != "Up to Date" else "Compliant")

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


def render() -> None:
    """Render equipment tracking page."""
    render_page_header("Equipment Tracking", "Monitor fleet health, maintenance, and utilization")

    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_proj_id = active_proj.id if active_proj else st.session_state.get("active_project_id")
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
    available = sum(1 for e in equipment_list if e["Availability"] == "Available")
    in_use = sum(1 for e in equipment_list if e["Availability"] == "In Use")
    maintenance = sum(1 for e in equipment_list if e["Availability"] == "Maintenance")
    avg_health = sum(e["Health"] for e in equipment_list) / len(equipment_list)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Fleet", str(len(equipment_list)), "🚜")
    with col2:
        render_kpi_card("Available", str(available), "✅", delta="Ready for deployment", delta_color="#22C55E")
    with col3:
        render_kpi_card("In Use", str(in_use), "🔄")
    with col4:
        render_kpi_card("Avg Health", f"{avg_health:.0f}%", "💚")

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
    from utils import charts
    st.plotly_chart(charts.create_equipment_usage_chart(eq_usage), use_container_width=True)
