import unittest
from backend.auth.password import hash_password, verify_password
from backend.auth.rbac import has_role, check_permission
from backend.utils.exceptions import PermissionDeniedError

class TestAuth(unittest.TestCase):
    def test_password_hashing(self):
        raw_pwd = "MySecretPassword123"
        hashed = hash_password(raw_pwd)
        self.assertNotEqual(hashed, raw_pwd)
        self.assertTrue(verify_password(raw_pwd, hashed))
        self.assertFalse(verify_password("WrongPassword", hashed))

    def test_rbac_roles(self):
        self.assertTrue(has_role("ADMIN", ["VIEWER"]))
        self.assertFalse(has_role("VIEWER", ["ADMIN"]))

        with self.assertRaises(PermissionDeniedError):
            check_permission("VIEWER", ["ADMIN", "PROJECT_MANAGER"])

if __name__ == "__main__":
    unittest.main()
