"""Regression and integration tests for Unified Enterprise Project Workflow and Cross-Module Synchronization."""

import pytest
from backend.services.project_service import project_service
from backend.schemas.project import ProjectCreate
from backend.workflow.project_workflow import project_workflow
from backend.ai_engine.intent_router import intent_router


def test_create_master_project_with_building_metadata():
    """Test creating a project with expanded master building metadata."""
    p_code = f"PRJ-TEST-{int(pytest.importorskip('time').time())}"
    p_create = ProjectCreate(
        project_name="Test Enterprise Hospital",
        project_code=p_code,
        client_name="Apollo Healthcare",
        project_location="Chennai, TN",
        budget=85000000.0,
        building_type="Hospital",
        total_builtup_area=12500.0,
        number_of_floors=8,
        basement_floors=2,
        concrete_grade="M35",
        steel_grade="Fe-550 TMT",
        contractor_name="L&T Construction",
        architect_name="Creative Group Architects"
    )
    created = project_service.create_project(p_create)
    assert created.id is not None
    assert created.project_code == p_code
    assert created.building_type == "Hospital"
    assert created.number_of_floors == 8
    assert created.concrete_grade == "M35"


def test_active_project_context_switcher():
    """Test setting and getting active project context across modules."""
    p_code = f"PRJ-CTX-{int(pytest.importorskip('time').time())}"
    p_create = ProjectCreate(
        project_name="Active Context Test Tower",
        project_code=p_code,
        client_name="Godrej Properties",
        project_location="Bengaluru, KA",
        budget=45000000.0
    )
    created = project_service.create_project(p_create)
    
    # Set active project
    active_proj = project_workflow.set_active_project(created.id)
    assert active_proj is not None
    assert active_proj.id == created.id
    assert active_proj.project_code == p_code


def test_sync_3d_metrics_to_project():
    """Test transferring 3D scene metrics directly into master project record."""
    p_code = f"PRJ-3D-{int(pytest.importorskip('time').time())}"
    p_create = ProjectCreate(
        project_name="3D Studio Test Building",
        project_code=p_code,
        client_name="Prestige Group",
        project_location="Hyderabad, TS",
        budget=32000000.0
    )
    created = project_service.create_project(p_create)

    metrics = {
        "total_builtup_area": 4800.5,
        "number_of_floors": 5,
        "number_of_rooms": 24,
        "building_type": "Commercial"
    }
    dummy_geo = '{"version": "1.0", "rooms": [{"name": "Executive Office"}]}'

    updated = project_workflow.sync_3d_metrics_to_project(
        project_id_or_code=created.id,
        scene_metrics=metrics,
        geometry_json=dummy_geo,
        version_note="V1.0 Initial 3D Layout",
        create_new_version=True
    )

    assert updated.total_builtup_area == 4800.5
    assert updated.number_of_floors == 5
    assert updated.number_of_rooms == 24
    assert updated.current_version == "V2.0"

    history = project_workflow.get_project_version_history(created.id)
    assert len(history) >= 1
    assert history[-1]["note"] == "V1.0 Initial 3D Layout"


def test_chia_active_project_auto_routing():
    """Test CHIA intent router auto-extracting active project code when query lacks explicit code."""
    p_code = "PRJ-AUTO-001"
    
    import streamlit as st
    st.session_state["active_project_code"] = p_code

    result = intent_router.route_intent("Show risks for this active project")
    assert result["is_valid"] is True
    assert p_code in result["extracted_entities"]["project"]


def test_project_switch_data_synchronization():
    """Verify that switching projects produces distinct, project-keyed metrics."""
    from utils import dummy_data
    
    # Project A metrics
    proj_a_id = "PRJ-A-HOSPITAL"
    timeline_a = dummy_data.get_timeline_data(project_id=proj_a_id)
    budget_a = dummy_data.get_budget_allocation(project_id=proj_a_id)

    # Project B metrics
    proj_b_id = "PRJ-B-TOWER"
    timeline_b = dummy_data.get_timeline_data(project_id=proj_b_id)
    budget_b = dummy_data.get_budget_allocation(project_id=proj_b_id)

    # Assert that Project A and Project B generate distinct values
    assert not timeline_a.equals(timeline_b)
    assert not budget_a.equals(budget_b)


def test_persistence_and_editability_workflow():
    """Verify project persistence, editability, logout cleanup, and re-login restoration."""
    import time
    from utils.auth import logout
    import streamlit as st

    # Create 3 test projects in DB
    ts = int(time.time())
    pa = project_service.create_project(ProjectCreate(project_name=f"Hospital {ts}", project_code=f"PRJ-A-{ts}", budget=1000000.0))
    pb = project_service.create_project(ProjectCreate(project_name=f"Tower {ts}", project_code=f"PRJ-B-{ts}", budget=2000000.0))
    pc = project_service.create_project(ProjectCreate(project_name=f"Mall {ts}", project_code=f"PRJ-C-{ts}", budget=3000000.0))

    # 1. Login & Initial selection (Project A)
    project_workflow.set_active_project(pa.id)
    assert st.session_state.get("active_project_id") == pa.id

    # 2. User changes project (Project A -> Project B -> Project C -> Project B)
    project_workflow.set_active_project(pb.id)
    assert st.session_state.get("active_project_id") == pb.id

    project_workflow.set_active_project(pc.id)
    assert st.session_state.get("active_project_id") == pc.id

    project_workflow.set_active_project(pb.id)
    assert st.session_state.get("active_project_id") == pb.id

    # 3. Simulate Logout: session-state keys cleared
    keys_to_clear = [
        "authenticated", "user", "active_project_id", "active_project_code",
        "active_project_name", "_active_project_obj", "sidebar_active_project_selector", "detail_project"
    ]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]

    assert "active_project_id" not in st.session_state

    # 4. Simulate Re-login: get_active_project restores last persisted project (Project B)
    restored = project_workflow.get_active_project()
    assert restored is not None
    assert restored.id == pb.id
    assert st.session_state.get("active_project_id") == pb.id

    # 5. Verify restored project remains fully editable (Project B -> Project C)
    proj_c2 = project_workflow.set_active_project(pc.id)
    assert st.session_state.get("active_project_id") == pc.id


def test_generate_unique_project_code_auto_increment():
    """Verify that generating project code auto-increments suffix when code already exists in DB."""
    base_code = f"PRJ-UNIQ-{int(pytest.importorskip('time').time())}-001"
    code1 = project_service.generate_unique_project_code(base_code)
    assert code1 == base_code.upper()

    # Create first project with base_code
    project_service.create_project(ProjectCreate(
        project_name="Unique Test Project 1",
        project_code=code1,
        budget=100000.0
    ))

    # Next call with same base code should auto-increment to 002
    code2 = project_service.generate_unique_project_code(base_code)
    assert code2 != code1
    assert code2.endswith("-002")

    # Create second project with code2
    project_service.create_project(ProjectCreate(
        project_name="Unique Test Project 2",
        project_code=code2,
        budget=100000.0
    ))

    # Next call should auto-increment to 003
    code3 = project_service.generate_unique_project_code(base_code)
    assert code3.endswith("-003")



