"""
Database Seeding Script for Agentic AI for Safety Monitoring with Construction Risk Analytics (CIH).
Populates optional development/demo seed data.
"""
import sys
from pathlib import Path
from datetime import date, datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.database.session import get_db_session
from backend.repositories.user_repository import UserRepository
from backend.repositories.project_repository import ProjectRepository
from backend.repositories.material_repository import MaterialRepository
from backend.repositories.worker_repository import WorkerRepository
from backend.repositories.equipment_repository import EquipmentRepository
from backend.repositories.safety_repository import SafetyRepository
from backend.auth.password import hash_password
from backend.database.manager import db_manager
from backend.app_logging.logger import logger

def seed_database():
    logger.info("Ensuring database tables exist...")
    db_manager.create_all_tables()
    logger.info("Seeding database with sample demo data...")
    with get_db_session() as session:
        user_repo = UserRepository(session)
        proj_repo = ProjectRepository(session)
        mat_repo = MaterialRepository(session)
        wrk_repo = WorkerRepository(session)
        eq_repo = EquipmentRepository(session)
        sft_repo = SafetyRepository(session)

        # 1. Admin User
        admin = user_repo.get_by_username("admin")
        if not admin:
            admin = user_repo.create({
                "username": "admin",
                "password_hash": hash_password("admin123"),
                "full_name": "System Administrator",
                "email": "admin@cih.com",
                "role": "ADMIN",
                "status": "ACTIVE"
            })
            logger.info("Seeded Admin user.")

        # 2. Demo Project
        project = proj_repo.get_by_code("PRJ-2026-001")
        if not project:
            project = proj_repo.create({
                "project_name": "Apex Commercial Tower",
                "project_code": "PRJ-2026-001",
                "client_name": "Apex Real Estate Ltd.",
                "project_location": "Downtown Financial Center",
                "budget": 2500000.0,
                "start_date": date(2026, 1, 15),
                "expected_end_date": date(2027, 6, 30),
                "status": "IN_PROGRESS",
                "description": "25-story luxury commercial high-rise building with smart HVAC and underground parking.",
                "user_id": admin.id
            })
            logger.info(f"Seeded Demo Project: {project.project_name}")

            # 3. Seed Materials
            mat_repo.create({
                "project_id": project.id,
                "material_name": "Portland Cement (Grade 53)",
                "category": "Raw Concrete",
                "unit": "Bags",
                "quantity_required": 5000.0,
                "quantity_available": 3200.0,
                "supplier": "BuildPro Supplies Ltd",
                "unit_cost": 8.50,
                "total_cost": 42500.0
            })
            mat_repo.create({
                "project_id": project.id,
                "material_name": "Reinforced Steel Rebar 12mm",
                "category": "Steel & Metal",
                "unit": "Tons",
                "quantity_required": 120.0,
                "quantity_available": 85.0,
                "supplier": "Apex Metallurgy",
                "unit_cost": 650.0,
                "total_cost": 78000.0
            })

            # 4. Seed Workers
            wrk_repo.create({
                "project_id": project.id,
                "worker_name": "Robert Vance",
                "designation": "Site Foreman",
                "contact": "+1-555-0192",
                "daily_wage": 220.0,
                "attendance": "PRESENT",
                "assigned_task": "Overseeing foundation pouring",
                "status": "ACTIVE"
            })
            wrk_repo.create({
                "project_id": project.id,
                "worker_name": "Marcus Brody",
                "designation": "Master Mason",
                "contact": "+1-555-0184",
                "daily_wage": 160.0,
                "attendance": "PRESENT",
                "assigned_task": "Reinforcement steel tying",
                "status": "ACTIVE"
            })

            # 5. Seed Equipment
            eq_repo.create({
                "project_id": project.id,
                "equipment_name": "CAT 320 Hydraulic Excavator",
                "equipment_type": "Earthmoving",
                "status": "OPERATIONAL",
                "availability": "AVAILABLE",
                "maintenance_date": date(2026, 7, 20),
                "operator": "David Miller"
            })

            # 6. Seed Safety Inspection
            sft_repo.create({
                "project_id": project.id,
                "inspection_date": date(2026, 8, 1),
                "risk_level": "LOW",
                "description": "Weekly site walk-through. Scaffolding harness checks passed.",
                "corrective_action": "Ensure all perimeter hardhat signs remain visible.",
                "status": "OPEN"
            })

            logger.info("Demo dataset seeded successfully.")

if __name__ == "__main__":
    seed_database()
