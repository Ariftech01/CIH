from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from backend.risk_intelligence.integrations.base_adapter import BaseIntegrationAdapter
from backend.risk_intelligence.schemas.safety_risk import SafetyObservation

class SafetyDataAdapter(BaseIntegrationAdapter):
    """
    Multi-Source Safety Data Integration & Normalization Adapter.
    Normalizes manual safety forms, user safety observations, worker records,
    and historical safety incidents into unified Business Context.
    Exposes readiness extension points for CCTV feeds, Computer Vision (YOLO/OpenCV),
    Wearable devices, Smart Helmets, BLE Tags, RFID, GPS, Digital Twins, and Emergency Alerts.
    """

    def __init__(self):
        super().__init__("Multi-Source Safety Data Adapter")

    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        return {
            "source": self.name,
            "project_id": project_id,
            "cv_adapter_status": "READY",
            "wearables_adapter_status": "READY",
            "ble_adapter_status": "READY",
            "rfid_adapter_status": "READY",
            "gps_adapter_status": "READY",
            "digital_twin_adapter_status": "READY",
            "emergency_alert_status": "READY",
            "status": "NORMALIZED"
        }

    def normalize_observations(self, raw_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes raw heterogeneous safety observations into standardized internal Business Context.
        """
        normalized = dict(raw_context)
        normalized["source_adapter"] = self.name
        normalized["normalized_at"] = datetime.utcnow().isoformat()

        observations: List[SafetyObservation] = []
        raw_obs_list = raw_context.get("safety_observations", [])
        if not raw_obs_list:
            raw_obs_list = raw_context.get("manual_observations", [])

        # Process string or dict observations
        for i, item in enumerate(raw_obs_list):
            obs_id = f"OBS_{uuid.uuid4().hex[:8]}"
            if isinstance(item, str):
                category = "PPE" if "ppe" in item.lower() or "helmet" in item.lower() or "vest" in item.lower() else "UNSAFE_BEHAVIOUR"
                severity = "HIGH" if "critical" in item.lower() or "danger" in item.lower() or "missing" in item.lower() else "MODERATE"
                obs = SafetyObservation(
                    observation_id=obs_id,
                    source="MANUAL_OBSERVATION",
                    category=category,
                    severity=severity,
                    evidence=item,
                    location=raw_context.get("work_zone", "General Site Zone")
                )
                observations.append(obs)
            elif isinstance(item, dict):
                obs = SafetyObservation(
                    observation_id=item.get("id", obs_id),
                    source=item.get("source", "MANUAL_FORM"),
                    worker_id=item.get("worker_id"),
                    location=item.get("location", "General Work Zone"),
                    category=item.get("category", "UNSAFE_BEHAVIOUR"),
                    severity=item.get("severity", "MODERATE"),
                    confidence=float(item.get("confidence", 1.0)),
                    evidence=item.get("evidence") or item.get("description"),
                    metadata=item.get("metadata", {})
                )
                observations.append(obs)

        # Parse safety inspection logs
        safety_records = raw_context.get("safety_records", []) or raw_context.get("safety_inspections", [])
        for record in safety_records:
            if isinstance(record, dict) and record.get("status") in ["FAIL", "HAZARD_DETECTED"]:
                obs_id = f"OBS_INSP_{uuid.uuid4().hex[:6]}"
                obs = SafetyObservation(
                    observation_id=obs_id,
                    source="INSPECTION_FORM",
                    location=record.get("location", "Inspection Zone"),
                    category=record.get("category", "PPE"),
                    severity=record.get("severity", "HIGH"),
                    evidence=record.get("issue") or record.get("notes") or "Safety inspection violation detected",
                )
                observations.append(obs)

        normalized["normalized_safety_observations"] = [o.model_dump() for o in observations]
        normalized["observed_safety_conditions_count"] = len(observations)
        return normalized

    # --- Extension Interfaces for Future Real-Time Hardware & AI Technologies ---

    def process_computer_vision_detection(self, cv_payload: Dict[str, Any]) -> SafetyObservation:
        """Extension point for YOLO/OpenCV detections."""
        return SafetyObservation(
            observation_id=f"CV_{uuid.uuid4().hex[:8]}",
            source="COMPUTER_VISION",
            worker_id=cv_payload.get("worker_id"),
            location=cv_payload.get("zone", "Camera Feed Zone"),
            category=cv_payload.get("detection_category", "PPE"),
            severity=cv_payload.get("severity", "HIGH"),
            confidence=cv_payload.get("confidence", 0.95),
            evidence=cv_payload.get("bounding_box_label", "CV Violation Detected"),
            metadata=cv_payload
        )

    def process_wearable_alert(self, wearable_payload: Dict[str, Any]) -> SafetyObservation:
        """Extension point for Smart Helmet / Wearable alerts."""
        return SafetyObservation(
            observation_id=f"WEAR_{uuid.uuid4().hex[:8]}",
            source="WEARABLE",
            worker_id=wearable_payload.get("worker_id"),
            location=wearable_payload.get("gps_coords", "Wearable Zone"),
            category=wearable_payload.get("alert_type", "HAZARD_EXPOSURE"),
            severity=wearable_payload.get("severity", "HIGH"),
            confidence=1.0,
            evidence=f"Wearable alert triggered: {wearable_payload.get('event_type', 'Fall/Impact')}",
            metadata=wearable_payload
        )

    def process_ble_tag_location(self, ble_payload: Dict[str, Any]) -> SafetyObservation:
        """Extension point for BLE Safety Tags & Restricted Area access."""
        return SafetyObservation(
            observation_id=f"BLE_{uuid.uuid4().hex[:8]}",
            source="BLE",
            worker_id=ble_payload.get("worker_id"),
            location=ble_payload.get("restricted_zone", "Restricted Area"),
            category="RESTRICTED_AREA",
            severity=ble_payload.get("severity", "CRITICAL"),
            confidence=1.0,
            evidence=f"BLE Tag detected worker in unauthorized zone {ble_payload.get('zone_id')}",
            metadata=ble_payload
        )

safety_data_adapter = SafetyDataAdapter()
