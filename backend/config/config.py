"""
Unified App Configuration for Agentic AI for Safety Monitoring with Construction Risk Analytics Backend.
"""
from .settings import settings
from .constants import *

class AppConfig:
    def __init__(self):
        self.settings = settings
        self.app_name = settings.PROJECT_NAME
        self.environment = settings.ENVIRONMENT
        self.db_url = settings.DATABASE_URL
        self.secret_key = settings.SECRET_KEY

config = AppConfig()
