"""Token-optimized Prompt Builder for CIH AI Enterprise Pipeline."""

from typing import Dict, Any, List, Optional
from services.ollamaService import MASTER_CONSTRUCTION_SYSTEM_PROMPT, get_module_context
from backend.ai_engine.context_engine import project_context_engine


class EnterprisePromptBuilder:
    """Assembles pruned, high-relevance system prompts and context blocks."""

    def build_system_prompt(
        self,
        module_name: Optional[str] = None,
        extracted_entities: Optional[Dict[str, List[str]]] = None,
        document_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Construct compact, high-quality system prompt.

        Returns:
            Formatted system prompt string.
        """
        parts: List[str] = [MASTER_CONSTRUCTION_SYSTEM_PROMPT.strip()]

        # 1. Inject Active Module Context (if specified)
        if module_name:
            mod_ctx = get_module_context(module_name)
            if mod_ctx:
                parts.append(f"\n\n=== ACTIVE MODULE OPERATIONAL CONTEXT ===\n{mod_ctx.strip()}")

        # 2. Inject Retrieved Live Database Entity Context (if entities extracted)
        if extracted_entities and any(extracted_entities.values()):
            db_ctx = project_context_engine.retrieve_entity_context(extracted_entities)
            if db_ctx:
                parts.append(f"\n\n=== RETRIEVED ENTERPRISE DATABASE CONTEXT ===\n{db_ctx.strip()}")

        # 3. Inject Active Document Context (if present)
        if document_context:
            doc_name = document_context.get("name", "Document")
            doc_text = document_context.get("text", "")[:4000]
            parts.append(f"\n\n=== ACTIVE UPLOADED DOCUMENT ({doc_name}) ===\n{doc_text.strip()}")

        parts.append("\n\nEnsure engineering precision, professional structure, and construction domain best practices.")

        return "".join(parts)


prompt_builder = EnterprisePromptBuilder()
