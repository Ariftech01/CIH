from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AutomationContext(BaseModel):
    workflow_id: str
    job_id: str
    project_id: str
    task_metadata: Dict[str, Any] = Field(default_factory=dict)
    event_type: str = "WORKFLOW_TRIGGER"
    status: str = "QUEUED"  # QUEUED, RUNNING, COMPLETED, FAILED, RETRYING
    duration_ms: float = 0.0
    retry_count: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class NotificationContext(BaseModel):
    notification_id: str
    event_type: str = "SYSTEM_EVENT"
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    recipients: List[str] = Field(default_factory=list)
    title: str
    message: str
    status: str = "QUEUED"  # QUEUED, DISPATCHED, DELIVERED, FAILED
    channel: str = "IN_APP"  # IN_APP, EMAIL, TEAMS, SLACK, SMS, WEBHOOK
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BackgroundJobSession(BaseModel):
    job_id: str
    service_name: str
    status: str = "RUNNING"  # RUNNING, COMPLETED, FAILED, SKIPPED
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PerformanceMetrics(BaseModel):
    total_requests: int = 0
    avg_latency_ms: float = 0.0
    memory_mb: float = 0.0
    cpu_pct: float = 0.0
    bottlenecks: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DeploymentChecklist(BaseModel):
    environment: str = "PRODUCTION"
    database_status: str = "CONNECTED"
    ai_status: str = "AVAILABLE"
    checks: Dict[str, bool] = Field(default_factory=dict)
    is_production_ready: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
