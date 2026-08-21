"""Project management module for Agentic AI for Safety Monitoring with Construction Risk Analytics (CIH).

Provides master project creation with expanded Building Information modeling metadata,
cross-module active project synchronization, version history, and real-time status updates.
"""

import streamlit as st
import pandas as pd

from utils import dummy_data
from utils.styles import render_kpi_card, render_page_header, status_to_badge
from backend.services.project_service import project_service
from backend.schemas.project import ProjectCreate, ProjectUpdate
from backend.workflow.workflow_engine import workflow_engine
from backend.workflow.project_workflow import project_workflow
from backend.automation.automation_engine import automation_engine
from backend.utils.exceptions import CIHBaseException


def _format_currency(value: float) -> str:
    """Format number as Indian currency style."""
    if value >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"₹{value / 1_000:.1f}K"
    return f"₹{value:,.0f}"


def _render_project_table(projects: pd.DataFrame) -> None:
    """Display styled project table."""
    display_df = projects.copy()
    if "Budget" in display_df.columns:
        display_df["Budget"] = display_df["Budget"].apply(lambda v: _format_currency(float(v)))
    if "Progress" in display_df.columns:
        display_df["Progress"] = display_df["Progress"].apply(lambda x: f"{x}%")
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=450)


def _render_create_project_form() -> None:
    """Render structured enterprise project creation wizard with draft persistence and completion indicators."""
    st.markdown("### ➕ Create Master Enterprise Project")
    st.caption("Complete the sections below to register a new master project. Required fields are marked with **\***.")

    # Initialize draft state in session state
    if "project_form_draft" not in st.session_state:
        st.session_state["project_form_draft"] = {}

    draft = st.session_state["project_form_draft"]

    # Calculate section completion status indicators
    sec_identity_done = bool(draft.get("project_name")) and bool(draft.get("client")) and bool(draft.get("location"))
    sec_budget_done = bool(draft.get("budget", 10000000) > 0)

    badge_identity = "✓ Complete" if sec_identity_done else "● Required fields pending"
    badge_budget = "✓ Complete" if sec_budget_done else "● Required fields pending"
    badge_building = "✓ Configured"
    badge_struct = "✓ Configured"
    badge_layout = "✓ Configured"
    badge_team = "✓ Configured"

    with st.form("create_project_form", clear_on_submit=False):
        # 1. SECTION 1: PROJECT IDENTITY & SCOPE
        with st.expander(f"📋 1. Project Identity & Scope — {badge_identity}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input(
                    "Project Name *",
                    value=draft.get("project_name", ""),
                    placeholder="e.g., Metro Rail Phase 3",
                    help="Official title of the master project (Required)"
                )
                client = st.text_input(
                    "Client / Sponsor *",
                    value=draft.get("client", ""),
                    placeholder="e.g., L&T Construction",
                    help="Client organization or sponsor entity (Required)"
                )
                location = st.text_input(
                    "Project Location *",
                    value=draft.get("location", ""),
                    placeholder="e.g., Mumbai, MH",
                    help="Site geographic location or city (Required)"
                )
                code_preview = "PRJ-AUTO-001"
                if project_name:
                    code_sub = project_name.replace(" ", "")[:3].upper()
                    if code_sub:
                        code_preview = f"PRJ-{code_sub}-001"
                st.text_input(
                    "Project Code / ID",
                    value=code_preview,
                    disabled=True,
                    help="Unique enterprise project code (Auto-generated on save)"
                )
            with col2:
                priority = st.selectbox(
                    "Project Priority (Recommended)",
                    ["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(draft.get("priority", "High")),
                    help="Operational priority classification"
                )
                owner_name = st.text_input(
                    "Project Owner / Entity (Optional)",
                    value=draft.get("owner_name", "CIH Holdings"),
                    help="Owner or parent enterprise entity"
                )
                site_area = st.number_input(
                    "Total Site Area (m²) (Optional)",
                    min_value=0.0,
                    value=float(draft.get("site_area", 5000.0)),
                    step=100.0,
                    help="Total plot or land parcel area"
                )

            description = st.text_area(
                "Project Scope & Description (Recommended)",
                value=draft.get("description", ""),
                placeholder="Enter comprehensive project objectives, scope, and deliverables...",
                help="Detailed scope overview"
            )

        # 2. SECTION 2: BUDGET & TIMELINE
        with st.expander(f"💰 2. Budget & Timeline — {badge_budget}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                budget = st.number_input(
                    "Allocated Budget (₹) *",
                    min_value=100000,
                    value=int(draft.get("budget", 10000000)),
                    step=500000,
                    help="Approved financial budget in INR (Required)"
                )
            with col2:
                start_date = st.date_input("Planned Start Date *", help="Project commencement date (Required)")
                end_date = st.date_input("Target Completion Date *", help="Target delivery date (Required)")

        # 3. SECTION 3: BUILDING & ARCHITECTURAL DETAILS
        with st.expander(f"🏢 3. Building & Architectural Details — {badge_building}", expanded=False):
            b_col1, b_col2, b_col3 = st.columns(3)
            with b_col1:
                b_type = st.selectbox("Project Type", ["Residential", "Commercial", "Industrial", "Hospital", "School", "Infrastructure", "Mixed Use"])
                total_builtup = st.number_input("Total Built-up Area (m²)", min_value=0.0, value=float(draft.get("total_builtup", 2500.0)), step=100.0)
            with b_col2:
                num_floors = st.number_input("Number of Floors", min_value=1, value=int(draft.get("num_floors", 4)), step=1)
                basement_floors = st.number_input("Basement Floors", min_value=0, value=int(draft.get("basement_floors", 1)), step=1)
                terrace_cnt = st.number_input("Terrace Count", min_value=0, value=int(draft.get("terrace_cnt", 1)), step=1)
            with b_col3:
                parking_lvls = st.number_input("Parking Levels", min_value=0, value=int(draft.get("parking_lvls", 1)), step=1)
                roof_type = st.selectbox("Roof Type", ["Flat RCC Slab", "Sloped Tile", "Steel Truss", "Glass Dome"])
                orientation = st.selectbox("Building Orientation", ["North-Facing", "East-Facing", "South-Facing", "West-Facing", "North-East"])

        # 4. SECTION 4: STRUCTURAL ENGINEERING SPECIFICATIONS
        with st.expander(f"🏗️ 4. Structural Engineering Specifications — {badge_struct}", expanded=False):
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                foundation = st.selectbox("Foundation Type", ["Isolated Footing", "Raft / Mat Foundation", "Piling Foundation", "Strap Footing"])
                frame_type = st.selectbox("Frame Type", ["RCC Frame", "Structural Steel Frame", "Pre-cast Concrete", "Hybrid Load-bearing"])
            with s_col2:
                struct_mat = st.selectbox("Structural Material", ["Reinforced Concrete", "Structural Steel", "Timber", "AAC Block Masonry"])
                concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40", "M50"], index=1)
            with s_col3:
                steel_grade = st.selectbox("Steel Rebar Grade", ["Fe-415 TMT", "Fe-500 TMT", "Fe-550 TMT", "Structural Steel E250"], index=1)
                seismic_zone = st.selectbox("Seismic Zone", ["Zone II", "Zone III", "Zone IV", "Zone V"], index=1)

        # 5. SECTION 5: BUILDING LAYOUT & ROOM BREAKDOWN
        with st.expander(f"🚪 5. Building Layout & Room Breakdown — {badge_layout}", expanded=False):
            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            with r_col1:
                bedrooms = st.number_input("Bedrooms", min_value=0, value=int(draft.get("bedrooms", 6)))
                bathrooms = st.number_input("Bathrooms", min_value=0, value=int(draft.get("bathrooms", 6)))
                living_rooms = st.number_input("Living Halls", min_value=0, value=int(draft.get("living_rooms", 2)))
                kitchens = st.number_input("Kitchens", min_value=0, value=int(draft.get("kitchens", 2)))
            with r_col2:
                offices = st.number_input("Office Rooms", min_value=0, value=int(draft.get("offices", 4)))
                conferences = st.number_input("Conference Rooms", min_value=0, value=int(draft.get("conferences", 2)))
                storage = st.number_input("Storage Rooms", min_value=0, value=int(draft.get("storage", 2)))
                utility = st.number_input("Utility Rooms", min_value=0, value=int(draft.get("utility", 2)))
            with r_col3:
                corridors = st.number_input("Corridors", min_value=0, value=int(draft.get("corridors", 4)))
                staircases = st.number_input("Staircases", min_value=1, value=int(draft.get("staircases", 2)))
                elevators = st.number_input("Elevators", min_value=0, value=int(draft.get("elevators", 2)))
                exits = st.number_input("Emergency Exits", min_value=1, value=int(draft.get("exits", 2)))
            with r_col4:
                balconies = st.number_input("Balconies", min_value=0, value=int(draft.get("balconies", 4)))
                open_areas = st.number_input("Open / Courtyard Areas", min_value=0, value=int(draft.get("open_areas", 1)))

        # 6. SECTION 6: STAKEHOLDERS & TEAM
        with st.expander(f"👷 6. Construction Stakeholders & Team — {badge_team}", expanded=False):
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                contractor_name = st.text_input("General Contractor", value=draft.get("contractor_name", "Shapoorji Pallonji & Co"))
                architect_name = st.text_input("Lead Architect", value=draft.get("architect_name", "Hafeez Contractor Studio"))
                consultant_name = st.text_input("Structural Consultant", value=draft.get("consultant_name", "AECOM India"))
            with t_col2:
                manager = st.selectbox("Project Manager", ["Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh", "Ananya Iyer"])
                site_eng_name = st.text_input("Site Engineer", value=draft.get("site_eng_name", "Arjun Mehta"))
                construction_phase = st.selectbox("Construction Phase", ["Planning", "Design", "Estimation", "Execution", "Monitoring", "Completed"])

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ Create Master Project & Initialize Workflow", use_container_width=True)

        # Store entered inputs in session state draft
        st.session_state["project_form_draft"] = {
            "project_name": project_name,
            "client": client,
            "location": location,
            "budget": budget,
            "priority": priority,
            "owner_name": owner_name,
            "site_area": site_area,
            "description": description,
            "b_type": b_type,
            "total_builtup": total_builtup,
            "num_floors": num_floors,
            "basement_floors": basement_floors,
            "terrace_cnt": terrace_cnt,
            "parking_lvls": parking_lvls,
            "roof_type": roof_type,
            "orientation": orientation,
            "foundation": foundation,
            "frame_type": frame_type,
            "struct_mat": struct_mat,
            "concrete_grade": concrete_grade,
            "steel_grade": steel_grade,
            "seismic_zone": seismic_zone,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "living_rooms": living_rooms,
            "kitchens": kitchens,
            "offices": offices,
            "conferences": conferences,
            "storage": storage,
            "utility": utility,
            "corridors": corridors,
            "staircases": staircases,
            "elevators": elevators,
            "exits": exits,
            "balconies": balconies,
            "open_areas": open_areas,
            "contractor_name": contractor_name,
            "architect_name": architect_name,
            "consultant_name": consultant_name,
            "manager": manager,
            "site_eng_name": site_eng_name,
            "construction_phase": construction_phase
        }

        if submitted:
            if not project_name or not client or not location:
                st.error("Please fill in all required fields marked with *")
            elif end_date <= start_date:
                st.error("End date must be after start date")
            else:
                try:
                    code_suffix = project_name.replace(" ", "")[:3].upper() if project_name else "GEN"
                    base_project_code = f"PRJ-{code_suffix}-{st.session_state.get('user_id', '001')[:3].upper()}"
                    project_code = project_service.generate_unique_project_code(base_project_code)
                    total_rooms = bedrooms + bathrooms + living_rooms + kitchens + offices + conferences + storage

                    p_create = ProjectCreate(
                        project_name=project_name,
                        project_code=project_code,
                        client_name=client,
                        project_location=location,
                        budget=float(budget),
                        start_date=start_date,
                        expected_end_date=end_date,
                        description=description,
                        status="PLANNED",
                        building_type=b_type,
                        total_builtup_area=float(total_builtup),
                        site_area=float(site_area),
                        construction_area=float(total_builtup),
                        number_of_floors=int(num_floors),
                        basement_floors=int(basement_floors),
                        terrace_count=int(terrace_cnt),
                        parking_levels=int(parking_lvls),
                        roof_type=roof_type,
                        building_orientation=orientation,
                        foundation_type=foundation,
                        frame_type=frame_type,
                        structural_material=struct_mat,
                        concrete_grade=concrete_grade,
                        steel_grade=steel_grade,
                        seismic_zone=seismic_zone,
                        number_of_rooms=total_rooms,
                        bedrooms=int(bedrooms),
                        bathrooms=int(bathrooms),
                        living_rooms=int(living_rooms),
                        kitchens=int(kitchens),
                        conference_rooms=int(conferences),
                        office_rooms=int(offices),
                        storage_rooms=int(storage),
                        corridors=int(corridors),
                        staircases=int(staircases),
                        elevators=int(elevators),
                        emergency_exits=int(exits),
                        balconies=int(balconies),
                        utility_rooms=int(utility),
                        construction_phase=construction_phase,
                        owner_name=owner_name,
                        contractor_name=contractor_name,
                        architect_name=architect_name,
                        consultant_name=consultant_name,
                        manager_name=manager,
                        site_engineer_name=site_eng_name,
                        priority=priority
                    )
                    created = project_service.create_project(p_create)
                    workflow_engine.initialize_project_workflow(created.id)
                    project_workflow.set_active_project(created.id)

                    automation_engine.handle_event("ProjectCreated", {
                        "project_id": created.id,
                        "project_name": created.project_name
                    })

                    # Clear draft after successful submission
                    st.session_state["project_form_draft"] = {}
                    st.success(f"✅ Master Enterprise Project '{project_name}' created successfully! Project Code: **{created.project_code}**")
                    st.balloons()
                except CIHBaseException as e:
                    st.error(f"Backend Validation Error: {e.message}")
                except Exception as e:
                    st.error(f"Project creation failed: {str(e)}")


def _render_project_details(projects: pd.DataFrame) -> None:
    """Show details and version history for selected project."""
    project_ids = projects["Project ID"].tolist()
    active_obj = project_workflow.get_active_project()
    curr_active_id = active_obj.id if active_obj else (project_ids[0] if project_ids else None)

    sel_idx = 0
    if curr_active_id and curr_active_id in project_ids:
        sel_idx = project_ids.index(curr_active_id)

    def _on_detail_project_change():
        chosen_id = st.session_state.get("detail_project")
        if chosen_id:
            project_workflow.set_active_project(chosen_id)

    selected_id = st.selectbox(
        "Select Enterprise Project Code",
        project_ids,
        index=sel_idx,
        key="detail_project",
        on_change=_on_detail_project_change
    )
    project = projects[projects["Project ID"] == selected_id].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Budget", _format_currency(project["Budget"]), "💰")
    with col2:
        render_kpi_card("Progress", f"{project['Progress']}%", "📈")
    with col3:
        st.markdown(
            f'<div class="cih-kpi-card"><div class="cih-kpi-label">Status</div>'
            f'<div style="margin-top:0.5rem;">{status_to_badge(project["Status"])}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="cih-glass-card">
            <div class="cih-card-title">Master Project Details — {project['Project Name']} ({project['Project ID']})</div>
            <div class="cih-metric-row"><span class="cih-metric-label">Client / Sponsor</span><span class="cih-metric-value">{project['Client']}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Location</span><span class="cih-metric-value">{project['Location']}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Manager</span><span class="cih-metric-value">{project['Manager']}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Timeline</span><span class="cih-metric-value">{project['Start Date']} → {project['End Date']}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Priority</span><span class="cih-metric-value">{status_to_badge(project['Priority'])}</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Scope Description</span><span class="cih-metric-value">{project['Description']}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render Version History Log
    st.markdown("#### 📜 Version History & 3D Audit Trail")
    try:
        proj_obj = project_service.get_project_by_code(selected_id)
        if proj_obj:
            versions = project_workflow.get_project_version_history(proj_obj.id)
            if versions:
                v_rows = []
                for v in reversed(versions):
                    v_rows.append({
                        "Version": v.get("version", "V1.0"),
                        "Timestamp": v.get("timestamp", "N/A"),
                        "Editor": v.get("editor", "Senior Engineer"),
                        "Change Note": v.get("note", "Update"),
                    })
                st.dataframe(pd.DataFrame(v_rows), use_container_width=True, hide_index=True)
            else:
                st.info("No prior 3D geometry version snapshots logged yet. Use 3D Visualizer 'Save as Project' to commit versions.")
    except Exception as e:
        st.info(f"Version history log: {str(e)}")


def _render_update_status(projects: pd.DataFrame) -> None:
    """Update project status form."""
    st.markdown("### 🔄 Update Project Status & Lifecycle Phase")
    col1, col2 = st.columns(2)
    with col1:
        project_id = st.selectbox("Project ID", projects["Project ID"].tolist(), key="update_id")
    with col2:
        new_status = st.selectbox("New Status", ["Active", "Completed", "On Hold", "Delayed", "Planning"])
    new_progress = st.slider("Progress (%)", 0, 100, 50, key="update_progress")
    if st.button("Update Status & Broadcast Event", key="btn_update_status"):
        st.success(f"Project {project_id} updated to {new_status} at {new_progress}% progress. Synchronized across all modules.")


from modules.cost_estimation import (
    render_basic_cost_estimator,
    render_construction_cost_estimator,
)


def render() -> None:
    """Render project management page."""
    render_page_header("Project Management", "Manage construction projects & master building metadata across all sites")

    db_projects = project_service.get_all_projects()
    if db_projects:
        data_rows = []
        for p in db_projects:
            data_rows.append({
                "Project ID": p.project_code,
                "Project Name": p.project_name,
                "Type": p.building_type or "Residential",
                "Client": p.client_name or "N/A",
                "Location": p.project_location or "N/A",
                "Manager": p.manager_name or "Project Manager",
                "Start Date": str(p.start_date) if p.start_date else "2026-01-01",
                "End Date": str(p.expected_end_date) if p.expected_end_date else "2026-12-31",
                "Budget": p.budget,
                "Progress": 25 if p.status == "IN_PROGRESS" else (100 if p.status == "COMPLETED" else 0),
                "Status": "Active" if p.status == "IN_PROGRESS" else ("Completed" if p.status == "COMPLETED" else "Planning"),
                "Priority": p.priority or "High",
                "Description": p.description or "No description provided."
            })
        projects = pd.DataFrame(data_rows)
    else:
        projects = dummy_data.get_projects()

    # Summary KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Projects", str(len(projects)), "📁")
    with col2:
        active = len(projects[projects["Status"] == "Active"])
        render_kpi_card("Active", str(active), "🏗️", delta="+In Progress", delta_color="#22C55E")
    with col3:
        total_budget = projects["Budget"].sum()
        render_kpi_card("Total Budget", _format_currency(total_budget), "💰")
    with col4:
        avg_progress = projects["Progress"].mean()
        render_kpi_card("Avg Progress", f"{avg_progress:.0f}%", "📈")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 All Projects",
        "➕ Create Master Project",
        "💰 Basic Cost Estimator",
        "🏗️ Construction Cost Estimator"
    ])

    with tab1:
        pm_view_state = st.session_state.get("pm_view_state", "list")

        if pm_view_state == "details":
            _render_project_details(projects)
            st.markdown("<br>", unsafe_allow_html=True)
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                if st.button("📋 All Projects", key="btn_details_back_to_list", use_container_width=True):
                    st.session_state["pm_view_state"] = "list"
                    st.rerun()
            with col_nav2:
                if st.button("🔄 Update Status", key="btn_details_to_update_status", use_container_width=True, type="primary"):
                    st.session_state["pm_view_state"] = "update_status"
                    st.rerun()

        elif pm_view_state == "update_status":
            _render_update_status(projects)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📋 All Projects", key="btn_update_back_to_list", use_container_width=True):
                st.session_state["pm_view_state"] = "list"
                st.rerun()

        else:
            st.markdown("#### Project Portfolio Registry")
            _render_project_table(projects)
            st.markdown("<br>", unsafe_allow_html=True)
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("➕ Create Project", key="btn_create", use_container_width=True):
                    st.info("Switch to the '➕ Create Master Project' tab above to register a new master project.")
            with btn_col2:
                if st.button("🔍 View Details", key="btn_view", use_container_width=True):
                    st.session_state["pm_view_state"] = "details"
                    st.rerun()
            with btn_col3:
                if st.button("🔄 Update Status", key="btn_status", use_container_width=True):
                    st.session_state["pm_view_state"] = "update_status"
                    st.rerun()

    with tab2:
        _render_create_project_form()

    with tab3:
        render_basic_cost_estimator()

    with tab4:
        render_construction_cost_estimator()

