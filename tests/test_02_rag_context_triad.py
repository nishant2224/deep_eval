"""
Day 3: RAG Pipeline Evaluation Part 2 - The Context Retrieval Triad
-------------------------------------------------------------------
This test suite evaluates the Search / Retriever component of a RAG pipeline:
1. ContextualRelevancyMetric: Measures noise and irrelevant chunks.
2. ContextualRecallMetric: Measures whether any critical facts were missed.
3. ContextualPrecisionMetric: Measures if the best chunks were ranked at the top.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
)


def test_contextual_relevancy():
    """
    Test 1: Contextual Relevancy (Noise detection)
    Checks if the retrieved context is focused on the user query
    without including excessive irrelevant text.
    """
    metric = ContextualRelevancyMetric(threshold=0.7)

    test_case = LLMTestCase(
        input="What are the passport validity requirements for entering Japan?",
        actual_output="Your passport must be valid for the entire duration of your stay in Japan.",
        retrieval_context=[
            "For foreign tourists entering Japan, passports must be valid for the full period of intended stay.",
            "Japan does not strictly enforce a 6-month passport validity rule for tourist visa-waiver countries, provided the passport remains valid throughout the visit.",
        ]
    )

    assert_test(test_case, [metric])


def test_contextual_recall_missing_critical_fact():
    """
    Test 2: Contextual Recall (Missing facts detection)
    The expected answer requires TWO distinct facts:
      1. Laptop return window (30 days)
      2. 2-year warranty and accidental damage protection.
    The retriever ONLY fetched fact #1 and completely missed fact #2!
    DeepEval assigns a score of 0.5 (< threshold 0.8) and fails.
    """
    metric = ContextualRecallMetric(threshold=0.8)

    test_case = LLMTestCase(
        input="What are the return and warranty terms for laptops?",
        actual_output="Laptops can be returned within 30 days of purchase.",
        expected_output="Laptops can be returned within 30 days of purchase. Additionally, all laptops come with a 2-year manufacturer warranty and 1 year of accidental damage protection.",
        # The retriever completely missed the warranty document!
        retrieval_context=[
            "Customers may return laptops within 30 days of purchase for a full refund."
        ]
    )

    # In Pytest, this raises an AssertionError because recall is 0.50 (< 0.8 threshold)
    with pytest.raises(AssertionError):
        assert_test(test_case, [metric])


def test_contextual_precision_ranking():
    """
    Test 3: Contextual Precision (Rank evaluation)
    Verifies that the most directly relevant chunk appears at the TOP (Rank #1)
    rather than being buried under general background information.
    """
    metric = ContextualPrecisionMetric(threshold=0.7)

    test_case = LLMTestCase(
        input="How do I reset my multi-factor authentication (MFA)?",
        actual_output="To reset your MFA, log into the IT Self-Service portal, select Security Settings, and click Reset MFA Device.",
        expected_output="Users can reset MFA by going to the IT Self-Service portal, choosing Security Settings, and selecting Reset MFA Device.",
        retrieval_context=[
            # Rank 1: Directly answers the question
            "To reset your MFA, log into the IT Self-Service portal, navigate to Security Settings, and click 'Reset MFA Device'.",
            # Rank 2: Relevant background
            "MFA resets require verification via backup email or phone number.",
            # Rank 3: Supplementary security policy
            "Company security policy mandates multi-factor authentication for all remote employees."
        ]
    )

    assert_test(test_case, [metric])


def test_end_to_end_context_triad():
    """
    Test 4: Full Retrieval Triad Suite
    Evaluates all three retriever metrics simultaneously on a well-designed RAG response.
    """
    relevancy_metric = ContextualRelevancyMetric(threshold=0.7)
    recall_metric = ContextualRecallMetric(threshold=0.7)
    precision_metric = ContextualPrecisionMetric(threshold=0.7)

    test_case = LLMTestCase(
        input="What are the baggage size limits for carry-on luggage?",
        actual_output="Carry-on luggage must not exceed 22 x 14 x 9 inches (56 x 36 x 23 cm) and must fit in the overhead bin.",
        expected_output="Carry-on luggage must be within 22 x 14 x 9 inches (56 x 36 x 23 cm) including handles and wheels, and must fit in the overhead compartment.",
        retrieval_context=[
            "Carry-on baggage limits: Maximum dimensions are 22 x 14 x 9 inches (56 x 36 x 23 cm), including handles and wheels.",
            "All carry-on items must easily fit into the overhead bin or beneath the seat in front of you."
        ]
    )

    assert_test(test_case, [relevancy_metric, recall_metric, precision_metric])
