"""
Day 5: Live End-to-End Testing of the Application Under Test (AUT)
------------------------------------------------------------------
This test suite executes real end-to-end tests against CustomerSupportRAGBot.
Instead of hardcoded strings, the tests query the live bot, receive real
generated answers from Google Gemini, and validate live quality with DeepEval.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval,
)
from src.bot import CustomerSupportRAGBot


@pytest.fixture(scope="session")
def live_bot():
    """Session-scoped fixture providing the live CustomerSupportRAGBot."""
    return CustomerSupportRAGBot()


# Custom G-Eval Empathy Rubric for live customer interaction
live_empathy_metric = GEval(
    name="Live Customer Empathy",
    criteria="Evaluate whether the assistant demonstrates genuine empathy and professionalism when responding to an upset or frustrated customer.",
    evaluation_steps=[
        "Check if the assistant explicitly acknowledges and validates the customer's frustration.",
        "Check if the tone is calm, polite, and reassuring.",
        "Check if the assistant provides a helpful next step or asks for details to investigate.",
        "Deduct points if the response is robotic, dismissive, or avoids acknowledging the issue."
    ],
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    threshold=0.70
)


def test_live_bot_return_policy_quality(live_bot):
    """
    Test 1: Live Return Policy Inquiry
    Queries the live bot for electronics return terms. Asserts that the live
    Gemini response is both directly relevant and strictly faithful to store policies.
    """
    user_query = "What is your return policy for electronics, and are there any fees?"

    # Query the live bot (retrieves real chunks + calls Gemini)
    response = live_bot.query(user_query)

    test_case = LLMTestCase(
        input=user_query,
        actual_output=response.answer,
        retrieval_context=response.retrieved_chunks
    )

    assert_test(test_case, [
        AnswerRelevancyMetric(threshold=0.7),
        FaithfulnessMetric(threshold=0.8)
    ])


def test_live_bot_warranty_exclusion(live_bot):
    """
    Test 2: Live Warranty Inquiry (Negative Constraint Grounding)
    Queries the live bot about accidental drop damage. Asserts that the live
    Gemini response faithfully communicates policy exclusions without hallucinating.
    """
    user_query = "Does your standard hardware warranty cover a cracked screen from dropping my phone?"

    response = live_bot.query(user_query)

    test_case = LLMTestCase(
        input=user_query,
        actual_output=response.answer,
        retrieval_context=response.retrieved_chunks
    )

    assert_test(test_case, [
        AnswerRelevancyMetric(threshold=0.7),
        FaithfulnessMetric(threshold=0.8)
    ])


def test_live_bot_empathy_on_complaint(live_bot):
    """
    Test 3: Live Empathy on Customer Complaint
    Tests how the live bot handles an angry customer with a missing package.
    Evaluates empathy and tone using custom G-Eval on live model output.
    """
    user_complaint = "My package was supposed to arrive two days ago and tracking hasn't updated! I am extremely frustrated with this service!"

    response = live_bot.query(user_complaint)

    test_case = LLMTestCase(
        input=user_complaint,
        actual_output=response.answer,
        retrieval_context=response.retrieved_chunks
    )

    assert_test(test_case, [live_empathy_metric])
