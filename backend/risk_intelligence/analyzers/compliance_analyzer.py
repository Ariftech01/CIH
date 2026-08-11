from typing import Dict, Any, List, Optional
from backend.risk_intelligence.rules.compliance_rules import ComplianceRules
from backend.risk_intelligence.schemas.compliance_risk import (
    ComplianceFinding, ComplianceHazard, ProjectGovernanceProfile, ContractorComplianceProfile, ComplianceMetric
)
from backend.risk_intelligence.utils.helpers import normalize_risk_score
from backend.app_logging.logger import logger as app_logger

class ComplianceAnalyzer:
    """
    Dedicated Regulatory Compliance Analyzer.
    Applies deterministic ComplianceRules, evaluates permit status, inspection readiness,
    documentation completeness, certification validity, and audit preparedness.
    Calculates the Compliance Score independently of overall project risk score and generates structured findings.
    """

    def analyze_compliance_conditions(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes complete 10-stage deterministic regulatory compliance analysis pipeline.
        Returns Compliance Score, hazards, findings, governance profiles, metrics, and metadata.
        """
        app_logger.info("ComplianceAnalyzer commencing comprehensive regulatory compliance evaluation.")

        # 1. Context Extraction
        project_id = context_data.get("project_id", "UNKNOWN_PROJECT")
        project_name = context_data.get("project_name", "Construction Project")
        
        permits_list = context_data.get("permit_records", []) or context_data.get("permits", [])
        inspections_list = context_data.get("inspection_records", []) or context_data.get("inspections", [])
        missing_docs = context_data.get("missing_documents", []) or context_data.get("missing_doc_types", [])
        contractors_list = context_data.get("contractors_list", []) or context_data.get("subcontractors", [])
        
        expired_permits = sum(1 for p in permits_list if p.get("status") in ["EXPIRED", "REVOKED"])
        renewal_due_permits = sum(1 for p in permits_list if p.get("status") in ["RENEWAL_DUE", "PENDING_RENEWAL"])
        missing_permits = context_data.get("missing_permits_count", 0)

        failed_inspections = sum(1 for i in inspections_list if i.get("status") in ["FAILED", "DEFICIENCY"])
        overdue_inspections = sum(1 for i in inspections_list if i.get("status") == "OVERDUE")

        expired_certs = context_data.get("expired_certifications_count", 0)
        contractor_license_issues = sum(1 for c in contractors_list if c.get("license_status") in ["EXPIRED", "SUSPENDED"])

        audit_deficiencies = context_data.get("audit_deficiencies_count", 0)
        policy_breaches = context_data.get("open_violations_count", 0)

        # 2. Rule Evaluations
        eval_permits = ComplianceRules.evaluate_permit_status(expired_permits, renewal_due_permits, missing_permits)
        eval_inspections = ComplianceRules.evaluate_inspection_readiness(failed_inspections, overdue_inspections)
        eval_docs = ComplianceRules.evaluate_documentation_completeness(missing_docs)
        eval_certs = ComplianceRules.evaluate_certification_validity(expired_certs, contractor_license_issues)
        eval_audit = ComplianceRules.evaluate_audit_readiness(audit_deficiencies, policy_breaches)

        hazards: List[ComplianceHazard] = []
        findings: List[ComplianceFinding] = []
        total_penalty = 0.0

        evaluations = [
            ("Permit Compliance", eval_permits, "Submit urgent permit renewal applications to municipal building authorities immediately."),
            ("Inspection Readiness", eval_inspections, "Rectify noted structural/safety inspection deficiencies and reschedule municipal review."),
            ("Documentation Completeness", eval_docs, "Compile and upload missing regulatory and environmental compliance documentation."),
            ("Certification Validity", eval_certs, "Renew expired equipment certifications and verify contractor license standing."),
            ("Audit Readiness", eval_audit, "Address active audit deficiency logs and enforce corporate governance compliance.")
        ]

        idx = 1
        for category, res, rec_action in evaluations:
            if res.get("hazard_detected"):
                penalty = float(res.get("score_penalty", 0.0))
                total_penalty += penalty

                hazard_obj = ComplianceHazard(
                    hazard_id=f"CMP_HAZ_{idx:03d}",
                    category=category,
                    title=res.get("title", "Compliance Non-Conformity"),
                    severity=res.get("severity", "LOW"),
                    description=res.get("desc", ""),
                    regulation_ref="Building Code & Municipal Regulations",
                    business_justification=f"Regulatory compliance breach incurring {penalty} penalty points.",
                    evidence=f"Category '{category}' evaluated with severity '{res.get('severity')}'."
                )
                hazards.append(hazard_obj)

                finding_obj = ComplianceFinding(
                    category=category,
                    title=res.get("title", "Compliance Finding"),
                    description=res.get("desc", ""),
                    severity=res.get("severity", "LOW"),
                    regulation_ref="Building Code & Municipal Regulations",
                    evidence=f"Rule penalty: {penalty} pts",
                    suggested_action=rec_action,
                    priority="HIGH" if res.get("severity") in ["HIGH", "CRITICAL"] else "MEDIUM"
                )
                findings.append(finding_obj)
                idx += 1

        # 3. Compliance Risk Score Calculation (normalized 0.0 - 100.0 hazard scale)
        compliance_score = normalize_risk_score(10.0 + total_penalty)

        # 4. Governance Profiles Generation
        gov_profile = ProjectGovernanceProfile(
            project_id=project_id,
            project_name=project_name,
            permit_compliance_rate=max(100.0 - (expired_permits * 25.0), 0.0),
            inspection_completion_rate=max(100.0 - (failed_inspections * 20.0), 0.0),
            documentation_accuracy_rate=max(100.0 - (len(missing_docs) * 15.0), 0.0),
            certification_validity_rate=max(100.0 - (expired_certs * 15.0), 0.0),
            audit_readiness_index=max(100.0 - (audit_deficiencies * 20.0), 0.0),
            governance_maturity_level="DEVELOPING" if total_penalty > 30.0 else "MATURE",
            compliance_score=compliance_score
        )

        contractor_profiles: List[ContractorComplianceProfile] = [
            ContractorComplianceProfile(
                contractor_id=c.get("id", f"CONT_{i+1}"),
                contractor_name=c.get("name", f"Contractor {i+1}"),
                trade=c.get("trade", "General Construction"),
                permit_status=c.get("license_status", "VALID"),
                violation_count=c.get("violations_count", 0),
                compliance_score=compliance_score
            )
            for i, c in enumerate(contractors_list[:5])
        ]

        # 5. Executive Metrics
        metrics = [
            ComplianceMetric(metric_name="Permit Compliance Rate", metric_value=gov_profile.permit_compliance_rate, category="PERMIT", status=eval_permits.get("severity", "OPTIMAL"), description="Percentage of active valid building permits"),
            ComplianceMetric(metric_name="Inspection Readiness Index", metric_value=gov_profile.inspection_completion_rate, category="INSPECTION", status=eval_inspections.get("severity", "OPTIMAL"), description="Pass rate of required site inspections"),
            ComplianceMetric(metric_name="Audit Readiness Index", metric_value=gov_profile.audit_readiness_index, category="AUDIT", status=eval_audit.get("severity", "OPTIMAL"), description="Preparedness index for regulatory audits")
        ]

        return {
            "compliance_score": compliance_score,
            "hazards": [h.model_dump() for h in hazards],
            "findings": [f.model_dump() for f in findings],
            "governance_profile": gov_profile.model_dump(),
            "contractor_profiles": [cp.model_dump() for cp in contractor_profiles],
            "metrics": [m.model_dump() for m in metrics],
            "total_hazards_count": len(hazards),
            "critical_hazards_count": sum(1 for h in hazards if h.severity == "CRITICAL"),
            "permits_evaluated_count": len(permits_list),
            "inspections_reviewed_count": len(inspections_list),
            "documents_verified_count": len(missing_docs)
        }

compliance_analyzer = ComplianceAnalyzer()
