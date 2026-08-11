import time
from abc import ABC, abstractmethod
from typing import Dict, Any
from backend.risk_intelligence.schemas.agent import AgentResult

class BaseRiskAgent(ABC):
    """
    Abstract Base Class for all Specialized Enterprise Risk Agents.
    Agents have a single responsibility, must not communicate directly with each other,
    and return structured AgentResult objects.
    """
    def __init__(self, name: str):
        self.name = name

    def execute(self, project_context: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        try:
            result = self.analyze(project_context)
            duration = (time.time() - start_time) * 1000.0
            result.duration_ms = duration
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000.0
            return AgentResult(
                agent_name=self.name,
                status="FAILED",
                score=0.0,
                duration_ms=duration,
                summary=f"Execution failed in {self.name}",
                error_message=str(e)
            )

    @abstractmethod
    def analyze(self, project_context: Dict[str, Any]) -> AgentResult:
        pass
