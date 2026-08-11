import unittest
import uuid
from backend.database.manager import db_manager
from backend.services.project_service import project_service
from backend.schemas.project import ProjectCreate
from backend.utils.exceptions import DuplicateProjectError

class TestServices(unittest.TestCase):
    def setUp(self):
        db_manager.create_all_tables()

    def test_project_service_create_and_duplicate_prevention(self):
        unique_code = f"SRV-{uuid.uuid4().hex[:6]}"
        p_in = ProjectCreate(
            project_name="Service Test Proj",
            project_code=unique_code,
            budget=250000.0
        )
        res = project_service.create_project(p_in)
        self.assertIsNotNone(res.id)
        self.assertEqual(res.project_code, unique_code.upper())

        # Test Duplicate Code Rejection
        with self.assertRaises(DuplicateProjectError):
            project_service.create_project(p_in)

if __name__ == "__main__":
    unittest.main()
