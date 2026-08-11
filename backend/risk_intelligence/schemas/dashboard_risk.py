from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class DashboardKPI(BaseModel):
    title: str
    value: str
    delta: Optional[str] = None
    icon: str = "📊"
    color: str = "#3B82F6"  # Hex color string matching glassmorphism theme
    status: str = "NORMAL"
    category: str = "GENERAL"

class DashboardWidget(BaseModel):
    widget_id: str
    widget_type: str = "KPI_CARD"  # KPI_CARD, SCORECARD, CHART, ALERT_PANEL, TABLE, RECOMMENDATIONS
    title: str
    data: Dict[str, Any] = Field(default_factory=dict)
    order: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DashboardContext(BaseModel):
    project_id: str
    project_name: str = "Construction Project"
    overall_risk_score: float = 0.0
    risk_level: str = "LOW"
    health_status: str = "HEALTHY"
    health_index: float = 100.0
    component_scores: Dict[str, Any] = Field(default_factory=dict)
    executive_kpis: List[DashboardKPI] = Field(default_factory=list)
    critical_alerts: List[Dict[str, Any]] = Field(default_factory=list)
    top_recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    recent_activity: List[Dict[str, Any]] = Field(default_factory=list)
    historical_trends: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
