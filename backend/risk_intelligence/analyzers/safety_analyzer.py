from typing import Dict, Any, List, Optional
from backend.risk_intelligence.rules.safety_rules import SafetyRules
from backend.risk_intelligence.schemas.safety_risk import (
    SafetyFinding, SafetyHazard, WorkerSafetyProfile, WorkgroupSafetyProfile, SafetyMetric
)
from backend.risk_intelligence.utils.helpers import normalize_risk_score
from backend.app_logging.logger import logger as app_logger

class SafetyAnalyzer:
    """
    Dedicated Safety Analyzer.
    Applies deterministic SafetyRules, evaluates PPE compliance, unsafe work practices,
    occupational hazard exposure, near misses, and calculates the Safety Score independently.
    Generates structured Safety Findings and workforce safety profiles.
    """

    def analyze(self, safety_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Legacy compatibility method for simple safety records list analysis."""
        total = len(safety_records)
        if total == 0:
            return {"safety_risk_score": 15.0, "violations": 0, "status": "NO_SAFETY_LOGS"}

        violations = sum(1 for s in safety_records if s.get("status") in ["FAIL", "HAZARD_DETECTED"])
        return {
            "total_inspections": total,
            "violations": violations,
            "safety_risk_score": min((violations / float(total)) * 100.0, 100.0),
            "status": "SAFETY_HAZARD" if violations > 0 else "SAFE"
        }

    def analyze_safety_conditions(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes complete 10-stage deterministic workforce safety analysis pipeline.
        Returns Safety Score, hazards, findings, profiles, metrics, and execution metadata.
        """
        app_logger.info("SafetyAnalyzer commencing comprehensive workforce safety evaluation.")

        # 1. Input Validation & Worker Context Extraction
        worker_list = context_data.get("worker_list", []) or context_data.get("workers", [])
        worker_count = len(worker_list) if worker_list else context_data.get("worker_count", 0)

        normalized_obs = context_data.get("normalized_safety_observations", [])
        ppe_compliance = context_data.get("ppe_compliance_rate", 90.0)
        incidents_list = context_data.get("incidents_list", []) or context_data.get("safety_incidents", [])
        incidents_count = len(incidents_list) if incidents_list else context_data.get("incidents_count", 0)
        near_misses_count = context_data.get("near_misses_count", 0)
        high_risk_activities = context_data.get("high_risk_activities", [])
        missing_ppe_items = context_data.get("missing_ppe_items", [])

        # 2. Extract observations by category
        ppe_obs = [o for o in normalized_obs if o.get("category") == "PPE"]
        behaviour_obs = [o for o in normalized_obs if o.get("category") == "UNSAFE_BEHAVIOUR"]
        exposure_obs = [o for o in normalized_obs if o.get("category") in ["HAZARD_EXPOSURE", "RESTRICTED_AREA"]]

        if not missing_ppe_items and ppe_obs:
            missing_ppe_items = [o.get("evidence", "Missing PPE") for o in ppe_obs]

        # 3. Deterministic Safety Rule Evaluations
        eval_ppe_rate = SafetyRules.evaluate_ppe_compliance(ppe_compliance)
        eval_ppe_items = SafetyRules.evaluate_ppe_item_violations(missing_ppe_items)
        eval_behaviour = SafetyRules.evaluate_unsafe_behaviour(behaviour_obs)
        eval_exposure = SafetyRules.evaluate_hazard_exposure(high_risk_activities, [o.get("location", "") for o in exposure_obs])
        eval_incidents = SafetyRules.evaluate_incident_frequency(incidents_count)
        eval_near_misses = SafetyRules.evaluate_near_miss_records(near_misses_count, recurring_pattern=(near_misses_count >= 2))

        hazards: List[SafetyHazard] = []
        findings: List[SafetyFinding] = []
        total_penalty = 0.0

        evaluations = [
            ("PPE Compliance Rate", {"hazard_detected": eval_ppe_rate["status"] == "FAIL", "severity": eval_ppe_rate["risk_level"], "score_penalty": eval_ppe_rate["score_penalty"], "title": f"PPE Compliance Rate: {ppe_compliance}%", "desc": f"Overall site PPE compliance rate is {ppe_compliance}%."}, "Enforce mandatory site PPE inspections and daily tool box talks."),
            ("Missing PPE Equipment", eval_ppe_items, "Provide missing PPE equipment immediately and restrict unequipped workers."),
            ("Unsafe Work Practices", eval_behaviour, "Issue immediate safety stand-down and re-train workers on safe operational procedures."),
            ("Occupational Hazard Exposure", eval_exposure, "Implement safety barrier isolation and continuous gas/height monitoring."),
            ("Historical Safety Incidents", {"hazard_detected": eval_incidents["status"] != "OPTIMAL", "severity": eval_incidents["risk_impact"], "score_penalty": eval_incidents["score_penalty"], "title": f"Recent Incident Count ({incidents_count})", "desc": f"{incidents_count} safety incident(s) reported in current phase."}, "Investigate root causes of past incidents and implement preventive controls."),
            ("Near-Miss Recurrence", eval_near_misses, "Review near-miss reporting logs and address root cause conditions immediately.")
        ]

        idx = 1
        for category, res, rec_action in evaluations:
            if res.get("hazard_detected"):
                penalty = float(res.get("score_penalty", 0.0))
                total_penalty += penalty

                hazard_obj = SafetyHazard(
                    hazard_id=f"SAF_HAZ_{idx:03d}",
                    category=category,
                    title=res.get("title", "Safety Hazard"),
                    severity=res.get("severity", "LOW"),
                    description=res.get("desc", ""),
                    location=context_data.get("work_zone", "General Work Zone"),
                    business_justification=f"Workforce safety breach incurring {penalty} penalty points.",
                    evidence=f"Category '{category}' evaluated with severity '{res.get('severity')}'."
                )
                hazards.append(hazard_obj)

                finding_obj = SafetyFinding(
                    category=category,
                    title=res.get("title", "Safety Finding"),
                    description=res.get("desc", ""),
                    severity=res.get("severity", "LOW"),
                    location=context_data.get("work_zone", "General Work Zone"),
                    evidence=f"Rule penalty: {penalty} pts",
                    suggested_action=rec_action,
                    priority="HIGH" if res.get("severity") in ["HIGH", "CRITICAL"] else "MEDIUM"
                )
                findings.append(finding_obj)
                idx += 1

        # 4. Safety Score Calculation (normalized 0.0 - 100.0 hazard scale)
        safety_score = normalize_risk_score(10.0 + total_penalty)

        # 5. Worker & Workgroup Safety Profiles Generation
        worker_profiles: List[WorkerSafetyProfile] = []
        for w in worker_list[:10]:
            w_id = w.get("id") or w.get("worker_id") or f"W_{idx}"
            w_name = w.get("name", f"Worker {w_id}")
            trade = w.get("trade") or w.get("role", "General Labour")
            w_profile = WorkerSafetyProfile(
                worker_id=str(w_id),
                worker_name=w_name,
                trade=trade,
                ppe_compliance_rate=ppe_compliance,
                risk_level="HIGH" if len(findings) > 2 else "LOW",
                safety_score=max(100.0 - total_penalty, 0.0)
            )
            worker_profiles.append(w_profile)

        trade_groups: Dict[str, int] = {}
        for wp in worker_profiles:
            trade_groups[wp.trade] = trade_groups.get(wp.trade, 0) + 1

        workgroup_profiles: List[WorkgroupSafetyProfile] = [
            WorkgroupSafetyProfile(
                group_id=f"GRP_{trade.upper().replace(' ', '_')}",
                group_name=f"{trade} Team",
                worker_count=count,
                average_safety_score=safety_score,
                common_violations=[f.category for f in findings[:2]],
                ppe_compliance_rate=ppe_compliance
            )
            for trade, count in trade_groups.items()
        ]

        # 6. Executive Metrics
        metrics = [
            SafetyMetric(metric_name="PPE Compliance Rate", metric_value=ppe_compliance, category="PPE", status=eval_ppe_rate["status"], description="Overall PPE compliance percentage"),
            SafetyMetric(metric_name="Unsafe Behaviours Count", metric_value=float(len(behaviour_obs)), category="BEHAVIOUR", status="ELEVATED" if len(behaviour_obs) > 0 else "OPTIMAL", description="Number of observed unsafe practices"),
            SafetyMetric(metric_name="Near-Miss Incidents", metric_value=float(near_misses_count), category="INCIDENTS", status="WARNING" if near_misses_count > 0 else "OPTIMAL", description="Number of near-miss records logged")
        ]

        return {
            "safety_score": safety_score,
            "hazards": [h.model_dump() for h in hazards],
            "findings": [f.model_dump() for f in findings],
            "worker_profiles": [wp.model_dump() for wp in worker_profiles],
            "workgroup_profiles": [gp.model_dump() for gp in workgroup_profiles],
            "metrics": [m.model_dump() for m in metrics],
            "total_hazards_count": len(hazards),
            "critical_hazards_count": sum(1 for h in hazards if h.severity == "CRITICAL"),
            "workers_evaluated_count": worker_count,
            "observed_conditions_count": len(normalized_obs)
        }

safety_analyzer = SafetyAnalyzer()
