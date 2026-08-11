from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.risk_intelligence.agents import (
    BaseRiskAgent, SiteRiskAgent, SafetyAgent, ComplianceAgent, InsuranceAgent, ReportingAgent
)
from backend.risk_intelligence.engine.pipeline import analysis_pipeline
from backend.risk_intelligence.engine.aggregator import risk_aggregator_engine
from backend.risk_intelligence.engine.recommendation_engine import enterprise_recommendation_engine
from backend.risk_intelligence.engine.historical_intelligence import historical_intelligence_engine
from backend.risk_intelligence.engine.project_health_engine import project_health_engine
from backend.risk_intelligence.engine.event_processor import event_processor
from backend.app_logging.logger import logger as app_logger

class ConstructionRiskIntelligenceEngine:
    """
    Central Orchestrator of the Construction Risk Intelligence (CRI) Subsystem.
    Executes analysis pipelines, coordinates specialized risk agents, aggregates risk scores,
    calculates project health indicators, generates actionable recommendations, and processes events.
    """

    def __init__(self):
        self.pipeline = analysis_pipeline
        self.aggregator = risk_aggregator_engine
        self.recommendation_engine = enterprise_recommendation_engine
        self.historical_engine = historical_intelligence_engine
        self.health_engine = project_health_engine
        self.event_processor = event_processor
        self.agents: List[BaseRiskAgent] = [
            SiteRiskAgent(),
            SafetyAgent(),
            ComplianceAgent(),
            InsuranceAgent(),
            ReportingAgent()
        ]

    def execute_analysis_pipeline(
        self,
        project_context: Dict[str, Any],
        assessment_id: str = "temp_id"
    ) -> Dict[str, Any]:
        """
        Runs the complete enterprise risk intelligence 8-stage analysis pipeline.
        """
        app_logger.info(f"CRIE Orchestrator executing pipeline for project '{project_context.get('project_id')}'")

        # Run 8-stage pipeline
        pipeline_output = self.pipeline.run_pipeline(
            project_context=project_context,
            agents=self.agents,
            aggregator=self.aggregator,
            recommendation_engine=self.recommendation_engine,
            assessment_id=assessment_id
        )

        # Evaluate Project Health
        health_info = self.health_engine.evaluate_health(
            overall_risk_score=pipeline_output["overall_risk_score"]
        )
        pipeline_output["project_health"] = health_info

        return pipeline_output

    def handle_event(self, event_type: str, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handles incoming system events and determines required CRIE analysis response.
        """
        return self.event_processor.process_event(event_type, event_payload)

risk_intelligence_engine = ConstructionRiskIntelligenceEngine()
