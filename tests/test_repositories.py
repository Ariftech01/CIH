import unittest
import uuid
from backend.database.session import get_db_session
from backend.database.manager import db_manager
from backend.repositories.project_repository import ProjectRepository

class TestRepositories(unittest.TestCase):
    def setUp(self):
        db_manager.create_all_tables()

    def test_project_repository_crud(self):
        uid = uuid.uuid4().hex[:6]
        code = f"REPO-{uid.upper()}"
        with get_db_session() as session:
            repo = ProjectRepository(session)
            
            # Create
            proj = repo.create({
                "project_name": "Repo Test Project",
                "project_code": code,
                "budget": 500000.0
            })
            self.assertIsNotNone(proj.id)
            proj_id = proj.id

            # Read
            fetched = repo.get_by_id(proj_id)
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched.project_name, "Repo Test Project")

            # Search
            results = repo.search_projects("Repo")
            self.assertGreaterEqual(len(results), 1)

            # Soft Delete
            deleted = repo.soft_delete(proj_id)
            self.assertTrue(deleted)
            self.assertIsNone(repo.get_by_id(proj_id))

if __name__ == "__main__":
    unittest.main()
