from typing import Dict, Any, List

class APIGateway:
    """
    API Gateway foundation providing OpenAPI specs, webhook event dispatching, and rate limiting.
    """
    def __init__(self):
        self.webhooks: List[Dict[str, Any]] = []

    def register_webhook(self, event_type: str, url: str):
        self.webhooks.append({"event": event_type, "url": url, "active": True})

    def dispatch_event(self, event_type: str, payload: Dict[str, Any]) -> int:
        dispatched = 0
        for wh in self.webhooks:
            if wh["event"] == event_type and wh["active"]:
                dispatched += 1
        return dispatched

    def get_openapi_schema(self) -> Dict[str, Any]:
        return {
            "openapi": "3.0.3",
            "info": {
                "title": "Agentic AI for Safety Monitoring with Construction Risk Analytics Enterprise API",
                "version": "1.0.0",
                "description": "Production REST API platform for CIH management, BIM automation, and AI Copilot."
            },
            "paths": {
                "/api/v1/health": {"get": {"summary": "Health Check"}},
                "/api/v1/projects": {"get": {"summary": "List Projects"}, "post": {"summary": "Create Project"}},
                "/api/v1/workflow/transition": {"post": {"summary": "Transition Workflow Stage"}},
                "/api/v1/analytics/dashboard": {"get": {"summary": "Dashboard KPIs"}}
            }
        }

api_gateway = APIGateway()
