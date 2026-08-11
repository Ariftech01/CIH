from typing import Dict, Any, List

class InsuranceRules:
    """
    Configurable deterministic rules for evaluating insurance policy coverage,
    incident financial severity, asset exposure, liability risk, and claim documentation readiness.
    """

    @staticmethod
    def evaluate_policy_coverage(expired_policies_count: int, coverage_gaps_count: int, renewal_due_count: int = 0) -> Dict[str, Any]:
        """Evaluates project insurance policy coverage completeness."""
        total = expired_policies_count + coverage_gaps_count + renewal_due_count
        if total == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Full Insurance Policy Coverage"}

        penalty = expired_policies_count * 30.0 + coverage_gaps_count * 20.0 + renewal_due_count * 10.0
        severity = "CRITICAL" if expired_policies_count > 0 else ("HIGH" if coverage_gaps_count >= 2 else "MODERATE")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 60.0),
            "title": f"Insurance Policy Coverage Deficiencies ({expired_policies_count} Expired, {coverage_gaps_count} Gaps)",
            "desc": f"Insurance policy review revealed {expired_policies_count} expired policy/policies, {coverage_gaps_count} coverage gap(s), and {renewal_due_count} pending renewal(s)."
        }

    @staticmethod
    def evaluate_incident_severity(high_severity_incidents: int, total_financial_impact: float) -> Dict[str, Any]:
        """Evaluates historical financial and operational incident impact on insurance exposure."""
        if high_severity_incidents == 0 and total_financial_impact == 0.0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Zero High-Severity Incidents"}

        penalty = high_severity_incidents * 20.0
        if total_financial_impact > 100000.0:
            penalty += 30.0
        elif total_financial_impact > 25000.0:
            penalty += 15.0

        severity = "CRITICAL" if total_financial_impact > 100000.0 or high_severity_incidents >= 3 else ("HIGH" if high_severity_incidents >= 1 else "MODERATE")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 55.0),
            "title": f"High Incident Loss Exposure (${total_financial_impact:,.2f} Total Impact)",
            "desc": f"{high_severity_incidents} high-severity incident(s) recorded with total financial exposure of ${total_financial_impact:,.2f}."
        }

    @staticmethod
    def evaluate_asset_exposure(uninsured_assets_count: int, high_value_unprotected_assets: int = 0) -> Dict[str, Any]:
        """Evaluates uninsured or underinsured high-value machinery and property assets."""
        total = uninsured_assets_count + high_value_unprotected_assets
        if total == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "All Capital Assets Fully Insured"}

        penalty = uninsured_assets_count * 15.0 + high_value_unprotected_assets * 25.0
        severity = "HIGH" if high_value_unprotected_assets > 0 or uninsured_assets_count >= 3 else "MODERATE"

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 45.0),
            "title": f"Uninsured Asset Exposure ({total} Assets at Risk)",
            "desc": f"{uninsured_assets_count} equipment asset(s) uninsured and {high_value_unprotected_assets} high-value asset(s) lack full property damage coverage."
        }

    @staticmethod
    def evaluate_liability_exposure(third_party_claims_count: int, public_liability_risks: int = 0) -> Dict[str, Any]:
        """Evaluates 3rd party, public, and worker compensation liability exposure."""
        total = third_party_claims_count + public_liability_risks
        if total == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Low Liability Risk"}

        penalty = third_party_claims_count * 20.0 + public_liability_risks * 15.0
        severity = "HIGH" if third_party_claims_count >= 2 else "MODERATE"

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 40.0),
            "title": f"Third-Party Liability Exposure ({third_party_claims_count} Active Claims)",
            "desc": f"{third_party_claims_count} third-party liability claim(s) and {public_liability_risks} public liability hazard(s) identified."
        }

    @staticmethod
    def evaluate_claim_readiness(missing_claim_docs: int, unverified_incidents: int = 0) -> Dict[str, Any]:
        """Evaluates claim documentation completeness and audit evidence package readiness."""
        total = missing_claim_docs + unverified_incidents
        if total == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Claim Documentation Package Complete"}

        penalty = missing_claim_docs * 10.0 + unverified_incidents * 15.0
        severity = "HIGH" if missing_claim_docs >= 3 or unverified_incidents >= 2 else "MODERATE"

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 35.0),
            "title": f"Incomplete Claim Documentation Package ({total} Deficiencies)",
            "desc": f"{missing_claim_docs} required claim document(s) missing and {unverified_incidents} incident(s) lack witness/photo verification."
        }
