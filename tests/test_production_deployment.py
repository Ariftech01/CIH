import unittest
import uuid
import os
import yaml
from pathlib import Path

from backend.config.settings import settings
from backend.database.manager import db_manager
from backend.observability.observability_service import observability_service
from backend.document_management.edms_service import edms_service
from backend.ai_engine.context_engine import project_context_engine
from backend.prediction_engine.prediction_service import enterprise_prediction_engine
from backend.api.gateway import api_gateway
from backend.security.security_service import security_service
from backend.schemas.document import DocumentCreate

from backend.database.session import get_db_session
from backend.repositories.project_repository import ProjectRepository

class TestProductionDeployment(unittest.TestCase):
    def setUp(self):
        db_manager.create_all_tables()
        self.uid = uuid.uuid4().hex[:6]
        with get_db_session() as session:
            p_repo = ProjectRepository(session)
            p_repo.create({
                "id": f"proj-{self.uid}",
                "project_name": f"Test Project {self.uid}",
                "project_code": f"PRJ-{self.uid}",
                "budget": 500000.0
            })


    def test_database_and_supabase_health(self):
        health = db_manager.check_health()
        self.assertEqual(health["status"], "Healthy")
        self.assertTrue(health["database_connected"])

    def test_render_yaml_validity(self):
        render_path = Path("render.yaml")
        self.assertTrue(render_path.exists(), "render.yaml must exist in root.")
        with open(render_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        self.assertIn("services", config)
        self.assertEqual(config["services"][0]["name"], "construction-intelligence-hub")

    def test_dockerfile_and_docker_compose_exists(self):
        self.assertTrue(Path("Dockerfile").exists(), "Dockerfile must exist.")
        self.assertTrue(Path(".dockerignore").exists(), ".dockerignore must exist.")
        self.assertTrue(Path("docker-compose.yml").exists(), "docker-compose.yml must exist.")

    def test_observability_service(self):
        observability_service.log_event("TEST", "Running Production Test", level="INFO")
        observability_service.record_telemetry("TestFeature", execution_time_ms=12.5)
        diagnostics = observability_service.get_system_diagnostics()
        self.assertEqual(diagnostics["services"]["workflow_engine"], "Healthy")
        self.assertGreater(diagnostics["uptime_seconds"], 0)

    def test_edms_document_management(self):
        doc_in = DocumentCreate(
            project_id=f"proj-{self.uid}",
            file_name=f"BOQ_{self.uid}.pdf",
            file_type="BOQ",
            file_size=1048576,
            storage_path=f"/storage/docs/BOQ_{self.uid}.pdf"
        )
        doc = edms_service.upload_document_metadata(doc_in)
        self.assertIsNotNone(doc.id)
        self.assertIn("V1", doc.file_type)

        reg = edms_service.register_ai_document_context(doc.id)
        self.assertTrue(reg["ai_registered"])

    def test_ai_context_and_knowledge_base(self):
        ctx = project_context_engine.build_project_context_prompt("non-existent-id")
        self.assertIsNotNone(ctx)

        kb = project_context_engine.query_construction_knowledge_base("concrete")
        self.assertGreater(len(kb), 0)

    def test_prediction_engine(self):
        pred = enterprise_prediction_engine.generate_project_prediction(f"proj-{self.uid}", "COST_OVERRUN")
        self.assertGreater(pred.confidence_score, 0.5)

        dt = enterprise_prediction_engine.get_digital_twin_sync_status(f"proj-{self.uid}")
        self.assertTrue(dt["digital_twin_prepared"])

    def test_api_gateway_and_security(self):
        openapi = api_gateway.get_openapi_schema()
        self.assertEqual(openapi["info"]["title"], "Construction Intelligence Hub Enterprise API")

        headers = security_service.get_security_headers()
        self.assertIn("X-Content-Type-Options", headers)

        sanitized = security_service.sanitize_input("<script>alert('xss')</script>")
        self.assertNotIn("<script>", sanitized)

if __name__ == "__main__":
    unittest.main()
