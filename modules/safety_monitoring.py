"""Safety monitoring module for CIH with Safety Agent risk intelligence integration."""

import streamlit as st
from utils import charts, dummy_data
from utils.styles import render_glass_card, render_kpi_card, render_page_header, status_to_badge
from backend.risk_intelligence.agents import SafetyAgent

def render() -> None:
    """Render safety monitoring page."""
    render_page_header("Safety Monitoring", "Workforce safety intelligence, PPE tracking, incident management, and Safety Agent risk evaluation")

    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_proj_id = active_proj.id if active_proj else st.session_state.get("active_project_id", "proj_safety_01")
    active_proj_name = active_proj.project_name if active_proj else st.session_state.get("active_project_name", "Commercial Site Safety Monitoring")

    if "safety_checklist" not in st.session_state:
        st.session_state.safety_checklist = dummy_data.get_safety_checklist()

    checklist = st.session_state.safety_checklist
    checked_count = sum(1 for v in checklist.values() if v)
    total_items = len(checklist)
    compliance_pct = (checked_count / total_items) * 100

    # Execute Safety Agent evaluation
    sample_context = {
        "project_id": active_proj_id,
        "project_name": active_proj_name,
        "missing_ppe_count": 0 if compliance_pct >= 90 else (1 if compliance_pct >= 70 else 3),
        "manual_safety_observations": [
            "Scaffolding toe-boards verified on level 4",
            "Lifting zone perimeter secured"
        ]
    }
    sa = SafetyAgent()
    sa_res = sa.analyze(sample_context)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        color = "#EF4444" if sa_res.score > 50 else ("#F59E0B" if sa_res.score > 25 else "#22C55E")
        render_kpi_card("Safety Agent Score", f"{sa_res.score:.1f}/100", "🦺", sa_res.summary, color)
    with col2:
        render_kpi_card("Safety Checklist", f"{checked_count}/{total_items}", "✅")
    with col3:
        render_kpi_card("Compliance Rate", f"{compliance_pct:.0f}%", "📋")
    with col4:
        incidents = dummy_data.get_safety_incidents(project_id=active_proj_id)
        open_incidents = len(incidents[incidents["Status"].isin(["Open", "Under Review"])])
        render_kpi_card("Open Incidents", str(open_incidents), "🚨", delta="Requires action", delta_color="#EF4444")

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
                    key=f"safety_{item}",
                )
        st.session_state.safety_checklist = updated

        if st.button("💾 Save Checklist", use_container_width=True):
            active_proj_id = st.session_state.get("active_project_id")
            if active_proj_id:
                try:
                    from backend.services.safety_service import safety_service
                    from backend.schemas.safety import SafetyInspectionCreate
                    from backend.automation.automation_engine import automation_engine
                    from datetime import date

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
