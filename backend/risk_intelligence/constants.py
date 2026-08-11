from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AssessmentStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EVALUATING = "EVALUATING"

class RecommendationPriority(str, Enum):
    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ResolutionStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class IncidentSeverity(str, Enum):
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    ARCHIVED = "ARCHIVED"

# Default scoring weights
DEFAULT_COMPONENT_WEIGHTS = {
    "Site Risk": 1.2,
    "Safety": 1.5,
    "Compliance": 1.3,
    "Insurance Exposure": 1.0,
    "Delay": 1.1,
    "Material": 1.0,
    "Equipment": 1.1
}

# Risk Threshold Constants
CRITICAL_RISK_THRESHOLD = 70.0
HIGH_RISK_THRESHOLD = 40.0
MODERATE_RISK_THRESHOLD = 20.0
