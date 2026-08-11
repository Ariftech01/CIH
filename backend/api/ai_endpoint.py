"""Local Backend API Endpoint for Floating AI Assistant & CIH Enterprise AI Gateway."""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any
from backend.app_logging.logger import logger
from backend.ai_engine.ai_pipeline import ai_enterprise_pipeline

AI_ENDPOINT_PORT = 8502
_server_instance: HTTPServer = None
_server_thread: threading.Thread = None


class AIEnterpriseHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler routing requests through AIEnterprisePipeline."""

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path in ["/api/health", "/api/v1/health"]:
            self._set_headers(200)
            res = {
                "status": "healthy",
                "service": "CIH Enterprise AI Pipeline API",
                "version": "1.0.0",
                "port": AI_ENDPOINT_PORT
            }
            self.wfile.write(json.dumps(res).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_POST(self):
        if self.path in ["/api/chat", "/api/v1/chat"]:
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body_bytes = self.rfile.read(content_len)
                data: Dict[str, Any] = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}

                prompt = data.get("message") or data.get("prompt") or ""
                module_name = data.get("module") or data.get("activeModule")
                history = data.get("history") or data.get("messages") or []
                doc_context = data.get("document")

                # Route query through unified Python Enterprise AI Pipeline
                pipeline_result = ai_enterprise_pipeline.process_query(
                    prompt=prompt,
                    module_name=module_name,
                    chat_history=history,
                    document_context=doc_context
                )

                self._set_headers(200)
                self.wfile.write(json.dumps(pipeline_result).encode("utf-8"))
            except Exception as e:
                logger.error(f"Error handling AI endpoint query: {e}")
                self._set_headers(500)
                err_res = {
                    "is_valid": True,
                    "response": f"⚠️ Error processing query through CIH AI Pipeline: {str(e)}",
                    "intent": "ERROR",
                    "extracted_entities": {},
                    "latency_ms": {},
                    "cached": False
                }
                self.wfile.write(json.dumps(err_res).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def log_message(self, format, *args):
        # Silence default HTTP server console noise
        pass


def start_ai_endpoint_server(port: int = AI_ENDPOINT_PORT) -> bool:
    """Start local background daemon HTTP server for AI Enterprise Gateway."""
    global _server_instance, _server_thread
    if _server_instance is not None:
        return True

    try:
        _server_instance = HTTPServer(("127.0.0.1", port), AIEnterpriseHTTPHandler)
        _server_thread = threading.Thread(target=_server_instance.serve_forever, daemon=True)
        _server_thread.start()
        logger.info(f"CIH Enterprise AI Endpoint background server started on http://127.0.0.1:{port}")
        return True
    except Exception as e:
        logger.warning(f"Could not start AI Endpoint background server on port {port}: {e}")
        return False
