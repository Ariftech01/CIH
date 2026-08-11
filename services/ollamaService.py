"""Ollama Service Layer for Construction Intelligence Hub (CIH).

Provides a domain-validated, enterprise-grade AI integration with local Ollama,
featuring lightweight pre-flight domain filtering, hidden master system prompts,
module context injection, structured responses, and fallback UI redirection cards.
"""

import json
import re
import time
import urllib.request
import urllib.error
from typing import Any, Dict, Generator, List, Optional
import streamlit as st

# Global default configuration
OLLAMA_HOST = "http://127.0.0.1:11434"
DEFAULT_MODEL = "llama3.2"
TIMEOUT = 120.0  # 120 seconds timeout for local inference queries
MAX_RETRIES = 3  # Maximum automatic retries for transient timeouts/failures

# ───────────────────────────────────────────────────────────────────────────
# CONSTANTS & DOMAIN TAXONOMY
# ───────────────────────────────────────────────────────────────────────────

MASTER_CONSTRUCTION_SYSTEM_PROMPT = """You are Construction Intelligence Hub AI.

You are an experienced Civil Engineer, Construction Project Manager, Quantity Surveyor, Site Engineer, Cost Consultant, Safety Officer, Equipment Specialist, and Construction Planning Expert.

Your purpose is to assist construction professionals.

Always provide professional, structured, technically accurate responses formatted like engineering reports.

When calculations are approximate, clearly state your assumptions.

Never invent project-specific data.

If sufficient information is unavailable, ask follow-up questions.

Prefer construction standards and engineering best practices.

Respond using headings, bullet lists, tables, and professional markdown formatting whenever appropriate.

Structure your response using the following headers where applicable:
### 📌 Executive Summary
### 🏗️ Detailed Engineering Explanation
### 🎯 Recommendations
### ⚙️ Engineering Best Practices
### ❓ Suggested Follow-up Questions
"""

DEFAULT_REFUSAL_TEXT = (
    "Construction Intelligence Hub AI\n\n"
    "Thank you for your question.\n\n"
    "I am a domain-specific AI assistant developed exclusively for the Construction Intelligence Hub platform.\n\n"
    "My expertise is focused on:\n\n"
    "• Construction Engineering\n"
    "• Civil Engineering\n"
    "• Project Planning\n"
    "• Cost Estimation\n"
    "• Safety Monitoring\n"
    "• Material Management\n"
    "• Equipment Tracking\n"
    "• Workforce Management\n"
    "• Construction Documentation\n"
    "• Infrastructure Projects\n\n"
    "The question you asked appears to be outside the scope of this application.\n\n"
    "Please ask questions related to construction engineering or project management.\n\n"
    "Here are some examples:\n\n"
    "• Estimate the cost of a residential building.\n"
    "• Generate a Bill of Quantities.\n"
    "• Suggest construction materials.\n"
    "• Explain reinforced concrete.\n"
    "• Recommend excavation equipment.\n"
    "• Generate a construction safety checklist.\n"
    "• Analyze a construction report."
)

