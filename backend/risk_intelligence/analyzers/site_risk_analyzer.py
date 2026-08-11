from typing import Dict, Any, List
from backend.risk_intelligence.rules.site_rules import SiteRules
from backend.risk_intelligence.schemas.site_risk import SiteFinding, SiteHazard
from backend.risk_intelligence.utils.helpers import normalize_risk_score

class SiteRiskAnalyzer:
    """
    Dedicated Site Risk Analyzer.
    Applies deterministic SiteRules, identifies physical hazards, generates structured findings,
    and calculates the Site Risk Score independently of overall project risk score.
    """

    def analyze_site_conditions(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        building_count = context_data.get("building_count", 1)
        equipment_list = context_data.get("equipment_list", [])
        material_list = context_data.get("material_list", [])
        incidents_list = context_data.get("incidents_list", [])

        equipment_count = len(equipment_list) if equipment_list else context_data.get("equipment_count", 0)
        total_materials = len(material_list) if material_list else context_data.get("material_count", 0)
        low_stock_materials = sum(1 for m in material_list if m.get("quantity", 0) <= m.get("min_stock_level", 0))
        overdue_equipment = sum(1 for e in equipment_list if e.get("status") == "MAINTENANCE" or e.get("is_overdue"))

        incidents_count = len(incidents_list) if incidents_list else context_data.get("incidents_count", 0)
        high_sev_incidents = sum(1 for i in incidents_list if i.get("severity") in ["HIGH", "CRITICAL"])

        # Run Rule Evaluations
        eval_layout = SiteRules.evaluate_layout_congestion(building_count, equipment_count)
        eval_material = SiteRules.evaluate_material_storage(low_stock_materials, total_materials)
        eval_equipment = SiteRules.evaluate_equipment_maintenance(overdue_equipment)
        eval_incidents = SiteRules.evaluate_incidents_history(incidents_count, high_sev_incidents)

        hazards: List[SiteHazard] = []
        findings: List[SiteFinding] = []
        total_penalty = 0.0

        evaluations = [
            ("Site Layout", eval_layout, "Optimize equipment positioning and zoning."),
            ("Material Storage", eval_material, "Reorder low inventory raw materials and organize storage bays."),
            ("Equipment Placement", eval_equipment, "Schedule overdue machinery inspections immediately."),
            ("Incident Record", eval_incidents, "Perform site hazard inspection and review safety protocols.")
        ]

        idx = 1
        for category, res, rec_action in evaluations:
            if res["hazard_detected"]:
                total_penalty += res["score_penalty"]
                hazard_obj = SiteHazard(
                    hazard_id=f"HAZ_{idx:03d}",
                    category=category,
                    title=res["title"],
                    severity=res["severity"],
                    description=res["desc"],
                    location="General Site Zone",
                    business_justification=f"Condition breaches safe operational thresholds with penalty {res['score_penalty']} pts.",
                    evidence=f"Category '{category}' evaluated with status '{res['severity']}'."
                )
                hazards.append(hazard_obj)

                finding_obj = SiteFinding(
                    category=category,
                    title=res["title"],
                    description=res["desc"],
                    severity=res["severity"],
                    location="General Site Zone",
                    evidence=f"Rule penalty: {res['score_penalty']} pts",
                    suggested_action=rec_action
                )
                findings.append(finding_obj)
                idx += 1

        # Baseline score calculation normalized to [0.0, 100.0]
        site_risk_score = normalize_risk_score(10.0 + total_penalty)

        return {
            "site_risk_score": site_risk_score,
            "hazards": [h.model_dump() for h in hazards],
            "findings": [f.model_dump() for f in findings],
            "total_hazards_count": len(hazards),
            "critical_hazards_count": sum(1 for h in hazards if h.severity == "CRITICAL")
        }

site_risk_analyzer = SiteRiskAnalyzer()
