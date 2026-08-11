"""Performance Benchmark Suite for CIH Enterprise Optimization."""

import time
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


class BenchmarkPerformance(unittest.TestCase):
    """Execution time benchmark tests."""

    def test_01_dummy_data_caching_performance(self):
        from utils.dummy_data import get_projects, get_workers, get_materials, get_equipment

        # First call (populates cache)
        t0 = time.perf_counter()
        p1 = get_projects()
        w1 = get_workers()
        m1 = get_materials()
        e1 = get_equipment()
        t_uncached = (time.perf_counter() - t0) * 1000.0

        # Second call (from cache)
        t0 = time.perf_counter()
        p2 = get_projects()
        w2 = get_workers()
        m2 = get_materials()
        e2 = get_equipment()
        t_cached = (time.perf_counter() - t0) * 1000.0

        print(f"\n[BENCHMARK] Dummy Data Generation: Uncached={t_uncached:.2f}ms | Cached={t_cached:.2f}ms")
        self.assertLess(t_cached, t_uncached + 5.0)
        self.assertEqual(len(p1), len(p2))

    def test_02_ollama_module_context_performance(self):
        from services.ollamaService import get_module_context

        t0 = time.perf_counter()
        ctx1 = get_module_context("🏠 Dashboard")
        t_first = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        ctx2 = get_module_context("🏠 Dashboard")
        t_second = (time.perf_counter() - t0) * 1000.0

        print(f"[BENCHMARK] Ollama Module Context: First={t_first:.2f}ms | Cached={t_second:.2f}ms")
        self.assertLessEqual(t_second, t_first + 2.0)
        self.assertEqual(ctx1, ctx2)

    def test_03_hybrid_runtime_startup_performance(self):
        from backend.startup import initialize_hybrid_runtime

        t0 = time.perf_counter()
        res1 = initialize_hybrid_runtime()
        t_first = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        res2 = initialize_hybrid_runtime()
        t_second = (time.perf_counter() - t0) * 1000.0

        print(f"[BENCHMARK] Hybrid Runtime Init: First={t_first:.2f}ms | Cached={t_second:.2f}ms")
        self.assertLessEqual(t_second, 5.0)

    def test_04_document_extraction_performance(self):
        from modules.ai_analysis import extract_text_from_file
        import io

        class DummyFile:
            def __init__(self, name: str, content: bytes):
                self.name = name
                self._content = content

            def getvalue(self):
                return self._content

        sample_txt = DummyFile("test.txt", b"Header: BOQ Scope\nItem 1: Concrete mix M30\nQuantity: 500 cu.m")
        t0 = time.perf_counter()
        text = extract_text_from_file(sample_txt)
        t_extract = (time.perf_counter() - t0) * 1000.0

        print(f"[BENCHMARK] Document Extraction: {t_extract:.2f}ms")
        self.assertIn("BOQ Scope", text)

    def test_05_crie_context_caching_performance(self):
        from modules.construction_risk import _get_cached_cri_context

        t0 = time.perf_counter()
        ctx1, dash1 = _get_cached_cri_context("proj_test_01", "Test Project")
        t_first = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        ctx2, dash2 = _get_cached_cri_context("proj_test_01", "Test Project")
        t_second = (time.perf_counter() - t0) * 1000.0

        print(f"[BENCHMARK] CRIE Risk Context: First={t_first:.2f}ms | Cached={t_second:.2f}ms")
        self.assertLessEqual(t_second, t_first + 2.0)

    def test_06_sidebar_logo_caching_performance(self):
        from utils.styles import _get_base64_logo

        logo_file = str(ROOT / "assets" / "logo.png")
        t0 = time.perf_counter()
        enc1 = _get_base64_logo(logo_file)
        t_first = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        enc2 = _get_base64_logo(logo_file)
        t_second = (time.perf_counter() - t0) * 1000.0

        print(f"[BENCHMARK] Sidebar Logo Base64: First={t_first:.2f}ms | Cached={t_second:.2f}ms")
        self.assertLessEqual(t_second, 0.5)


if __name__ == "__main__":
    unittest.main()
