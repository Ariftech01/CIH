import time
from typing import Dict, Any, List
from datetime import datetime
from backend.risk_intelligence.engine.execution_planner import execution_planner
from backend.risk_intelligence.validators.risk_validator import RiskValidator
from backend.app_logging.logger import logger as app_logger

class AnalysisPipeline:
    """
    Standardized 8-stage Execution Pipeline for CRIE:
    Stage 1: Request Reception
    Stage 2: Validation
    Stage 3: Business Context Assembly & Normalization
    Stage 4: Execution Planning
    Stage 5: Analytical Component / Agent Execution
    Stage 6: Risk Aggregation
    Stage 7: Persistence
    Stage 8: Response Generation
    """

    def run_pipeline(
        self,
        project_context: Dict[str, Any],
        agents: List[Any],
        aggregator: Any,
        recommendation_engine: Any,
        assessment_id: str = "temp_id"
    ) -> Dict[str, Any]:
        start_time = time.time()
        project_id = project_context.get("project_id", "UNKNOWN")

        # Stage 1: Request Reception & Stage 2: Validation
        app_logger.info(f"Pipeline Stage 1 & 2: Validating request for project_id={project_id}")
        warnings = RiskValidator.validate_project_context(project_context)

        # Stage 3: Business Context Assembly
        app_logger.info(f"Pipeline Stage 3: Assembling context for project '{project_context.get('project_name')}'")

        # Stage 4: Execution Planning
        plan = execution_planner.plan_execution(analysis_type=project_context.get("analysis_type", "FULL"))
        app_logger.info(f"Pipeline Stage 4: Planned mode '{plan['mode']}' with {len(plan['target_agents'])} agents")

        # Stage 5: Agent Execution
        agent_results = []
        component_scores = {}
        for agent in agents:
            if agent.name in plan["target_agents"]:
                res = agent.execute(project_context)
                agent_results.append(res)
                if res.status == "SUCCESS" and res.weight > 0.0:
                    component_name = agent.name.replace(" Agent", "")
                    component_scores[component_name] = {
                        "category": component_name,
                        "score": res.score,
                        "weight": res.weight,
                        "status": "NORMAL",
                        "breakdown": res.findings
                    }

        # Stage 6: Risk Aggregation
        app_logger.info("Pipeline Stage 6: Aggregating risk scores")
        aggregated_res = aggregator.aggregate(component_scores)

        # Stage 7: Recommendations Generation
        recs = recommendation_engine.generate_recommendations(
            assessment_id=assessment_id,
            project_id=project_id,
            component_scores=component_scores
        )

        duration = (time.time() - start_time) * 1000.0

        # Stage 8: Response Generation
        return {
            "project_id": project_id,
            "assessment_id": assessment_id,
            "overall_risk_score": aggregated_res["overall_risk_score"],
            "risk_level": aggregated_res["risk_level"],
            "confidence_score": aggregated_res["confidence_score"],
            "component_scores": component_scores,
            "agent_results": [r.model_dump() for r in agent_results],
            "recommendations": recs,
            "warnings": warnings,
            "duration_ms": duration,
            "evaluated_at": datetime.utcnow().isoformat()
        }

analysis_pipeline = AnalysisPipeline()
