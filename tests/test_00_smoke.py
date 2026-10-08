"""
Module 00: Smoke Test
---------------------
Your first DeepEval test suite. Demonstrates the difference between
a passing and a failing test using the AnswerRelevancyMetric.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric


def test_answer_relevancy_passing():
    """
    Test Case 1: PASS
    The LLM directly answers the user's inquiry regarding account creation.
    """
    # 1. Define the Metric with an acceptable threshold (0.0 to 1.0)
    # A threshold of 0.7 means the score must be at least 70% relevant.
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7)

    # 2. Define the LLMTestCase
    test_case = LLMTestCase(
        input="How do I create a new account on your portal?",
        actual_output="To create a new account, navigate to the Sign Up page, enter your email, choose a password, and verify your email via the confirmation link."
    )

    # 3. Assert using DeepEval's assert_test
    assert_test(test_case, [relevancy_metric])


def test_answer_relevancy_failing():
    """
    Test Case 2: INTENTIONAL FAIL (for educational inspection)
    The LLM gives an irrelevant answer (talking about pricing when asked about account creation).
    DeepEval will fail this and provide a reason detailing the lack of relevancy.
    """
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7)

    test_case = LLMTestCase(
        input="How do I create a new account on your portal?",
        actual_output="Our premium subscription costs $29 per month and includes unlimited access to all features."
    )

    # In Pytest, we can wrap this in pytest.raises(AssertionError) to verify
    # that our evaluation framework accurately catches irrelevant responses!
    with pytest.raises(AssertionError):
        assert_test(test_case, [relevancy_metric])
