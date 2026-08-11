import unittest
import uuid
from datetime import date
from backend.database.manager import db_manager
from backend.services.auth_service import auth_service
from backend.services.project_service import project_service
from backend.services.building_service import building_service
from backend.services.cost_service import cost_service
from backend.services.material_service import material_service
from backend.services.worker_service import worker_service
from backend.services.equipment_service import equipment_service
from backend.services.safety_service import safety_service
from backend.services.task_service import task_service
from backend.services.approval_service import approval_service
from backend.services.notification_service import notification_service
from backend.services.collaboration_service import collaboration_service
from backend.services.workflow_service import workflow_service
from backend.services.ai_service import ai_service
from backend.workflow.workflow_engine import workflow_engine
from backend.automation.automation_engine import automation_engine
from backend.quantification.quantification_engine import quantification_engine
from backend.analytics.analytics_engine import analytics_engine
from backend.cache.cache_manager import cache_manager
from backend.auth.rbac import has_role, check_permission
from backend.utils.exceptions import PermissionDeniedError, DuplicateProjectError

from backend.schemas.user import UserCreate
from backend.schemas.project import ProjectCreate, ProjectUpdate
from backend.schemas.building import BuildingCreate
from backend.schemas.floor import FloorCreate
from backend.schemas.room import RoomCreate
from backend.schemas.cost_estimation import CostEstimationCreate
from backend.schemas.material import MaterialCreate
from backend.schemas.worker import WorkerCreate
from backend.schemas.equipment import EquipmentCreate
from backend.schemas.safety import SafetyInspectionCreate
from backend.schemas.task import TaskCreate, TaskUpdate
from backend.schemas.approval import ApprovalCreate, ApprovalUpdate
from backend.schemas.notification import NotificationCreate
from backend.schemas.collaboration import ProjectMemberCreate
from backend.schemas.ai import AIConversationCreate, AIMessageCreate, AIPredictionCreate

