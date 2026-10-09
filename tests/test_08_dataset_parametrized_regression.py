"""
Day 9: Parameterized Golden Dataset Regression Test Suite.

Focus:
- Data-Driven Testing (DDT) using @pytest.mark.parametrize over benchmark datasets.
- Clean test IDs dynamically extracted from inquiry queries.
- Evaluating the live AUT (CustomerSupportRAGBot) against synthetic golden benchmarks.
- Enforcing production quality gates: FaithfulnessMetric and AnswerRelevancyMetric.
"""

import json
from pathlib import Path
import pytest
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from src.bot import CustomerSupportRAGBot

ROOT_DIR = Path(__file__).resolve().parent.parent
GOLDENS_FILE = ROOT_DIR / "data" / "synthetic_goldens.json"


def load_benchmark_goldens():
    """Loads all synthetic goldens from data/synthetic_goldens.json."""
    if not GOLDENS_FILE.exists():
        pytest.skip(f"Benchmark file not found at: {GOLDENS_FILE}")

    with open(GOLDENS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_test_id(golden: dict) -> str:
    """Generates a clean, readable Pytest test ID from the question query."""
    words = golden["input"].split()[:5]
    slug = "_".join(words).replace("?", "").replace(",", "").replace("/", "_")
    return slug[:40]


BENCHMARK_GOLDENS = load_benchmark_goldens()


@pytest.fixture(scope="module")
def live_bot():
    """Module-scoped live CustomerSupportRAGBot instance."""
    return CustomerSupportRAGBot()


@pytest.mark.parametrize(
    "golden",
    BENCHMARK_GOLDENS,
    ids=[format_test_id(g) for g in BENCHMARK_GOLDENS],
)
def test_live_rag_golden_regression(live_bot, golden):
    """
    Parameterized Quality Gate:
    Runs the live CustomerSupportRAGBot against each golden benchmark inquiry,
    verifying both factual faithfulness and answer relevancy.
    """
    # 1. Query live SUT
    response = live_bot.query(golden["input"])

    # 2. Build test case with actual response and golden expected ground truth
    test_case = LLMTestCase(
        input=golden["input"],
        actual_output=response.answer,
        expected_output=golden["expected_output"],
        retrieval_context=response.retrieved_chunks,
    )

    # 3. Quality Gate Thresholds:
    # Faithfulness >= 0.70 (must not contradict knowledge base)
    # AnswerRelevancy >= 0.70 (must directly address inquiry)
    faithfulness_gate = FaithfulnessMetric(threshold=0.7)
    relevancy_gate = AnswerRelevancyMetric(threshold=0.7)

    assert_test(test_case, [faithfulness_gate, relevancy_gate])