CONSTRUCTION_KEYWORDS = [
    # General & Civil Engineering
    "construction", "civil", "build", "building", "structure", "structural", "architecture", "architect",
    "site", "contractor", "subcontractor", "engineer", "engineering", "infrastructure", "project",
    "rcc", "reinforced concrete", "reinforced cement concrete", "curing", "waterproofing",
    "stadium", "bridge", "bridges", "bim", "building information modeling", "autocad", "cad",
    "earthquake-resistant", "earthquake resistant", "green building", "green buildings", "leed",
    # Materials
    "concrete", "cement", "steel", "rebar", "tmt", "brick", "mortar", "sand", "aggregate", "asphalt",
    "bitumen", "wood", "timber", "glass", "tile", "tiles", "paint", "roofing", "shuttering", "formwork",
    "plaster", "insulation", "façade", "facade", "cladding", "material", "inventory",
    # Scope & Tasks
    "foundation", "piling", "footing", "excavation", "trench", "slab", "beam", "column", "wall", "masonry",
    "scaffolding", "shoring", "curtain wall", "mep", "hvac", "plumbing", "electrical", "wiring", "conduit",
    "drainage", "flooring", "compaction", "slump", "survey", "geotechnical", "soil", "grading",
    # Cost & Estimation
    "boq", "bill of quantities", "estimate", "estimation", "cost", "budget", "rate", "unit rate", "price",
    "procurement", "purchase", "vendor", "supplier", "tender", "bid", "bidding", "quantity surveyor",
    "takeoff", "contingency", "financial", "ledger",
    # Safety & Compliance
    "safety", "hazard", "risk", "ppe", "helmet", "harness", "osha", "is 456", "is 1893", "nbc", "code",
    "standard", "inspection", "audit", "permit", "compliance", "incident", "accident",
    # Workforce & Management
    "labor", "labour", "worker", "workers", "crew", "masons", "welder", "rigger", "foreman", "supervisor",
    "workforce", "manpower", "attendance", "shift", "productivity",
    # Equipment & Machinery
    "equipment", "machinery", "fleet", "crane", "excavator", "bulldozer", "loader", "dumper", "truck",
    "batching plant", "mixer", "generator", "compactor", "tanker", "maintenance", "idle", "uptime",
    # Schedule & Progress
    "schedule", "scheduling", "gantt", "milestone", "delay", "timeline", "duration", "critical path",
    "cpm", "pert", "wbs", "progress", "completion", "weekly report", "daily report", "site report", "logistics"
]

NON_CONSTRUCTION_KEYWORDS = [
    # Sports & Celebrities
    "virat", "kohli", "ms dhoni", "dhoni", "cricket score", "ipl", "football match", "soccer match", "messi", "ronaldo",
    "sports score", "nfl score", "nba score", "fifa world cup", "world cup winner",
    # Entertainment, Movies & Media
    "movie", "movies", "film", "films", "actor", "actress", "cinema", "hollywood", "bollywood",
    "netflix", "song", "music", "album", "gaming", "game", "playstation", "xbox", "joke", "jokes",
    # Politics & Current Events
    "prime minister", "president", "election", "politics", "political", "modi", "biden", "trump",
    "parliament", "war news", "political news", "today's political news",
    # General Programming & Unrelated Tech
    "python code", "write python", "programming question", "programming questions", "how to code",
    "javascript array", "html button", "react hook", "java spring", "c++ pointers", "code snake",
    # Crypto & Finance Market
    "bitcoin", "crypto", "ethereum", "dogecoin", "stock market", "nifty", "sensex", "share price",
    # Lifestyle, Travel, Food, Medical & Consumer Tech
    "recipe", "cooking", "restaurant", "hotel", "travel", "vacation", "flight", "shopping", "fashion",
    "disease", "symptom", "medicine", "doctor", "general medical advice", "medical advice",
    "microsoft", "founded microsoft", "who founded microsoft", "what is chatgpt", "chatgpt",
    "what is artificial intelligence", "artificial intelligence", "best mobile phone", "mobile phone"
]

MODULE_CONTEXT_INSTRUCTIONS = {
    "dashboard": "You are assisting with executive construction dashboard analysis.",
    "constructionriskintelligence": "You are acting as an Enterprise Construction Risk Intelligence Specialist. Focus on multi-agent risk assessment, site hazard evaluation, workforce safety, regulatory compliance, insurance exposure, executive report composition, and automated site risk mitigation.",
    "projectmanagement": "You are assisting with construction project management.",
    "costestimation": "You are acting as a Senior Construction Cost Consultant. Focus on cost estimation, budget optimization, rate analysis, BOQ structure, financial contingency, and cost reduction strategies.",
    "materialmanagement": "You are acting as a Senior Construction Material Engineer. Focus on material specifications, inventory control, concrete/steel testing, quality compliance, logistics, and wastage reduction.",
    "workermanagement": "You are acting as a Senior Workforce Planner. Focus on labor productivity, crew allocation ratios, skill trade scheduling, site attendance, wages, and worker welfare.",
    "safetymonitoring": "You are acting as a Senior Construction Safety Officer. Focus on site safety protocols, OSHA compliance, IS 456 / IS 1893 hazard mitigation, PPE enforcement, and incident prevention.",
    "equipmenttracking": "You are acting as a Heavy Equipment Specialist. Focus on construction machinery fleet utilization, crane operations, excavation equipment, fuel efficiency, and preventive maintenance.",
    "progressmonitoring": "You are assisting with progress monitoring and schedule milestone tracking.",
    "reports": "You are assisting with construction executive report generation.",
    "aianalysis": "You are assisting with construction document intelligence and predictive modeling."
}


PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "pretend you are",
    "forget construction mode",
    "act as a general assistant",
    "you are no longer restricted",
    "act as an unrestricted",
    "dan mode",
    "jailbreak"
]

# ───────────────────────────────────────────────────────────────────────────
# DOMAIN VALIDATION & UI HELPERS
# ───────────────────────────────────────────────────────────────────────────

def is_construction_domain(prompt: str) -> bool:
    """Pre-flight validation to check if prompt belongs to the construction domain.

    Returns:
        bool: True if construction-related or general greeting; False if non-construction topic.
    """
    if not prompt or not prompt.strip():
        return False

    prompt_lower = prompt.lower().strip()

    # 1. Block adversarial prompt injection attempts unless accompanied by valid construction query
    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern in prompt_lower:
            # Check if there is an actual construction question embedded
            construction_overrides = ["concrete", "cement", "boq", "steel", "foundation", "scaffolding", "excavation", "rcc", "bridge", "stadium foundation"]
            if not any(co in prompt_lower for co in construction_overrides):
                return False
            return False  # Strict security: deny prompt injection attempts unconditionally

    # 2. Greetings & System intros are welcome
    greetings = ["hi", "hello", "hey", "who are you", "what can you do", "help", "good morning", "good evening", "greetings"]
    if any(prompt_lower == g or prompt_lower.startswith(g + " ") for g in greetings):
        return True

    # 3. Construction Entity Identifier codes (e.g. PRJ-0A752A, PRJ-2026-001, RISK-101, WRK-501)
    if re.search(r"\b(?:PRJ|RISK|WRK|WKR|EMP|EQP|EQ|DOC)-[A-Za-z0-9_-]+\b", prompt, re.IGNORECASE):
        return True

    # 3. Explicit strong positive construction indicators (overrides weak generic non-construction words like 'cricket' in 'cricket stadium')
    strong_positive = [
        "construction", "civil", "structure", "structural", "architecture", "architect",
        "contractor", "subcontractor", "boq", "bill of quantities", "concrete", "cement", "steel", "rebar",
        "tmt", "mason", "masonry", "slab", "beam", "column", "foundation", "piling", "footing",
        "excavation", "trench", "scaffolding", "shoring", "mep", "hvac", "plumbing", "shuttering",
        "formwork", "plaster", "waterproofing", "is 456", "is 1893", "nbc", "osha", "takeoff",
        "batching plant", "tower crane", "excavator", "bulldozer", "gantt", "critical path", "cpm",
        "rcc", "reinforced concrete", "curing", "stadium foundation", "stadium design", "build a cricket stadium",
        "build a stadium", "construct a bridge", "bridge", "bridges", "earthquake-resistant", "earthquake resistant",
        "green building", "green buildings", "bim", "autocad", "cad", "site inspection", "cost estimation",
        "labor productivity", "labour productivity", "construction delay", "construction delays",
        "budget optimization", "construction risk", "recommend machinery"
    ]
    has_strong_positive = any(sp in prompt_lower for sp in strong_positive)

    # 4. Check negative non-construction indicators
    has_negative = any(nk in prompt_lower for nk in NON_CONSTRUCTION_KEYWORDS)

    if has_negative and not has_strong_positive:
        return False

    if has_strong_positive:
        return True

    # 5. Check positive construction indicators
    has_positive = any(ck in prompt_lower for ck in CONSTRUCTION_KEYWORDS)
    if has_positive:
        return True

    return False


