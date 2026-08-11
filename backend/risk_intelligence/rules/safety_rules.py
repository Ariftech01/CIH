from typing import Dict, Any, List

class SafetyRules:
    """
    Configurable deterministic rules for evaluating workforce safety, PPE compliance,
    unsafe work practices, occupational hazard exposure, near-miss frequency, and high-risk activities.
    """
    DEFAULT_MIN_PPE_THRESHOLD = 90.0
    HIGH_HAZARD_INCIDENT_COUNT = 3

    @staticmethod
    def evaluate_ppe_compliance(compliance_rate: float) -> Dict[str, Any]:
        """Legacy compatibility method for evaluating overall PPE compliance rate."""
        if compliance_rate >= 95.0:
            return {"status": "PASS", "risk_level": "LOW", "score_penalty": 0.0}
        elif compliance_rate >= 85.0:
            return {"status": "WARNING", "risk_level": "MEDIUM", "score_penalty": 15.0}
        else:
            return {"status": "FAIL", "risk_level": "HIGH", "score_penalty": 35.0}

    @staticmethod
    def evaluate_incident_frequency(recent_incidents_count: int) -> Dict[str, Any]:
        """Legacy compatibility method for evaluating recent incident frequency."""
        if recent_incidents_count == 0:
            return {"status": "OPTIMAL", "risk_impact": "NONE", "score_penalty": 0.0}
        elif recent_incidents_count <= 2:
            return {"status": "ELEVATED", "risk_impact": "MODERATE", "score_penalty": 20.0}
        else:
            return {"status": "CRITICAL", "risk_impact": "SEVERE", "score_penalty": 50.0}

    @staticmethod
    def evaluate_ppe_item_violations(missing_items: List[str]) -> Dict[str, Any]:
        """Evaluates specific missing PPE items (helmet, vest, gloves, boots, fall harness, eye, respiratory)."""
        if not missing_items:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Full PPE Compliance"}

        penalty = 0.0
        critical_items = ["helmet", "harness", "respirator", "fall_protection"]
        has_critical = any(item.lower() in [c.lower() for c in missing_items] for item in missing_items)

        for item in missing_items:
            item_lower = item.lower()
            if "helmet" in item_lower or "harness" in item_lower:
                penalty += 25.0
            elif "vest" in item_lower or "boot" in item_lower:
                penalty += 15.0
            elif "glove" in item_lower or "eye" in item_lower:
                penalty += 10.0
            else:
                penalty += 10.0

        severity = "CRITICAL" if has_critical or len(missing_items) >= 3 else ("HIGH" if len(missing_items) >= 2 else "MODERATE")
        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 60.0),
            "title": f"Missing PPE: {', '.join(missing_items)}",
            "desc": f"Worker(s) observed missing essential PPE items: {', '.join(missing_items)}. Breaches safety policy."
        }

    @staticmethod
    def evaluate_unsafe_behaviour(behaviour_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates observed unsafe worker practices."""
        if not behaviour_logs:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "No Unsafe Behaviour Observed"}

        count = len(behaviour_logs)
        critical_count = sum(1 for b in behaviour_logs if b.get("severity") == "CRITICAL" or "restricted" in str(b).lower() or "fall" in str(b).lower())

        penalty = count * 12.0 + critical_count * 15.0
        severity = "CRITICAL" if critical_count > 0 or count >= 4 else ("HIGH" if count >= 2 else "MODERATE")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 50.0),
            "title": f"Unsafe Worker Practices ({count} Logged)",
            "desc": f"{count} unsafe work practice observation(s) logged on site ({critical_count} critical breaches)."
        }

    @staticmethod
    def evaluate_hazard_exposure(active_high_risk_activities: List[str], zone_hazards: List[str]) -> Dict[str, Any]:
        """Evaluates worker exposure to high-risk work environments (height, excavation, electrical, hot work, confined space)."""
        all_hazards = list(set(active_high_risk_activities + zone_hazards))
        if not all_hazards:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Standard Work Environment"}

        penalty = len(all_hazards) * 10.0
        high_risk_keys = ["working_at_height", "confined_space", "excavation", "electrical", "hot_work"]
        critical_exposure = any(k in [h.lower().replace(" ", "_") for h in all_hazards] for k in high_risk_keys)

        severity = "HIGH" if critical_exposure or len(all_hazards) >= 3 else "MODERATE"
        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 40.0),
            "title": f"Occupational Hazard Exposure ({len(all_hazards)} Active Hazards)",
            "desc": f"Workforce exposed to high-risk hazards: {', '.join(all_hazards)} without full safety isolation."
        }

    @staticmethod
    def evaluate_near_miss_records(near_miss_count: int, recurring_pattern: bool = False) -> Dict[str, Any]:
        """Evaluates frequency and recurrence of near-miss safety incidents."""
        if near_miss_count == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Zero Near-Miss Incidents"}

        penalty = near_miss_count * 10.0 + (20.0 if recurring_pattern else 0.0)
        severity = "CRITICAL" if recurring_pattern or near_miss_count >= 3 else ("HIGH" if near_miss_count >= 2 else "MODERATE")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 45.0),
            "title": f"Near-Miss Incident Pattern ({near_miss_count} Records)",
            "desc": f"{near_miss_count} near-miss incident(s) recorded. Recurring pattern: {recurring_pattern}."
        }
