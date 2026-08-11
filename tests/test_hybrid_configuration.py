import importlib
import os
import unittest
from unittest.mock import patch


class HybridConfigurationTests(unittest.TestCase):
    def test_settings_require_explicit_database_url(self):
        with patch.dict(os.environ, {"DATABASE_URL": "", "APP_ENV": "testing"}, clear=False):
            settings_module = importlib.import_module("backend.config.settings")
            env_module = importlib.import_module("backend.config.env")
            engine_module = importlib.import_module("backend.database.engine")
            startup_module = importlib.import_module("backend.startup")

            importlib.reload(env_module)
            importlib.reload(settings_module)
            importlib.reload(engine_module)
            importlib.reload(startup_module)

            self.assertEqual(settings_module.settings.APP_ENV, "testing")
            self.assertEqual(settings_module.settings.DATABASE_URL, "")

    def test_startup_context_reports_runtime_configuration(self):
        with patch.dict(
            os.environ,
            {"APP_ENV": "development", "DATABASE_URL": "postgresql+psycopg2://user:pass@localhost:5432/cih"},
            clear=False,
        ):
            settings_module = importlib.import_module("backend.config.settings")
            env_module = importlib.import_module("backend.config.env")
            engine_module = importlib.import_module("backend.database.engine")
            startup_module = importlib.import_module("backend.startup")

            importlib.reload(env_module)
            importlib.reload(settings_module)
            importlib.reload(engine_module)
            importlib.reload(startup_module)

            context = startup_module.build_startup_context()

            self.assertEqual(context["app_env"], "development")
            self.assertTrue(context["database_url_configured"])
            self.assertEqual(context["database_backend"], "postgresql")

    def tearDown(self):
        env_module = importlib.import_module("backend.config.env")
        settings_module = importlib.import_module("backend.config.settings")
        engine_module = importlib.import_module("backend.database.engine")
        startup_module = importlib.import_module("backend.startup")
        importlib.reload(env_module)
        importlib.reload(settings_module)
        importlib.reload(engine_module)
        importlib.reload(startup_module)


if __name__ == "__main__":
    unittest.main()

