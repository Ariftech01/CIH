class CRIBaseException(Exception):
    """Base exception for all Construction Risk Intelligence errors."""
    pass

class RiskAssessmentNotFoundError(CRIBaseException):
    """Raised when a requested Risk Assessment record is not found."""
    pass

class IncidentNotFoundError(CRIBaseException):
    """Raised when an Incident record is not found."""
    pass

class RecommendationNotFoundError(CRIBaseException):
    """Raised when a Risk Recommendation record is not found."""
    pass

class InvalidProjectContextError(CRIBaseException):
    """Raised when incoming project context data is invalid or incomplete."""
    pass

class RiskCalculationError(CRIBaseException):
    """Raised when deterministic risk scoring fails."""
    pass

class AgentExecutionError(CRIBaseException):
    """Raised when a specialized Risk Agent execution fails."""
    pass