def render_domain_refusal_card(user_prompt: str = "") -> None:
    """Render a clean, professional Glass UI card for non-construction redirects."""
    st.markdown(
        """
        <div class="cih-glass-card" style="border: 1px solid rgba(59, 130, 246, 0.3); border-left: 4px solid #3B82F6; padding: 1.25rem; margin-bottom: 1rem;">
            <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem;">
                <span style="font-size:1.8rem;">🏗️</span>
                <div>
                    <div style="font-weight:700; font-size:1.05rem; color:var(--text-primary);">Construction Intelligence Hub AI</div>
                    <div style="font-size:0.78rem; color:var(--text-muted);">CIH Domain-Specific Engineering Assistant</div>
                </div>
            </div>
            <div style="font-size:0.9rem; color:var(--text-secondary); line-height:1.6; margin-bottom:1rem;">
                Thank you for your question.<br><br>
                I am a domain-specific AI assistant developed exclusively for the Construction Intelligence Hub platform.<br><br>
                <strong>My expertise is focused on:</strong>
                <ul style="margin: 0.5rem 0 0.75rem 1.2rem; padding: 0;">
                    <li>Construction Engineering</li>
                    <li>Civil Engineering</li>
                    <li>Project Planning</li>
                    <li>Cost Estimation</li>
                    <li>Safety Monitoring</li>
                    <li>Material Management</li>
                    <li>Equipment Tracking</li>
                    <li>Workforce Management</li>
                    <li>Construction Documentation</li>
                    <li>Infrastructure Projects</li>
                </ul>
                The question you asked appears to be outside the scope of this application. Please ask questions related to construction engineering or project management.
            </div>
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); padding:0.85rem; border-radius:10px;">
                <div style="font-weight:600; font-size:0.82rem; color:var(--text-primary); margin-bottom:0.5rem;">💡 Suggested Construction Examples:</div>
                <div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.6;">
                    • Estimate the cost of a residential building.<br>
                    • Generate a Bill of Quantities.<br>
                    • Suggest construction materials.<br>
                    • Explain reinforced concrete.<br>
                    • Recommend excavation equipment.<br>
                    • Generate a construction safety checklist.<br>
                    • Analyze a construction report.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



def get_suggested_followup_questions(topic: str = "general") -> List[str]:
    """Return 4-6 domain relevant follow-up construction questions."""
    topic_lower = topic.lower()
    if "cost" in topic_lower or "budget" in topic_lower or "price" in topic_lower or "estimate" in topic_lower:
        return [
            "Estimate labour costs for a 3000 sq.ft structure",
            "Generate detailed BOQ breakdown table",
            "Calculate cement and steel quantity ratio",
            "Suggest cost optimization techniques for raw materials",
            "Analyze budget contingency reserves allocation"
        ]
    elif "safety" in topic_lower or "risk" in topic_lower or "hazard" in topic_lower:
        return [
            "List PPE requirements for high-rise scaffolding",
            "Generate daily site safety audit checklist",
            "What are monsoon excavation shoring protocols?",
            "Explain IS 456 & OSHA site compliance rules",
            "Recommend emergency hazard response workflows"
        ]
    elif "material" in topic_lower or "concrete" in topic_lower or "steel" in topic_lower:
        return [
            "Calculate concrete mix proportions for M30 grade",
            "Estimate Fe-550 TMT steel rebar wastage factor",
            "Suggest alternative eco-friendly building materials",
            "How to test concrete slump & compressive strength?",
            "Optimize raw material lead time logistics"
        ]
    elif "worker" in topic_lower or "labor" in topic_lower or "workforce" in topic_lower:
        return [
            "Suggest mason-to-helper staffing ratio for brickwork",
            "Calculate daily workforce productivity rate",
            "How to manage labor overtime budget caps?",
            "Generate site worker attendance report template",
            "Recommend skilled crew allocations per floor"
        ]
    elif "equipment" in topic_lower or "machinery" in topic_lower or "crane" in topic_lower:
        return [
            "Recommend equipment fleet for 5-acre excavation",
            "Calculate tower crane operating cost per hour",
            "How to minimize heavy machinery idle downtime?",
            "Generate preventive maintenance schedule for excavators",
            "Fuel consumption optimization for dump trucks"
        ]
    elif "schedule" in topic_lower or "delay" in topic_lower or "gantt" in topic_lower:
        return [
            "Suggest fast-tracking options for superstructure slab",
            "How to mitigate supply chain material delays?",
            "Generate Critical Path Method (CPM) milestone schedule",
            "Calculate project Schedule Variance (SV) and SPI",
            "Optimize slab curing time without losing strength"
        ]
    else:
        return [
            "Estimate the cost of a 2500 sq ft residential building",
            "Suggest construction materials for a commercial complex",
            "Generate a Bill of Quantities (BOQ)",
            "Explain IS 456 construction safety standards",
            "Recommend equipment for foundation excavation"
        ]


def _cached_ollama_health_check(host: str, model_name: str) -> Dict[str, Any]:
    """Perform a complete diagnostic of the local Ollama integration (cached for 15 seconds)."""
    from backend.cache.cache_manager import cache_manager
    cache_key = f"ollama_health_{host}_{model_name}"
    cached_status = cache_manager.get(cache_key)
    if cached_status is not None:
        return cached_status

    status = {
        "installed": False,
        "running": False,
        "model_available": False,
        "reachable": False,
        "latency_ms": 0.0,
        "model_name": model_name,
        "memory_usage": "Unknown",
        "status_text": "Disconnected",
        "error_details": ""
    }

    start_time = time.time()
    url = f"{host}/api/tags"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=0.5) as response:
            if response.status == 200:
                status["installed"] = True
                status["running"] = True
                status["reachable"] = True
                status["status_text"] = "Connected"

                data = json.loads(response.read().decode("utf-8"))
                models = data.get("models", [])

                target_model = model_name.lower()
                found = False
                for m in models:
                    m_name = m.get("name", "").lower()
                    if target_model in m_name or m_name in target_model:
                        found = True
                        status["model_available"] = True
                        size_bytes = m.get("size", 0)
                        if size_bytes > 0:
                            status["memory_usage"] = f"{size_bytes / (1024**3):.2f} GB"
                        break

                if not found:
                    status["error_details"] = f"Model '{model_name}' not found. Run 'ollama pull {model_name}'"
                    status["status_text"] = "Model Missing"

                latency = (time.time() - start_time) * 1000
                status["latency_ms"] = round(latency, 2)

    except urllib.error.URLError as e:
        status["installed"] = True
        status["running"] = False
        status["reachable"] = False
        status["status_text"] = "Service Offline"
        status["error_details"] = f"Ollama daemon not running. Details: {e.reason}"
    except Exception as e:
        status["installed"] = False
        status["running"] = False
        status["reachable"] = False
        status["status_text"] = "Offline"
        status["error_details"] = str(e)

    cache_manager.set(cache_key, status, ttl_seconds=60)
    return status


class OllamaService:
    """Service class encapsulating domain-validated Ollama LLM capabilities."""

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self.host = OLLAMA_HOST

    def initialize(self, model_name: str = DEFAULT_MODEL) -> None:
        """Initialize or change the active model name."""
        self.model_name = model_name

    def health_check(self) -> Dict[str, Any]:
        """Perform a complete diagnostic of the local Ollama integration (cached for 15s)."""
        return _cached_ollama_health_check(self.host, self.model_name)


    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None, model_override: Optional[str] = None) -> str:
        """Send a list of messages to Ollama after domain validation."""
        # 1. Pre-flight Domain Validation
        last_user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "")
                break

        if last_user_msg and not is_construction_domain(last_user_msg):
            return DEFAULT_REFUSAL_TEXT

        url = f"{self.host}/api/chat"
        model = model_override or self.model_name

        # 2. Master System Prompt
        sys_prompt = system_prompt or MASTER_CONSTRUCTION_SYSTEM_PROMPT

        formatted_messages = [{"role": "system", "content": sys_prompt}]
        formatted_messages.extend(messages)

        data = {
            "model": model,
            "messages": formatted_messages,
            "stream": False,
            "options": {"temperature": 0.3}
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                    res = json.loads(response.read().decode("utf-8"))
                    return res["message"]["content"].strip()
            except Exception as e:
                if attempt == MAX_RETRIES:
                    raise RuntimeError(f"Chat request failed after {MAX_RETRIES} attempts: {str(e)}")
                time.sleep(1.0 * attempt)

    def prediction(self, prediction_type: str, context: str, model_override: Optional[str] = None) -> Dict[str, Any]:
        """Request a structured json forecast from Ollama with auto-retry."""
        url = f"{self.host}/api/generate"
        model = model_override or self.model_name

        system_prompts = {
            "safety": "You are a Construction Safety AI Officer. Analyze the project safety data. Respond ONLY in valid JSON format.",
            "cost": "You are a Construction Cost & Procurement Optimization AI. Analyze the project budget data. Respond ONLY in valid JSON format.",
            "timeline": "You are a Construction Schedule Planner and Supply Chain Analyst. Respond ONLY in valid JSON format."
        }

        system_prompt = system_prompts.get(prediction_type, "You are a Construction Analysis AI. Respond ONLY in valid JSON.")

        data = {
            "model": model,
            "prompt": context,
            "system": system_prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.1}
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                    res = json.loads(response.read().decode("utf-8"))
                    response_text = res.get("response", "").strip()
                    return self._clean_json(response_text)
            except Exception as e:
                if attempt == MAX_RETRIES:
                    raise RuntimeError(f"Prediction failed after {MAX_RETRIES} attempts: {str(e)}")
                time.sleep(1.0 * attempt)

    def insights(self, user_msg: str, chat_history: List[Dict[str, str]], context: str, model_override: Optional[str] = None) -> str:
        """Conversational analysis interface with domain validation and hidden context."""
        # 1. Pre-flight Domain Validation
        if not is_construction_domain(user_msg):
            return DEFAULT_REFUSAL_TEXT

        model = model_override or self.model_name

        system_prompt = (
            f"{MASTER_CONSTRUCTION_SYSTEM_PROMPT}\n\n"
            f"=== OPERATIONAL ACTIVE CONTEXT ===\n{context}\n========================"
        )

        history_msgs = []
        for msg in chat_history[-6:]:
            role = "assistant" if msg["role"] == "assistant" else "user"
            history_msgs.append({"role": role, "content": msg["content"]})

        messages = [{"role": "user", "content": user_msg}]

        return self.chat(history_msgs + messages, system_prompt=system_prompt, model_override=model)

    def stream_response(self, prompt: str, system_prompt: Optional[str] = None, chat_history: Optional[List[Dict[str, str]]] = None, model_override: Optional[str] = None) -> Generator[str, None, None]:
        """Yield response chunks for streaming UI outputs with pre-flight domain validation and auto-retries."""
        # 1. Pre-flight Domain Validation
        if not is_construction_domain(prompt):
            yield DEFAULT_REFUSAL_TEXT
            return

        url = f"{self.host}/api/chat"
        model = model_override or self.model_name

        sys_prompt = system_prompt or MASTER_CONSTRUCTION_SYSTEM_PROMPT

        messages = [{"role": "system", "content": sys_prompt}]

        if chat_history:
            for msg in chat_history[-6:]:
                role = "assistant" if msg["role"] == "assistant" else "user"
                messages.append({"role": role, "content": msg["content"]})

        messages.append({"role": "user", "content": prompt})

        data = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": 0.3}
        }

        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                    chunk_received = False
                    for line in response:
                        if line:
                            try:
                                chunk = json.loads(line.decode("utf-8"))
                                content = chunk.get("message", {}).get("content", "")
                                if content:
                                    chunk_received = True
                                    yield content
                            except Exception:
                                pass
                    if chunk_received:
                        return
            except Exception as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    time.sleep(1.0 * attempt)

        if last_error:
            raise RuntimeError(f"Streaming failed after {MAX_RETRIES} attempts: {str(last_error)}")

    def _clean_json(self, text: str) -> Dict[str, Any]:
        """Utility to extract JSON contents from raw LLM responses."""
        text = text.strip()
        start_idx = text.find('{')
        end_idx = text.rfind('}')

        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            text = text[start_idx:end_idx + 1]

        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()
        return json.loads(text)


# Singleton Instance for global use
ollama_service = OllamaService()


@st.cache_data(ttl=300, show_spinner=False)
def get_module_context(selection: str, project_id: Optional[str] = None) -> str:
    """Compile page-specific operational context based on the active module and current project."""
    from utils import dummy_data

    if not project_id and "st" in globals() and hasattr(st, "session_state"):
        project_id = st.session_state.get("active_project_id")

    active_p_name = st.session_state.get("active_project_name", "Current Enterprise Project") if hasattr(st, "session_state") else "Current Enterprise Project"
    active_p_code = st.session_state.get("active_project_code", "") if hasattr(st, "session_state") else ""

    norm = selection.lower()
    for char in ["🏠", "🛡️", "🤖", "📁", "💰", "🧱", "👷", "🦺", "🚜", "📈", "📄", "⚙", "ℹ", " "]:
        norm = norm.replace(char, "")

    # Inject hidden module-specific context instruction
    module_instruction = MODULE_CONTEXT_INSTRUCTIONS.get(norm, "You are assisting with general construction intelligence management.")

    context_lines = [
        f"MODULE CONTEXT: {module_instruction}",
        f"CURRENT PROJECT: {active_p_name} ({active_p_code})" if active_p_code else f"CURRENT PROJECT: {active_p_name}",
        ""
    ]

    if "dashboard" in norm:
        try:
            projects = dummy_data.get_projects()
            workers = dummy_data.get_workers()
            kpis = dummy_data.get_dashboard_kpis(projects, workers)
            activities = dummy_data.get_recent_activities()
            deadlines = dummy_data.get_upcoming_deadlines()

            context_lines.append("=== EXECUTIVE DASHBOARD OVERVIEW ===")
            context_lines.append(f"- Active Projects: {kpis['active_projects']} / {kpis['total_projects']}")
            context_lines.append(f"- Project Average Completion: {kpis['project_completion']}%")
            context_lines.append(f"- Budget Utilization: {kpis['budget_utilization']}%")
            context_lines.append(f"- Labor Attendance Today: {kpis['workers']} present")
            context_lines.append(f"- Safety Performance Score: {kpis['safety_score']}%")
            context_lines.append("\nUpcoming Critical Deadlines:")
            for _, d in deadlines.head(3).iterrows():
                context_lines.append(f"  * {d['Project']}: Due {d['Deadline']} ({d['Days Left']} days left) - {d['Priority']} Priority")
        except Exception as e:
            context_lines.append(f"Dashboard data unavailable: {str(e)}")

    elif "projectmanagement" in norm:
        try:
            projects = dummy_data.get_projects()
            context_lines.append("=== PROJECT REGISTRY ===")
            for _, r in projects.iterrows():
                context_lines.append(f"- {r['Project Name']} ({r['Project ID']}): Status={r['Status']}, Budget={r['Budget']:,} INR, Progress={r['Progress']}%")
        except Exception as e:
            context_lines.append(f"Project records unavailable: {str(e)}")

    elif "materialmanagement" in norm:
        try:
            materials = dummy_data.get_materials()
            context_lines.append("=== INVENTORY & MATERIALS LOGISTICS ===")
            for _, r in materials.iterrows():
                context_lines.append(f"- {r['Material']}: Available={r['Available']} units, Required={r['Required']} units, Status={r['Status']}")
        except Exception as e:
            context_lines.append(f"Inventory records unavailable: {str(e)}")

    elif "workermanagement" in norm:
        try:
            workers = dummy_data.get_workers()
            present_count = len(workers[workers["Status"] == "Present"])
            context_lines.append("=== WORKFORCE MANAGEMENT REGISTER ===")
            context_lines.append(f"Total workers tracked: {len(workers)} (Present today: {present_count})")
        except Exception as e:
            context_lines.append(f"Worker registry unavailable: {str(e)}")

    elif "safetymonitoring" in norm:
        try:
            incidents = dummy_data.get_safety_incidents()
            checklist = dummy_data.get_safety_checklist()
            context_lines.append("=== SAFETY COMPLIANCE & INCIDENT LOG ===")
            context_lines.append("Daily Safety Checklist Passed: " + str(sum(1 for v in checklist.values() if v)))
        except Exception as e:
            context_lines.append(f"Safety records unavailable: {str(e)}")

    elif "costestimation" in norm:
        try:
            projects = dummy_data.get_projects()
            context_lines.append("=== COST ESTIMATION & BUDGET FORECASTS ===")
            for _, r in projects.head(5).iterrows():
                context_lines.append(f"- {r['Project Name']}: Budget={r['Budget']:,} INR, Progress={r['Progress']}%")
        except Exception as e:
            context_lines.append(f"Cost models data unavailable: {str(e)}")

    else:
        context_lines.append("=== GENERAL SYSTEM CONTEXT ===")

    return "\n".join(context_lines)
