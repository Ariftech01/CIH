"""Intent Router & Entity Identifier Extractor for CIH AI Subsystem."""

import re
from typing import Dict, Any, List, Optional
from services.ollamaService import is_construction_domain, DEFAULT_REFUSAL_TEXT

# Regex Patterns for Construction Intelligence Entity Identifiers
ENTITY_PATTERNS = {
    "project": re.compile(r"\b(PRJ-[A-Za-z0-9_-]+)\b", re.IGNORECASE),
    "risk": re.compile(r"\b(RISK-[A-Za-z0-9_-]+)\b", re.IGNORECASE),
    "worker": re.compile(r"\b((?:WRK|WKR|EMP)-[A-Za-z0-9_-]+)\b", re.IGNORECASE),
    "equipment": re.compile(r"\b((?:EQP|EQ)-[A-Za-z0-9_-]+)\b", re.IGNORECASE),
    "document": re.compile(r"\b(DOC-[A-Za-z0-9_-]+)\b", re.IGNORECASE),
}


class IntentRouter:
    """Classifies user query intent, extracts entity IDs, and applies domain guardrails."""

    def extract_entity_ids(self, prompt: str) -> Dict[str, List[str]]:
        """Extract all construction entity identifiers from query string."""
        entities: Dict[str, List[str]] = {
            "project": [],
            "risk": [],
            "worker": [],
            "equipment": [],
            "document": []
        }
        if not prompt:
            return entities

        for entity_type, pattern in ENTITY_PATTERNS.items():
            matches = pattern.findall(prompt)
            if matches:
                # Deduplicate matching codes upper-cased
                unique_codes = sorted(list(set(m.upper() for m in matches)))
                entities[entity_type] = unique_codes

        # If no explicit project code in prompt, fallback to current active project context
        if not entities["project"]:
            try:
                import streamlit as st
                from backend.cache.cache_manager import cache_manager
                active_code = st.session_state.get("active_project_code") or cache_manager.get("cih_active_project_code")
                if active_code:
                    entities["project"] = [active_code]
            except Exception:
                pass

        return entities

    def route_intent(self, prompt: str) -> Dict[str, Any]:
        """Classify prompt intent, extract identifiers, and enforce domain guardrails.

        Returns:
            Dict containing:
                is_valid (bool): Whether query passes domain guardrail.
                intent (str): ENTITY_LOOKUP | SAFETY_AUDIT | COST_ESTIMATE | GENERAL_CONSTRUCTION | OUT_OF_DOMAIN
                extracted_entities (Dict[str, List[str]])
                refusal_response (Optional[str])
        """
        extracted = self.extract_entity_ids(prompt)
        has_entities = any(len(codes) > 0 for codes in extracted.values())

        # Entity IDs (e.g. PRJ-0A752A) are automatically valid construction domain queries
        if not has_entities and not is_construction_domain(prompt):
            return {
                "is_valid": False,
                "intent": "OUT_OF_DOMAIN",
                "extracted_entities": extracted,
                "refusal_response": DEFAULT_REFUSAL_TEXT
            }

        prompt_lower = prompt.lower() if prompt else ""

        if has_entities:
            intent = "ENTITY_LOOKUP"
        elif any(k in prompt_lower for k in ["safety", "ppe", "hazard", "risk", "osha", "inspection"]):
            intent = "SAFETY_AUDIT"
        elif any(k in prompt_lower for k in ["cost", "budget", "boq", "estimate", "pricing", "rate"]):
            intent = "COST_ESTIMATE"
        else:
            intent = "GENERAL_CONSTRUCTION"

        return {
            "is_valid": True,
            "intent": intent,
            "extracted_entities": extracted,
            "refusal_response": None
        }


intent_router = IntentRouter()
