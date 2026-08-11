from typing import Dict, Any, List

class ComplianceRules:
    """
    Configurable deterministic business rules for evaluating regulatory compliance,
    permit status, inspection readiness, documentation completeness, certification validity,
    and audit preparedness.
    """

    @staticmethod
    def evaluate_violations(open_violations_count: int) -> Dict[str, Any]:
        """Legacy compatibility method for evaluating open violation count."""
        if open_violations_count == 0:
            return {"status": "FULL_COMPLIANCE", "compliance_score": 100.0, "level": "LOW"}
        elif open_violations_count <= 2:
            return {"status": "MINOR_NON_COMPLIANCE", "compliance_score": 75.0, "level": "MEDIUM"}
        else:
            return {"status": "MAJOR_NON_COMPLIANCE", "compliance_score": 40.0, "level": "HIGH"}

    @staticmethod
    def evaluate_permit_status(expired_count: int, renewal_due_count: int, missing_count: int = 0) -> Dict[str, Any]:
        """Evaluates construction permit status."""
        total_issues = expired_count + renewal_due_count + missing_count
        if total_issues == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "All Permits Valid & Active"}

        penalty = expired_count * 30.0 + missing_count * 25.0 + renewal_due_count * 10.0
        severity = "CRITICAL" if expired_count > 0 or missing_count > 0 else ("HIGH" if renewal_due_count >= 2 else "MODERATE")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 60.0),
            "title": f"Permit Compliance Breach ({expired_count} Expired, {renewal_due_count} Renewal Due)",
            "desc": f"Project has {expired_count} expired permit(s), {missing_count} missing permit(s), and {renewal_due_count} pending renewal(s)."
        }

    @staticmethod
    def evaluate_inspection_readiness(failed_count: int, overdue_count: int) -> Dict[str, Any]:
        """Evaluates mandatory municipal and structural inspection readiness."""
        total_issues = failed_count + overdue_count
        if total_issues == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Inspections Fully Up-To-Date"}

        penalty = failed_count * 25.0 + overdue_count * 15.0
        severity = "CRITICAL" if failed_count > 0 else ("HIGH" if overdue_count >= 2 else "MODERATE")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 50.0),
            "title": f"Inspection Deficiencies ({failed_count} Failed, {overdue_count} Overdue)",
            "desc": f"{failed_count} inspection(s) failed validation and {overdue_count} inspection(s) are overdue."
        }

    @staticmethod
    def evaluate_documentation_completeness(missing_doc_types: List[str]) -> Dict[str, Any]:
        """Evaluates required regulatory, safety, and environmental documentation completeness."""
        if not missing_doc_types:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Complete Regulatory Documentation"}

        count = len(missing_doc_types)
        penalty = count * 12.0
        severity = "HIGH" if count >= 3 else ("MODERATE" if count >= 2 else "MINOR")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 40.0),
            "title": f"Missing Mandatory Documents ({', '.join(missing_doc_types)})",
            "desc": f"Required compliance documents missing: {', '.join(missing_doc_types)}."
        }

    @staticmethod
    def evaluate_certification_validity(expired_certs_count: int, contractor_license_issues: int = 0) -> Dict[str, Any]:
        """Evaluates equipment certifications and contractor licenses."""
        total = expired_certs_count + contractor_license_issues
        if total == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Certifications & Licenses Valid"}

        penalty = expired_certs_count * 15.0 + contractor_license_issues * 20.0
        severity = "HIGH" if contractor_license_issues > 0 or expired_certs_count >= 3 else "MODERATE"

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 45.0),
            "title": f"Certification & License Non-Conformity ({expired_certs_count} Expired)",
            "desc": f"{expired_certs_count} equipment/safety certification(s) expired and {contractor_license_issues} contractor license issue(s) detected."
        }

    @staticmethod
    def evaluate_audit_readiness(past_deficiencies: int, open_policy_breaches: int) -> Dict[str, Any]:
        """Evaluates audit readiness and internal governance policy compliance."""
        total = past_deficiencies + open_policy_breaches
        if total == 0:
            return {"hazard_detected": False, "severity": "INFORMATIONAL", "score_penalty": 0.0, "title": "Full Audit Readiness"}

        penalty = past_deficiencies * 15.0 + open_policy_breaches * 10.0
        severity = "CRITICAL" if past_deficiencies >= 3 else ("HIGH" if total >= 3 else "MODERATE")

        return {
            "hazard_detected": True,
            "severity": severity,
            "score_penalty": min(penalty, 40.0),
            "title": f"Audit Readiness Deficiencies ({total} Issues)",
            "desc": f"{past_deficiencies} audit deficiency record(s) and {open_policy_breaches} open policy breach(es) active."
        }
