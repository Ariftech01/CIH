from typing import Dict, Any, List, Optional
from backend.risk_intelligence.rules.insurance_rules import InsuranceRules
from backend.risk_intelligence.schemas.insurance_risk import (
    InsuranceFinding, InsuranceHazard, ProjectInsuranceProfile, AssetInsuranceProfile, InsuranceMetric
)
from backend.risk_intelligence.utils.helpers import normalize_risk_score
from backend.app_logging.logger import logger as app_logger

class InsuranceAnalyzer:
    """
    Dedicated Insurance Exposure Analyzer.
    Applies deterministic InsuranceRules, evaluates policy coverage, incident financial severity,
    asset exposure, liability risk, and claim documentation readiness.
    Calculates the Insurance Score independently of overall project risk score and generates structured findings.
    """

    def analyze_insurance_conditions(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes complete 10-stage deterministic insurance exposure analysis pipeline.
        Returns Insurance Score, hazards, findings, insurance profiles, metrics, and metadata.
        """
        app_logger.info("InsuranceAnalyzer commencing comprehensive insurance exposure evaluation.")

        # 1. Context Extraction
        project_id = context_data.get("project_id", "UNKNOWN_PROJECT")
        project_name = context_data.get("project_name", "Construction Project")

        policies_list = context_data.get("policy_records", []) or context_data.get("policies", [])
        incidents_list = context_data.get("incidents_list", []) or context_data.get("incidents", [])
        equipment_list = context_data.get("equipment_list", []) or context_data.get("assets", [])
        claims_list = context_data.get("claims_list", []) or context_data.get("claims", [])

        expired_policies = sum(1 for p in policies_list if p.get("status") in ["EXPIRED", "CANCELLED"])
        coverage_gaps = context_data.get("coverage_gaps_count", 0)
        renewal_due_policies = sum(1 for p in policies_list if p.get("status") in ["RENEWAL_DUE", "PENDING_RENEWAL"])

        high_sev_incidents = sum(1 for i in incidents_list if i.get("severity") in ["HIGH", "CRITICAL"])
        total_financial_loss = sum(float(i.get("financial_impact", 0.0)) for i in incidents_list)

        uninsured_assets = sum(1 for e in equipment_list if e.get("insurance_status") in ["UNINSURED", "EXPIRED"])
        high_val_unprotected = sum(1 for e in equipment_list if e.get("replacement_value", 0) > 100000 and e.get("insurance_status") != "COVERED")

        third_party_claims = sum(1 for c in claims_list if c.get("type") in ["THIRD_PARTY", "PUBLIC_LIABILITY"])
        public_liability_risks = context_data.get("public_liability_risks_count", 0)

        missing_claim_docs = context_data.get("missing_claim_docs_count", 0)
        unverified_incidents = sum(1 for i in incidents_list if not i.get("evidence_attached", True))

        # 2. Rule Evaluations
        eval_policy = InsuranceRules.evaluate_policy_coverage(expired_policies, coverage_gaps, renewal_due_policies)
        eval_incidents = InsuranceRules.evaluate_incident_severity(high_sev_incidents, total_financial_loss)
        eval_assets = InsuranceRules.evaluate_asset_exposure(uninsured_assets, high_val_unprotected)
        eval_liability = InsuranceRules.evaluate_liability_exposure(third_party_claims, public_liability_risks)
        eval_claims = InsuranceRules.evaluate_claim_readiness(missing_claim_docs, unverified_incidents)

        hazards: List[InsuranceHazard] = []
        findings: List[InsuranceFinding] = []
        total_penalty = 0.0

        evaluations = [
            ("Policy Coverage", eval_policy, "Renew expired policies and eliminate coverage gaps with primary insurer immediately."),
            ("Incident Loss Severity", eval_incidents, "Perform forensic root cause analysis on high-loss incidents and prepare insurance claim dossier."),
            ("Capital Asset Exposure", eval_assets, "Bind property damage and inland marine insurance for high-value heavy equipment."),
            ("Third-Party Liability", eval_liability, "Review public liability limits and notify insurance broker of active third-party exposure."),
            ("Claim Documentation Readiness", eval_claims, "Complete witness statements, site photo logs, and police reports for pending claims.")
        ]

        idx = 1
        for category, res, rec_action in evaluations:
            if res.get("hazard_detected"):
                penalty = float(res.get("score_penalty", 0.0))
                total_penalty += penalty

                hazard_obj = InsuranceHazard(
                    hazard_id=f"INS_HAZ_{idx:03d}",
                    category=category,
                    title=res.get("title", "Insurance Risk Exposure"),
                    severity=res.get("severity", "LOW"),
                    description=res.get("desc", ""),
                    policy_ref="Commercial General Liability",
                    business_justification=f"Insurance risk exposure incurring {penalty} penalty points.",
                    evidence=f"Category '{category}' evaluated with severity '{res.get('severity')}'."
                )
                hazards.append(hazard_obj)

                finding_obj = InsuranceFinding(
                    category=category,
                    title=res.get("title", "Insurance Finding"),
                    description=res.get("desc", ""),
                    severity=res.get("severity", "LOW"),
                    policy_ref="Commercial General Liability",
                    evidence=f"Rule penalty: {penalty} pts",
                    suggested_action=rec_action,
                    priority="HIGH" if res.get("severity") in ["HIGH", "CRITICAL"] else "MEDIUM"
                )
                findings.append(finding_obj)
                idx += 1

        # 3. Insurance Risk Score Calculation (normalized 0.0 - 100.0 hazard scale)
        insurance_score = normalize_risk_score(10.0 + total_penalty)

        # 4. Insurance Profiles Generation
        proj_profile = ProjectInsuranceProfile(
            project_id=project_id,
            project_name=project_name,
            policy_coverage_rate=max(100.0 - (expired_policies * 30.0), 0.0),
            claim_readiness_rate=max(100.0 - (missing_claim_docs * 15.0), 0.0),
            asset_protection_rate=max(100.0 - (uninsured_assets * 20.0), 0.0),
            liability_exposure_index=float(third_party_claims * 25.0),
            insurance_score=insurance_score
        )

        asset_profiles: List[AssetInsuranceProfile] = [
            AssetInsuranceProfile(
                asset_id=str(e.get("id", f"AST_{i+1}")),
                asset_name=e.get("name", f"Asset {i+1}"),
                asset_category=e.get("category", "Heavy Machinery"),
                replacement_value=float(e.get("replacement_value", 50000.0)),
                coverage_status=e.get("insurance_status", "COVERED"),
                insurance_score=insurance_score
            )
            for i, e in enumerate(equipment_list[:5])
        ]

        # 5. Executive Metrics
        metrics = [
            InsuranceMetric(metric_name="Policy Coverage Rate", metric_value=proj_profile.policy_coverage_rate, category="COVERAGE", status=eval_policy.get("severity", "OPTIMAL"), description="Active policy coverage percentage"),
            InsuranceMetric(metric_name="Financial Incident Exposure", metric_value=total_financial_loss, category="LOSS", status=eval_incidents.get("severity", "OPTIMAL"), description="Total dollar exposure from logged site incidents"),
            InsuranceMetric(metric_name="Claim Package Readiness", metric_value=proj_profile.claim_readiness_rate, category="CLAIMS", status=eval_claims.get("severity", "OPTIMAL"), description="Completeness rate of claim documentation packages")
        ]

        return {
            "insurance_score": insurance_score,
            "hazards": [h.model_dump() for h in hazards],
            "findings": [f.model_dump() for f in findings],
            "project_insurance_profile": proj_profile.model_dump(),
            "asset_profiles": [ap.model_dump() for ap in asset_profiles],
            "metrics": [m.model_dump() for m in metrics],
            "total_hazards_count": len(hazards),
            "critical_hazards_count": sum(1 for h in hazards if h.severity == "CRITICAL"),
            "policies_evaluated_count": len(policies_list),
            "incidents_reviewed_count": len(incidents_list),
            "claims_reviewed_count": len(claims_list),
            "assets_evaluated_count": len(equipment_list)
        }

insurance_analyzer = InsuranceAnalyzer()
