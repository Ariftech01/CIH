from typing import Optional
from datetime import date
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class ProjectBase(BaseSchema):
    project_name: str = Field(..., min_length=1, max_length=100)
    project_code: str = Field(..., min_length=1, max_length=50)
    client_name: Optional[str] = None
    project_location: Optional[str] = None
    budget: float = Field(default=0.0, ge=0)
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    status: str = "PLANNED"
    description: Optional[str] = None

    # Building Details
    building_type: Optional[str] = "Residential"
    total_builtup_area: Optional[float] = 0.0
    site_area: Optional[float] = 0.0
    construction_area: Optional[float] = 0.0
    number_of_floors: Optional[int] = 1
    basement_floors: Optional[int] = 0
    terrace_count: Optional[int] = 1
    parking_levels: Optional[int] = 0
    roof_type: Optional[str] = "Flat RCC Slab"
    building_orientation: Optional[str] = "North-Facing"

    # Structural Information
    foundation_type: Optional[str] = "Isolated Footing"
    frame_type: Optional[str] = "RCC Frame"
    structural_material: Optional[str] = "Reinforced Concrete"
    concrete_grade: Optional[str] = "M30"
    steel_grade: Optional[str] = "Fe-550 TMT"
    seismic_zone: Optional[str] = "Zone III"
    wind_zone: Optional[str] = "39 m/s"

    # Building Layout
    number_of_rooms: Optional[int] = 0
    bedrooms: Optional[int] = 0
    bathrooms: Optional[int] = 0
    living_rooms: Optional[int] = 0
    kitchens: Optional[int] = 0
    conference_rooms: Optional[int] = 0
    office_rooms: Optional[int] = 0
    storage_rooms: Optional[int] = 0
    corridors: Optional[int] = 0
    staircases: Optional[int] = 1
    elevators: Optional[int] = 0
    emergency_exits: Optional[int] = 1
    balconies: Optional[int] = 0
    utility_rooms: Optional[int] = 0

    # Stakeholders & Phase
    construction_phase: Optional[str] = "Planning"
    owner_name: Optional[str] = None
    contractor_name: Optional[str] = None
    architect_name: Optional[str] = None
    consultant_name: Optional[str] = None
    manager_name: Optional[str] = "Rajesh Kumar"
    site_engineer_name: Optional[str] = None
    priority: Optional[str] = "High"

    # 3D Scene & Versioning
    model_geometry_json: Optional[str] = None
    current_version: Optional[str] = "V1.0"
    version_history_json: Optional[str] = None

class ProjectCreate(ProjectBase):
    user_id: Optional[str] = None

class ProjectUpdate(BaseSchema):
    project_name: Optional[str] = None
    client_name: Optional[str] = None
    project_location: Optional[str] = None
    budget: Optional[float] = Field(default=None, ge=0)
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    status: Optional[str] = None
    description: Optional[str] = None

    building_type: Optional[str] = None
    total_builtup_area: Optional[float] = None
    site_area: Optional[float] = None
    construction_area: Optional[float] = None
    number_of_floors: Optional[int] = None
    basement_floors: Optional[int] = None
    terrace_count: Optional[int] = None
    parking_levels: Optional[int] = None
    roof_type: Optional[str] = None
    building_orientation: Optional[str] = None

    foundation_type: Optional[str] = None
    frame_type: Optional[str] = None
    structural_material: Optional[str] = None
    concrete_grade: Optional[str] = None
    steel_grade: Optional[str] = None
    seismic_zone: Optional[str] = None
    wind_zone: Optional[str] = None

    number_of_rooms: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    living_rooms: Optional[int] = None
    kitchens: Optional[int] = None
    conference_rooms: Optional[int] = None
    office_rooms: Optional[int] = None
    storage_rooms: Optional[int] = None
    corridors: Optional[int] = None
    staircases: Optional[int] = None
    elevators: Optional[int] = None
    emergency_exits: Optional[int] = None
    balconies: Optional[int] = None
    utility_rooms: Optional[int] = None

    construction_phase: Optional[str] = None
    owner_name: Optional[str] = None
    contractor_name: Optional[str] = None
    architect_name: Optional[str] = None
    consultant_name: Optional[str] = None
    manager_name: Optional[str] = None
    site_engineer_name: Optional[str] = None
    priority: Optional[str] = None

    model_geometry_json: Optional[str] = None
    current_version: Optional[str] = None
    version_history_json: Optional[str] = None

class ProjectResponse(ProjectBase, AuditSchema):
    user_id: Optional[str] = None
