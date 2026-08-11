import unittest
from backend.database.manager import db_manager
from backend.database.connection import check_connection, ping_database

class TestDatabase(unittest.TestCase):
    def test_database_connection(self):
        self.assertTrue(check_connection())
        self.assertTrue(ping_database())

    def test_database_table_creation(self):
        db_manager.create_all_tables()
        self.assertTrue(db_manager.is_healthy())

if __name__ == "__main__":
    unittest.main()
