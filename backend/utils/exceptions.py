"""
Custom Exception Classes for Agentic AI for Safety Monitoring with Construction Risk Analytics (CIH) Backend.
"""

class CIHBaseException(Exception):
    """Base exception for all CIH custom errors."""
    def __init__(self, message: str = "An application error occurred", details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

class DatabaseConnectionError(CIHBaseException):
    """Raised when database connection fails."""
    def __init__(self, message: str = "Database connection failed", details: dict = None):
        super().__init__(message, details)

class EntityNotFoundError(CIHBaseException):
    """Base exception for missing entities."""
    def __init__(self, entity_name: str = "Entity", entity_id: str = None):
        msg = f"{entity_name} with ID '{entity_id}' not found." if entity_id else f"{entity_name} not found."
        super().__init__(msg)

class ProjectNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Project", entity_id)

class BuildingNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Building", entity_id)

class FloorNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Floor", entity_id)

class RoomNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Room", entity_id)

class CostEstimationNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Cost Estimation", entity_id)

class MaterialNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Material", entity_id)

class WorkerNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Worker", entity_id)

class EquipmentNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Equipment", entity_id)

class SafetyInspectionNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Safety Inspection", entity_id)

class ReportNotFound(EntityNotFoundError):
    def __init__(self, entity_id: str = None):
        super().__init__("Report", entity_id)

class ValidationError(CIHBaseException):
    """Raised when business validation fails."""
    def __init__(self, message: str = "Validation error", details: dict = None):
        super().__init__(message, details)

class DuplicateProjectError(CIHBaseException):
    """Raised when attempting to create a project with duplicate code or name."""
    def __init__(self, message: str = "Project already exists", details: dict = None):
        super().__init__(message, details)

class AuthenticationError(CIHBaseException):
    """Raised when authentication credentials or token validation fails."""
    def __init__(self, message: str = "Authentication failed", details: dict = None):
        super().__init__(message, details)

class PermissionDeniedError(CIHBaseException):
    """Raised when user lacks access rights for requested operation."""
    def __init__(self, message: str = "Permission denied", details: dict = None):
        super().__init__(message, details)
