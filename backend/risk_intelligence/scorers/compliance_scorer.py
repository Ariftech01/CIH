from typing import Dict, Any
from backend.risk_intelligence.schemas.score import ComponentScoreResult
from backend.risk_intelligence.rules.compliance_rules import ComplianceRules

class ComplianceScorer:
    """
    Calculates Compliance Risk Score based on regulation checks and violation logs.
    """
    def calculate_score(self, context_data: Dict[str, Any]) -> ComponentScoreResult:
        violations_count = context_data.get("open_violations_count", 0)
        eval_res = ComplianceRules.evaluate_violations(violations_count)

        # Risk score is inverted compliance score (100 - compliance_score)
        risk_score = 100.0 - eval_res["compliance_score"]

        return ComponentScoreResult(
            category="Compliance",
            score=risk_score,
            weight=1.3,
            status=eval_res["status"],
            breakdown={
                "open_violations_count": violations_count,
                "compliance_score": eval_res["compliance_score"]
            }
        )
