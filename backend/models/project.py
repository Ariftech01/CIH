from datetime import date
from typing import Optional, List
from sqlalchemy import String, Text, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint("budget >= 0", name="check_project_budget_non_negative"),
    )

    project_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    project_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    client_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    project_location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    budget: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expected_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="PLANNED", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Building Details
    building_type: Mapped[Optional[str]] = mapped_column(String(50), default="Residential", nullable=True)
    total_builtup_area: Mapped[Optional[float]] = mapped_column(Float, default=0.0, nullable=True)
    site_area: Mapped[Optional[float]] = mapped_column(Float, default=0.0, nullable=True)
    construction_area: Mapped[Optional[float]] = mapped_column(Float, default=0.0, nullable=True)
    number_of_floors: Mapped[Optional[int]] = mapped_column(default=1, nullable=True)
    basement_floors: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    terrace_count: Mapped[Optional[int]] = mapped_column(default=1, nullable=True)
    parking_levels: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    roof_type: Mapped[Optional[str]] = mapped_column(String(50), default="Flat RCC Slab", nullable=True)
    building_orientation: Mapped[Optional[str]] = mapped_column(String(30), default="North-Facing", nullable=True)

    # Structural Information
    foundation_type: Mapped[Optional[str]] = mapped_column(String(50), default="Isolated Footing", nullable=True)
    frame_type: Mapped[Optional[str]] = mapped_column(String(50), default="RCC Frame", nullable=True)
    structural_material: Mapped[Optional[str]] = mapped_column(String(50), default="Reinforced Concrete", nullable=True)
    concrete_grade: Mapped[Optional[str]] = mapped_column(String(20), default="M30", nullable=True)
    steel_grade: Mapped[Optional[str]] = mapped_column(String(20), default="Fe-550 TMT", nullable=True)
    seismic_zone: Mapped[Optional[str]] = mapped_column(String(20), default="Zone III", nullable=True)
    wind_zone: Mapped[Optional[str]] = mapped_column(String(20), default="39 m/s", nullable=True)

    # Building Layout
    number_of_rooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    bedrooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    bathrooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    living_rooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    kitchens: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    conference_rooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    office_rooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    storage_rooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    corridors: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    staircases: Mapped[Optional[int]] = mapped_column(default=1, nullable=True)
    elevators: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    emergency_exits: Mapped[Optional[int]] = mapped_column(default=1, nullable=True)
    balconies: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)
    utility_rooms: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)

    # Construction Stakeholders & Phase
    construction_phase: Mapped[Optional[str]] = mapped_column(String(50), default="Planning", nullable=True)
    owner_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    contractor_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    architect_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    consultant_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    manager_name: Mapped[Optional[str]] = mapped_column(String(100), default="Rajesh Kumar", nullable=True)
    site_engineer_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    priority: Mapped[Optional[str]] = mapped_column(String(20), default="High", nullable=True)

    # 3D Scene Geometry & Versioning
    model_geometry_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    current_version: Mapped[Optional[str]] = mapped_column(String(20), default="V1.0", nullable=True)
    version_history_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign key to user
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    creator: Mapped[Optional["User"]] = relationship("User", back_populates="projects")
    buildings: Mapped[List["Building"]] = relationship("Building", back_populates="project", cascade="all, delete-orphan")
    cost_estimations: Mapped[List["CostEstimation"]] = relationship("CostEstimation", back_populates="project", cascade="all, delete-orphan")
    materials: Mapped[List["Material"]] = relationship("Material", back_populates="project", cascade="all, delete-orphan")
    workers: Mapped[List["Worker"]] = relationship("Worker", back_populates="project", cascade="all, delete-orphan")
    equipment: Mapped[List["Equipment"]] = relationship("Equipment", back_populates="project", cascade="all, delete-orphan")
    safety_inspections: Mapped[List["SafetyInspection"]] = relationship("SafetyInspection", back_populates="project", cascade="all, delete-orphan")
    progress_records: Mapped[List["ProjectProgress"]] = relationship("ProjectProgress", back_populates="project", cascade="all, delete-orphan")
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="project", cascade="all, delete-orphan")
    ai_conversations: Mapped[List["AIConversation"]] = relationship("AIConversation", back_populates="project")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="project")
    predictions: Mapped[List["AIPrediction"]] = relationship("AIPrediction", back_populates="project")
