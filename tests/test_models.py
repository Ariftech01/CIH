import unittest
import uuid
from backend.database.session import get_db_session
from backend.database.manager import db_manager
from backend.models.user import User
from backend.models.project import Project

class TestModels(unittest.TestCase):
    def setUp(self):
        db_manager.create_all_tables()

    def test_user_project_relationship(self):
        uid = uuid.uuid4().hex[:6]
        with get_db_session() as session:
            user = User(
                username=f"user_{uid}",
                password_hash="hash123",
                full_name="Test User",
                email=f"test_{uid}@example.com"
            )
            session.add(user)
            session.flush()

            project = Project(
                project_name="Test Tower",
                project_code=f"TST-{uid}",
                budget=100000.0,
                user_id=user.id
            )
            session.add(project)
            session.flush()

            self.assertEqual(project.user_id, user.id)
            self.assertIsNotNone(project.id)
            self.assertIsNotNone(user.id)

if __name__ == "__main__":
    unittest.main()
