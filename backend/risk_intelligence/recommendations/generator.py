from typing import List, Dict, Any
from backend.risk_intelligence.schemas.score import ComponentScoreResult
from backend.risk_intelligence.schemas.recommendation import RecommendationCreate

class RecommendationGenerator:
    """
    Generates categorized, prioritized, and evidence-backed actionable recommendations
    based on component risk scores and analysis findings.
    """
    def generate_recommendations(
        self,
        assessment_id: str,
        project_id: str,
        component_scores: Dict[str, ComponentScoreResult]
    ) -> List[RecommendationCreate]:
        recs: List[RecommendationCreate] = []

        # Safety Recommendations
        safety = component_scores.get("Safety")
        if safety and safety.score > 30.0:
            recs.append(
                RecommendationCreate(
                    assessment_id=assessment_id,
                    project_id=project_id,
                    category="Safety",
                    priority="HIGH" if safety.score > 60 else "MEDIUM",
                    title="Mandatory Site Safety Audit & PPE Verification",
                    description="Safety risk score elevated due to recent incident logs or PPE non-compliance.",
                    suggested_action="Conduct site-wide safety briefing and verify PPE compliance across all active shifts.",
                    supporting_evidence=f"Safety Score: {safety.score}/100"
                )
            )

        # Site Risk / Equipment Recommendations
        site = component_scores.get("Site Risk")
        if site and site.score > 40.0:
            recs.append(
                RecommendationCreate(
                    assessment_id=assessment_id,
                    project_id=project_id,
                    category="Site Operational Risk",
                    priority="HIGH",
                    title="Equipment Maintenance & Supply Chain Inspection",
                    description="Site risk elevated due to heavy machinery load or inventory shortage.",
                    suggested_action="Inspect equipment maintenance logs and reorder critical raw materials.",
                    supporting_evidence=f"Site Risk Score: {site.score}/100"
                )
            )

        # Compliance Recommendations
        compliance = component_scores.get("Compliance")
        if compliance and compliance.score > 25.0:
            recs.append(
                RecommendationCreate(
                    assessment_id=assessment_id,
                    project_id=project_id,
                    category="Compliance",
                    priority="HIGH",
                    title="Resolve Outstanding Regulatory Non-Compliance Records",
                    description="Compliance violations detected on current project records.",
                    suggested_action="Review local building code checklist and resolve open compliance tickets.",
                    supporting_evidence=f"Compliance Penalty: {compliance.score}/100"
                )
            )

        # Insurance Recommendations
        insurance = component_scores.get("Insurance Exposure")
        if insurance and insurance.score > 40.0:
            recs.append(
                RecommendationCreate(
                    assessment_id=assessment_id,
                    project_id=project_id,
                    category="Insurance",
                    priority="MEDIUM",
                    title="Review Insurance Liability & Claim Preparedness",
                    description="High incident exposure recorded for high-budget project assets.",
                    suggested_action="Verify active insurance policies and prepare incident documentation for risk audit.",
                    supporting_evidence=f"Insurance Exposure Score: {insurance.score}/100"
                )
            )

        return recs
