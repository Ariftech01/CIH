from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from backend.risk_intelligence.integrations.base_adapter import BaseIntegrationAdapter
from backend.risk_intelligence.schemas.insurance_risk import InsuranceObservation

class InsuranceDataAdapter(BaseIntegrationAdapter):
    """
    Multi-Source Insurance Data Integration & Normalization Adapter.
    Normalizes incident logs, equipment/asset inventory, historical claims, policy details,
    uploaded insurance documents, and manual insurance observations into unified Business Context.
    Exposes readiness extension points for Insurance Provider APIs, Digital Claim Platforms,
    ERP Systems, Asset Tracking, Computer Vision, Weather APIs, Telematics, IoT, and Drone Inspections.
    """

    def __init__(self):
        super().__init__("Multi-Source Insurance Data Adapter")

    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        return {
            "source": self.name,
            "project_id": project_id,
            "provider_api_adapter_status": "READY",
            "digital_claims_status": "READY",
            "erp_integration_status": "READY",
            "weather_api_status": "READY",
            "computer_vision_damage_status": "READY",
            "status": "NORMALIZED"
        }

    def normalize_observations(self, raw_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes raw heterogeneous insurance and claim data into standardized internal Business Context.
        """
        normalized = dict(raw_context)
        normalized["source_adapter"] = self.name
        normalized["normalized_at"] = datetime.utcnow().isoformat()

        observations: List[InsuranceObservation] = []
        raw_obs_list = raw_context.get("insurance_observations", []) or raw_context.get("manual_insurance_observations", [])

        # Process string or dict observations
        for item in raw_obs_list:
            obs_id = f"OBS_INS_{uuid.uuid4().hex[:8]}"
            if isinstance(item, str):
                category = "PROPERTY_DAMAGE" if "damage" in item.lower() or "fire" in item.lower() else ("EQUIPMENT" if "equipment" in item.lower() or "crane" in item.lower() else "THIRD_PARTY_LIABILITY")
                severity = "HIGH" if "critical" in item.lower() or "severe" in item.lower() or "uninsured" in item.lower() else "MODERATE"
                obs = InsuranceObservation(
                    observation_id=obs_id,
                    source="MANUAL_INSURANCE_RECORD",
                    category=category,
                    severity=severity,
                    evidence=item
                )
                observations.append(obs)
            elif isinstance(item, dict):
                obs = InsuranceObservation(
                    observation_id=item.get("id", obs_id),
                    source=item.get("source", "INSURANCE_FORM"),
                    incident_id=item.get("incident_id"),
                    policy_ref=item.get("policy_ref"),
                    category=item.get("category", "PROPERTY_DAMAGE"),
                    severity=item.get("severity", "MODERATE"),
                    confidence=float(item.get("confidence", 1.0)),
                    evidence=item.get("evidence") or item.get("description"),
                    metadata=item.get("metadata", {})
                )
                observations.append(obs)

        # Parse incident records into observations
        incidents_list = raw_context.get("incidents_list", []) or raw_context.get("incidents", [])
        for inc in incidents_list:
            if isinstance(inc, dict):
                obs_id = f"OBS_INC_{uuid.uuid4().hex[:6]}"
                financial_impact = float(inc.get("financial_impact", 0.0))
                severity = "CRITICAL" if financial_impact > 50000.0 or inc.get("severity") in ["CRITICAL", "HIGH"] else "MODERATE"
                obs = InsuranceObservation(
                    observation_id=obs_id,
                    source="INCIDENT_LOG",
                    incident_id=inc.get("id") or inc.get("incident_id"),
                    category="PROPERTY_DAMAGE" if inc.get("type") == "DAMAGE" else "THIRD_PARTY_LIABILITY",
                    severity=severity,
                    evidence=f"Incident '{inc.get('id', 'INC_LOG')}': {inc.get('description', 'Site incident recorded')} (Financial Impact: ${financial_impact:,.2f})"
                )
                observations.append(obs)

        normalized["normalized_insurance_observations"] = [o.model_dump() for o in observations]
        normalized["observed_insurance_conditions_count"] = len(observations)
        return normalized

    # --- Extension Interfaces for Future Real-Time Provider & Financial Systems ---

    def process_insurance_provider_update(self, provider_payload: Dict[str, Any]) -> InsuranceObservation:
        """Extension point for Insurance Provider API policy status updates."""
        return InsuranceObservation(
            observation_id=f"PROV_{uuid.uuid4().hex[:8]}",
            source="PROVIDER_API",
            policy_ref=provider_payload.get("policy_number"),
            category="POLICY_COVERAGE",
            severity=provider_payload.get("severity", "HIGH"),
            confidence=1.0,
            evidence=f"Insurance Provider API update: Policy {provider_payload.get('policy_number')} status '{provider_payload.get('status')}'",
            metadata=provider_payload
        )

    def process_digital_claim_platform(self, claim_payload: Dict[str, Any]) -> InsuranceObservation:
        """Extension point for Digital Claim Platform updates."""
        return InsuranceObservation(
            observation_id=f"CLAIM_{uuid.uuid4().hex[:8]}",
            source="DIGITAL_CLAIM",
            incident_id=claim_payload.get("incident_id"),
            policy_ref=claim_payload.get("policy_ref"),
            category="CLAIM_DOCUMENTATION",
            severity=claim_payload.get("severity", "MODERATE"),
            confidence=1.0,
            evidence=f"Digital Claim Platform: Claim '{claim_payload.get('claim_id')}' status '{claim_payload.get('claim_status')}'",
            metadata=claim_payload
        )

    def process_weather_alert_exposure(self, weather_payload: Dict[str, Any]) -> InsuranceObservation:
        """Extension point for Weather API storm & flood exposure warnings."""
        return InsuranceObservation(
            observation_id=f"WX_{uuid.uuid4().hex[:8]}",
            source="WEATHER_API",
            category="PROPERTY_DAMAGE",
            severity=weather_payload.get("severity", "HIGH"),
            confidence=weather_payload.get("confidence", 0.95),
            evidence=f"Severe Weather Exposure Alert: {weather_payload.get('event_name')} in project location",
            metadata=weather_payload
        )

insurance_data_adapter = InsuranceDataAdapter()
