from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from backend.risk_intelligence.integrations.base_adapter import BaseIntegrationAdapter
from backend.risk_intelligence.schemas.compliance_risk import ComplianceObservation

class ComplianceDataAdapter(BaseIntegrationAdapter):
    """
    Multi-Source Compliance Data Integration & Normalization Adapter.
    Normalizes permit records, inspection logs, certification records, audit histories,
    uploaded regulatory documents, and manual compliance observations into unified Business Context.
    Exposes readiness extension points for Government Regulatory APIs, Municipal Building Authorities,
    Digital Inspection Platforms, Document OCR, Electronic Signatures, BIM, and Digital Twins.
    """

    def __init__(self):
        super().__init__("Multi-Source Compliance Data Adapter")

    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        return {
            "source": self.name,
            "project_id": project_id,
            "govt_api_adapter_status": "READY",
            "municipal_authority_status": "READY",
            "digital_inspection_status": "READY",
            "ocr_document_ai_status": "READY",
            "bim_digital_twin_status": "READY",
            "status": "NORMALIZED"
        }

    def normalize_observations(self, raw_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes raw heterogeneous regulatory compliance data into standardized internal Business Context.
        """
        normalized = dict(raw_context)
        normalized["source_adapter"] = self.name
        normalized["normalized_at"] = datetime.utcnow().isoformat()

        observations: List[ComplianceObservation] = []
        raw_obs_list = raw_context.get("compliance_observations", []) or raw_context.get("manual_compliance_observations", [])

        # Process string or dict observations
        for item in raw_obs_list:
            obs_id = f"OBS_CMP_{uuid.uuid4().hex[:8]}"
            if isinstance(item, str):
                category = "PERMIT" if "permit" in item.lower() else ("INSPECTION" if "inspection" in item.lower() else "DOCUMENTATION")
                severity = "MAJOR" if "expired" in item.lower() or "violation" in item.lower() or "missing" in item.lower() else "MODERATE"
                obs = ComplianceObservation(
                    observation_id=obs_id,
                    source="MANUAL_COMPLIANCE_RECORD",
                    category=category,
                    severity=severity,
                    evidence=item
                )
                observations.append(obs)
            elif isinstance(item, dict):
                obs = ComplianceObservation(
                    observation_id=item.get("id", obs_id),
                    source=item.get("source", "COMPLIANCE_FORM"),
                    permit_id=item.get("permit_id"),
                    category=item.get("category", "PERMIT"),
                    severity=item.get("severity", "MODERATE"),
                    confidence=float(item.get("confidence", 1.0)),
                    evidence=item.get("evidence") or item.get("description"),
                    metadata=item.get("metadata", {})
                )
                observations.append(obs)

        # Parse permit records if provided
        permit_records = raw_context.get("permit_records", []) or raw_context.get("permits", [])
        for permit in permit_records:
            if isinstance(permit, dict) and permit.get("status") in ["EXPIRED", "RENEWAL_DUE", "REVOKED"]:
                obs_id = f"OBS_PERM_{uuid.uuid4().hex[:6]}"
                obs = ComplianceObservation(
                    observation_id=obs_id,
                    source="PERMIT_SYSTEM",
                    permit_id=permit.get("id") or permit.get("permit_number"),
                    category="PERMIT",
                    severity="CRITICAL" if permit.get("status") in ["EXPIRED", "REVOKED"] else "MAJOR",
                    evidence=f"Permit '{permit.get('name', 'Building Permit')}' status: {permit.get('status')}"
                )
                observations.append(obs)

        # Parse inspection records if provided
        inspection_records = raw_context.get("inspection_records", []) or raw_context.get("inspections", [])
        for insp in inspection_records:
            if isinstance(insp, dict) and insp.get("status") in ["FAILED", "OVERDUE", "DEFICIENCY"]:
                obs_id = f"OBS_INSP_{uuid.uuid4().hex[:6]}"
                obs = ComplianceObservation(
                    observation_id=obs_id,
                    source="INSPECTION_FORM",
                    category="INSPECTION",
                    severity="MAJOR" if insp.get("status") == "FAILED" else "MODERATE",
                    evidence=f"Inspection '{insp.get('type', 'Mandatory Inspection')}' status: {insp.get('status')}"
                )
                observations.append(obs)

        normalized["normalized_compliance_observations"] = [o.model_dump() for o in observations]
        normalized["observed_compliance_conditions_count"] = len(observations)
        return normalized

    # --- Extension Interfaces for Future Real-Time Hardware, OCR & Government Systems ---

    def process_government_api_update(self, api_payload: Dict[str, Any]) -> ComplianceObservation:
        """Extension point for Municipal Building Authority & Government API integration."""
        return ComplianceObservation(
            observation_id=f"GOVT_{uuid.uuid4().hex[:8]}",
            source="GOVT_API",
            permit_id=api_payload.get("permit_id"),
            category="PERMIT",
            severity=api_payload.get("severity", "MAJOR"),
            confidence=1.0,
            evidence=f"Government API Regulatory Status Update: {api_payload.get('regulatory_status')}",
            metadata=api_payload
        )

    def process_ocr_document_verification(self, ocr_payload: Dict[str, Any]) -> ComplianceObservation:
        """Extension point for Document AI & OCR regulatory document extraction."""
        return ComplianceObservation(
            observation_id=f"OCR_{uuid.uuid4().hex[:8]}",
            source="OCR_DOC",
            category="DOCUMENTATION",
            severity=ocr_payload.get("severity", "MODERATE"),
            confidence=ocr_payload.get("ocr_confidence", 0.92),
            evidence=f"Document OCR analysis: {ocr_payload.get('document_type')} missing required stamp/signature",
            metadata=ocr_payload
        )

    def process_digital_inspection_platform(self, platform_payload: Dict[str, Any]) -> ComplianceObservation:
        """Extension point for Digital Inspection Platforms."""
        return ComplianceObservation(
            observation_id=f"DIG_INSP_{uuid.uuid4().hex[:8]}",
            source="DIGITAL_INSPECTION_PLATFORM",
            category="INSPECTION",
            severity=platform_payload.get("severity", "MAJOR"),
            confidence=1.0,
            evidence=f"Digital Inspection Log: {platform_payload.get('inspection_item')} failed validation",
            metadata=platform_payload
        )

compliance_data_adapter = ComplianceDataAdapter()