class TestEnterpriseWorkflowAutomation(unittest.TestCase):
    def setUp(self):
        db_manager.create_all_tables()
        self.uid = uuid.uuid4().hex[:6]

    def test_end_to_end_enterprise_workflow(self):
        # 1. User Registration & Auth
        u_in = UserCreate(
            username=f"pm_{self.uid}",
            password="SecurePass123!",
            full_name="Enterprise PM",
            email=f"pm_{self.uid}@cih.com",
            role="PROJECT_MANAGER"
        )
        user = auth_service.register_user(u_in)
        self.assertIsNotNone(user.id)

        auth_user = auth_service.authenticate_user(u_in.username, "SecurePass123!")
        self.assertEqual(auth_user.id, user.id)

        # 2. Project Creation & Workflow Initialization
        code = f"PRJ-{self.uid.upper()}"
        p_in = ProjectCreate(
            project_name=f"Tower {self.uid}",
            project_code=code,
            client_name="Global Infra Corp",
            project_location="Metropolis Financial District",
            budget=5000000.0,
            start_date=date(2026, 1, 1),
            expected_end_date=date(2027, 12, 31),
            description="50-story commercial skyscraper.",
            user_id=user.id
        )
        proj = project_service.create_project(p_in)
        self.assertIsNotNone(proj.id)

        # Workflow Engine Init
        ws = workflow_engine.initialize_project_workflow(proj.id)
        self.assertEqual(ws.current_stage, "DRAFT")

        # Automation Engine Event
        automation_engine.handle_event("ProjectCreated", {
            "project_id": proj.id,
            "project_name": proj.project_name
        })
        ws_updated = workflow_service.get_workflow_state(proj.id)
        self.assertEqual(ws_updated.current_stage, "PLANNING")

        # 3. 3D Building Visualizer Save & Quantification Engine
        b_in = BuildingCreate(
            project_id=proj.id,
            building_name="Tower Alpha",
            building_type="Commercial High-Rise",
            number_of_floors=10,
            total_area=1200.0,
            units="sqm"
        )
        bld = building_service.create_building(b_in)
        self.assertIsNotNone(bld.id)

        # Add Floor & Room
        flr = building_service.add_floor(bld.id, FloorCreate(
            building_id=bld.id,
            floor_number=1,
            floor_name="Ground Floor",
            floor_height=3.5,
            area=1200.0
        ))
        room = building_service.add_room(RoomCreate(
            floor_id=flr.id,
            room_name="Grand Lobby",
            room_type="Lobby",
            length=20.0,
            width=30.0,
            height=3.5
        ))
        self.assertEqual(room.area, 600.0)

        # Quantification Engine Execution
        quantities = quantification_engine.calculate_quantities(
            total_area=1200.0,
            building_height=35.0,
            floor_count=10,
            wall_area=3360.0
        )
        self.assertGreater(quantities["concrete_volume_m3"], 0)
        self.assertGreater(quantities["cement_bags"], 0)

        automation_engine.handle_event("BuildingSaved", {"project_id": proj.id})
        ws_bld = workflow_service.get_workflow_state(proj.id)
        self.assertEqual(ws_bld.current_stage, "DESIGN")
        self.assertTrue(ws_bld.building_designed)

        # 4. Cost Estimation Integration
        est_in = CostEstimationCreate(
            project_id=proj.id,
            estimated_material_cost=1500000.0,
            estimated_labour_cost=800000.0,
            estimated_equipment_cost=400000.0,
            currency="USD"
        )
        cost_est = cost_service.create_estimate(est_in)
        self.assertEqual(cost_est.estimated_total_cost, 2700000.0)

        automation_engine.handle_event("CostEstimated", {
            "project_id": proj.id,
            "estimated_total_cost": cost_est.estimated_total_cost
        })
        ws_cost = workflow_service.get_workflow_state(proj.id)
        self.assertEqual(ws_cost.current_stage, "ESTIMATION")

        # 5. Material & Worker & Equipment Management
        mat = material_service.add_material(MaterialCreate(
            project_id=proj.id,
            material_name="Ready-Mix Concrete M30",
            category="Concrete",
            unit="Cu.M",
            quantity_required=quantities["concrete_volume_m3"],
            quantity_available=quantities["concrete_volume_m3"] * 0.8,
            supplier="UltraTech Concrete",
            unit_cost=85.0
        ))
        self.assertIsNotNone(mat.id)

        wrk = worker_service.add_worker(WorkerCreate(
            project_id=proj.id,
            worker_name="Alex Mercer",
            designation="Site Engineer",
            daily_wage=250.0,
            status="ACTIVE"
        ))
        self.assertIsNotNone(wrk.id)

        eq = equipment_service.add_equipment(EquipmentCreate(
            project_id=proj.id,
            equipment_name="Liebherr Tower Crane 280 EC-H",
            equipment_type="Heavy Crane",
            status="OPERATIONAL",
            availability="AVAILABLE"
        ))
        self.assertIsNotNone(eq.id)

        # 6. Safety Inspection
        sft = safety_service.record_inspection(SafetyInspectionCreate(
            project_id=proj.id,
            inspection_date=date.today(),
            risk_level="LOW",
            description="Perimeter safety barriers and harness inspection passed.",
            status="OPEN"
        ))
        self.assertIsNotNone(sft.id)

        automation_engine.handle_event("SafetyCompleted", {"project_id": proj.id})
        ws_sft = workflow_service.get_workflow_state(proj.id)
        self.assertEqual(ws_sft.current_stage, "EXECUTION")

        # 7. Task Management & Approvals
        tasks = task_service.get_project_tasks(proj.id)
        self.assertGreater(len(tasks), 0)
        task_service.update_task(tasks[0].id, TaskUpdate(status="COMPLETED", completion_percentage=100))

        appr = approval_service.create_approval_request(ApprovalCreate(
            project_id=proj.id,
            approval_type="COST_ESTIMATE",
            title="Approval for Phase 1 Construction Cost",
            requested_by=user.id
        ))
        processed_appr = approval_service.process_approval(appr.id, ApprovalUpdate(
            status="APPROVED",
            approved_by=user.id,
            comments="Estimate approved within budget."
        ))
        self.assertEqual(processed_appr.status, "APPROVED")

        # 8. Multi-Project Collaboration
        collab = collaboration_service.add_member(ProjectMemberCreate(
            project_id=proj.id,
            user_id=user.id,
            project_role="PROJECT_MANAGER"
        ))
        self.assertIsNotNone(collab.id)

        # 9. Notifications & Analytics
        notifs = notification_service.get_unread_notifications()
        self.assertGreater(len(notifs), 0)

        kpis = analytics_engine.get_dashboard_kpis()
        self.assertGreaterEqual(kpis["total_projects"], 1)

        # 10. AI Service Integration
        conv = ai_service.create_conversation(AIConversationCreate(
            user_id=user.id,
            project_id=proj.id,
            conversation_title="Project Feasibility Chat"
        ))
        msg = ai_service.add_message(AIMessageCreate(
            conversation_id=conv.id,
            sender="user",
            message="What is the estimated concrete requirement for Tower Alpha?"
        ))
        self.assertIsNotNone(msg.id)

        pred = ai_service.save_prediction(AIPredictionCreate(
            project_id=proj.id,
            prediction_type="COST_OVERRUN",
            prediction_result="Low Risk of Overrun (92% Confidence)",
            confidence_score=0.92
        ))
        self.assertEqual(pred.confidence_score, 0.92)

        # 11. RBAC Check
        self.assertTrue(has_role("PROJECT_MANAGER", ["PROJECT_MANAGER", "VIEWER"]))
        with self.assertRaises(PermissionDeniedError):
            check_permission("VIEWER", ["ADMIN"])

        # 12. Caching Manager
        cache_manager.set("test_key", "test_value", ttl_seconds=10)
        self.assertEqual(cache_manager.get("test_key"), "test_value")

if __name__ == "__main__":
    unittest.main()
