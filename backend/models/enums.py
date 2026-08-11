import enum

class UserRoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    SITE_ENGINEER = "SITE_ENGINEER"
    SAFETY_OFFICER = "SAFETY_OFFICER"
    ESTIMATOR = "ESTIMATOR"
    VIEWER = "VIEWER"

class UserStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class ProjectStatusEnum(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class RiskLevelEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ReportTypeEnum(str, enum.Enum):
    SUMMARY = "SUMMARY"
    COST = "COST"
    MATERIAL = "MATERIAL"
    WORKER = "WORKER"
    EQUIPMENT = "EQUIPMENT"
    SAFETY = "SAFETY"
    PROGRESS = "PROGRESS"

class EquipmentStatusEnum(str, enum.Enum):
    OPERATIONAL = "OPERATIONAL"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    IDLE = "IDLE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

class WorkerStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ON_LEAVE = "ON_LEAVE"
    TERMINATED = "TERMINATED"
