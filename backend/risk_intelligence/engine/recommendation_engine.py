from typing import List, Dict, Any
from backend.risk_intelligence.recommendations.generator import RecommendationGenerator
from backend.risk_intelligence.constants import RecommendationPriority

class EnterpriseRecommendationEngine:
    """
    Deterministic Enterprise Recommendation Engine.
    Generates, deduplicates, groups, and prioritizes actionable construction recommendations
    from component findings without LLM reasoning.
    """

    def __init__(self):
        self.generator = RecommendationGenerator()

    def generate_recommendations(
        self,
        assessment_id: str,
        project_id: str,
        component_scores: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        # Convert dict format to schema component scores if needed
        from backend.risk_intelligence.schemas.score import ComponentScoreResult

        comp_objects = {}
        for k, v in component_scores.items():
            if isinstance(v, dict):
                comp_objects[k] = ComponentScoreResult(
                    category=k,
                    score=v.get("score", 0.0),
                    weight=v.get("weight", 1.0),
                    status=v.get("status", "NORMAL"),
                    breakdown=v.get("breakdown", {})
                )
            else:
                comp_objects[k] = v

        raw_recs = self.generator.generate_recommendations(
            assessment_id=assessment_id,
            project_id=project_id,
            component_scores=comp_objects
        )

        # Deduplicate & format recommendations
        unique_recs = {}
        for r in raw_recs:
            rec_dict = r.model_dump()
            key = f"{rec_dict['category']}_{rec_dict['title']}"
            if key not in unique_recs:
                unique_recs[key] = rec_dict

        sorted_recs = sorted(
            list(unique_recs.values()),
            key=lambda x: 0 if x.get("priority") == RecommendationPriority.CRITICAL.value else (1 if x.get("priority") == RecommendationPriority.HIGH.value else 2)
        )
        return sorted_recs

enterprise_recommendation_engine = EnterpriseRecommendationEngine()
