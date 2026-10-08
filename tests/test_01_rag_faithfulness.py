"""
Day 2: RAG Pipeline Evaluation Part 1 - Faithfulness & Hallucination
-------------------------------------------------------------------
This test suite verifies whether an LLM generates responses strictly
derived from retrieved internal documentation without hallucinating facts.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, HallucinationMetric


def test_rag_faithfulness_passing():
    """
    Test Case 1: PASSING
    The LLM answers the user's return policy inquiry using ONLY
    the facts present in the retrieved internal knowledge base.
    """
    # 1. Define FaithfulnessMetric (threshold >= 0.8 means 80%+ claims must be grounded)
    metric = FaithfulnessMetric(threshold=0.8)

    # 2. Define the test case with retrieval_context
    test_case = LLMTestCase(
        input="What is your return policy for electronics?",
        actual_output="Electronics can be returned within 14 days of delivery if they are in original packaging. A 10% restocking fee applies to opened boxes.",
        retrieval_context=[
            "Electronics items may be returned within 14 days of confirmed delivery.",
            "All returned electronics must include original packaging and accessories.",
            "A 10% restocking fee is deducted for opened electronics boxes.",
            "Items damaged due to misuse are not eligible for refunds."
        ]
    )

    # 3. Assert test passes
    assert_test(test_case, [metric])


def test_rag_faithfulness_failing_with_hallucination():
    """
    Test Case 2: INTENTIONAL FAIL (Catching Hallucination)
    The LLM invents facts (claims free return shipping and 60 days) that are
    nowhere in the retrieved documentation. DeepEval detects the ungrounded claims.
    """
    metric = FaithfulnessMetric(threshold=0.8)

    test_case = LLMTestCase(
        input="What is your return policy for electronics?",
        actual_output="You can return electronics up to 60 days after purchase with free return shipping on all orders.",
        retrieval_context=[
            "Electronics items may be returned within 14 days of confirmed delivery.",
            "Customers are responsible for return postage unless the item arrived defective."
        ]
    )

    # In Pytest, we expect an AssertionError because the response contains hallucinations
    with pytest.raises(AssertionError):
        assert_test(test_case, [metric])


def test_rag_hallucination_metric():
    """
    Test Case 3: HallucinationMetric
    HallucinationMetric measures contradiction against contexts (lower score = less hallucination).
    A threshold of 0.3 means hallucination score must not exceed 30%.
    """
    # In modern DeepEval: 1.0 is full alignment (pass), 0.0 is failure.
    # threshold=0.7 means alignment score must be at least 70%.
    hallucination_metric = HallucinationMetric(threshold=0.7)

    test_case = LLMTestCase(
        input="What are the store hours on Sundays?",
        actual_output="On Sundays, the store is open from 10:00 AM to 5:00 PM.",
        # HallucinationMetric accepts 'contexts' parameter
        context=[
            "Our retail store is open Monday through Saturday from 9:00 AM to 8:00 PM.",
            "Sunday store hours are 10:00 AM to 5:00 PM."
        ]
    )

    assert_test(test_case, [hallucination_metric])
