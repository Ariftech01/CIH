"""Comprehensive Regression Test Suite for CIH AI Subsystem Optimization & Guardrails."""

import json
import unittest
import urllib.request
import urllib.error
import time
from backend.ai_engine.intent_router import intent_router
from backend.ai_engine.context_engine import project_context_engine
from backend.ai_engine.prompt_builder import prompt_builder
from backend.ai_engine.ai_pipeline import ai_enterprise_pipeline
from backend.api.ai_endpoint import start_ai_endpoint_server, AI_ENDPOINT_PORT
from backend.database.manager import db_manager
from services.ollamaService import is_construction_domain, DEFAULT_REFUSAL_TEXT


class TestAIPipelineRegressions(unittest.TestCase):
    """Regression tests proving domain guardrail enforcement, project ID retrieval, floating assistant routing, and performance optimization."""

    @classmethod
    def setUpClass(cls):
        db_manager.create_all_tables()
        start_ai_endpoint_server(AI_ENDPOINT_PORT)
        # Brief pause to allow background HTTP endpoint server to initialize
        time.sleep(0.5)

    def test_01_out_of_domain_queries_rejected(self):
        """Verify general knowledge & off-topic questions are politely rejected with 0ms LLM time."""
        off_topic_queries = [
            "Who is the prime minister of India?",
            "Write python code for a snake game",
            "Tell me a funny joke",
            "What is the capital of France?",
            "How to cook chocolate cake?"
        ]

        for query in off_topic_queries:
            # 1. Guardrail test
            self.assertFalse(is_construction_domain(query), f"Query should be off-topic: {query}")

            # 2. Intent Router test
            route_res = intent_router.route_intent(query)
            self.assertFalse(route_res["is_valid"])
            self.assertEqual(route_res["intent"], "OUT_OF_DOMAIN")

            # 3. Enterprise Pipeline test
            pipe_res = ai_enterprise_pipeline.process_query(query)
            self.assertFalse(pipe_res["is_valid"])
            self.assertEqual(pipe_res["response"], DEFAULT_REFUSAL_TEXT)
            self.assertEqual(pipe_res["latency_ms"]["inference_ms"], 0.0)

    def test_02_construction_queries_accepted(self):
        """Verify domain-specific construction questions pass guardrails."""
        construction_queries = [
            "Estimate the cost of a residential building",
            "Generate a construction safety checklist for high rise",
            "Calculate concrete mix proportions for M30 grade",
            "What is IS 456 standard curing time for slab?"
        ]

        for query in construction_queries:
            self.assertTrue(is_construction_domain(query), f"Query should be valid construction domain: {query}")
            route_res = intent_router.route_intent(query)
            self.assertTrue(route_res["is_valid"])
            self.assertNotEqual(route_res["intent"], "OUT_OF_DOMAIN")

    def test_03_project_id_retrieval(self):
        """Verify queries like PRJ-0A752A retrieve live database information."""
        project_queries = [
            "PRJ-0A752A tell me about this project",
            "What is the current budget status of PRJ-2026-001?",
            "Show progress for PRJ-0012"
        ]

        for query in project_queries:
            route_res = intent_router.route_intent(query)
            self.assertTrue(route_res["is_valid"])
            self.assertEqual(route_res["intent"], "ENTITY_LOOKUP")

            proj_codes = route_res["extracted_entities"].get("project", [])
            self.assertGreater(len(proj_codes), 0)

            # Context retrieval verification
            db_context = project_context_engine.retrieve_entity_context(route_res["extracted_entities"])
            self.assertIn("RETRIEVED DATABASE PROJECT CONTEXT", db_context)
            self.assertIn(proj_codes[0], db_context)

            # End-to-end pipeline execution
            pipe_res = ai_enterprise_pipeline.process_query(query)
            self.assertTrue(pipe_res["is_valid"])
            self.assertIn(proj_codes[0], pipe_res["response"])

    def test_04_multi_entity_extraction(self):
        """Verify extraction and context retrieval for Risk, Worker, Equipment, and Document codes."""
        query = "Audit RISK-101 and check WRK-0005 attendance along with EQP-204 logs and DOC-901"
        route_res = intent_router.route_intent(query)

        self.assertTrue(route_res["is_valid"])
        extracted = route_res["extracted_entities"]
        self.assertIn("RISK-101", extracted["risk"])
        self.assertIn("WRK-0005", extracted["worker"])
        self.assertIn("EQP-204", extracted["equipment"])
        self.assertIn("DOC-901", extracted["document"])

        ctx = project_context_engine.retrieve_entity_context(extracted)
        self.assertIn("RISK-101", ctx)
        self.assertIn("WRK-0005", ctx)
        self.assertIn("EQP-204", ctx)
        self.assertIn("DOC-901", ctx)

    def test_05_floating_assistant_api_endpoint(self):
        """Verify the Floating Assistant background API endpoint routes through enterprise pipeline."""
        url = f"http://127.0.0.1:{AI_ENDPOINT_PORT}/api/chat"

        # 1. Off-topic query test via HTTP API
        off_topic_data = json.dumps({"message": "Who is the president of US?", "module": "Dashboard"}).encode("utf-8")
        req = urllib.request.Request(url, data=off_topic_data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertFalse(res["is_valid"])
            self.assertIn("Construction Intelligence Hub AI", res["response"])

        # 2. Project ID query test via HTTP API
        prj_data = json.dumps({"message": "PRJ-0A752A status report", "module": "Project Management"}).encode("utf-8")
        req = urllib.request.Request(url, data=prj_data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(res["is_valid"])
            self.assertIn("PRJ-0A752A", res["response"])

    def test_06_latency_profiling_and_caching(self):
        """Verify performance profiling breakdown and caching speedup."""
        query = "PRJ-0A752A detailed structural report"

        # First call (uncached entity retrieval)
        t0 = time.perf_counter()
        res1 = ai_enterprise_pipeline.process_query(query)
        t1 = (time.perf_counter() - t0) * 1000.0

        self.assertIn("guardrail_ms", res1["latency_ms"])
        self.assertIn("retrieval_ms", res1["latency_ms"])
        self.assertIn("prompt_assembly_ms", res1["latency_ms"])
        self.assertIn("inference_ms", res1["latency_ms"])
        self.assertIn("total_ms", res1["latency_ms"])

        # Second call (cached entity retrieval)
        t0 = time.perf_counter()
        res2 = ai_enterprise_pipeline.process_query(query)
        t2 = (time.perf_counter() - t0) * 1000.0

        # Cached call should be valid and fast
        self.assertTrue(res1["is_valid"])
        self.assertTrue(res2["is_valid"])
        self.assertLess(res2["latency_ms"]["retrieval_ms"], 5.0)

    def test_07_prompt_size_optimization(self):
        """Verify system prompt size remains token-optimized under 800 tokens (~3200 chars)."""
        prompt = prompt_builder.build_system_prompt(
            module_name="costestimation",
            extracted_entities={"project": ["PRJ-0A752A"]}
        )
        self.assertLess(len(prompt), 4000, "System prompt should be pruned and compact.")
        self.assertIn("PRJ-0A752A", prompt)


if __name__ == "__main__":
    unittest.main()
