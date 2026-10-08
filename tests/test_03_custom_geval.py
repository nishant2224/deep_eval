"""
Day 4: Custom Business Rubrics with G-Eval
------------------------------------------
This test suite demonstrates how SDETs define custom evaluation rubrics
using natural language criteria to test business logic, brand tone,
empathy, and actionability.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval


# Reusable Custom G-Eval Metric: Empathy & Tone
empathy_metric = GEval(
    name="Customer Empathy & Professionalism",
    criteria="Evaluate whether the response demonstrates genuine empathy, politeness, and professionalism when handling a customer complaint.",
    evaluation_steps=[
        "Check if the response explicitly acknowledges the customer's frustration or inconvenience.",
        "Check if the tone remains polite, warm, and respectful without defensive or dismissive wording.",
        "Check if the assistant offers concrete assistance or a constructive solution.",
        "Deduct points heavily if the response is cold, robotic, or blames the customer."
    ],
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    threshold=0.75
)

# Reusable Custom G-Eval Metric: Actionability
actionability_metric = GEval(
    name="IT Security Actionability",
    criteria="Determine whether the IT support response provides clear, immediate, and actionable steps for an urgent security event.",
    evaluation_steps=[
        "Check if the response provides an immediate emergency action (e.g. hotline phone number or remote-lock procedure).",
        "Check if clear follow-up steps (such as filing a portal report or password change) are specified.",
        "Deduct points if the advice is vague, passive, or leaves the user guessing."
    ],
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    threshold=0.75
)


def test_geval_empathy_passing():
    """
    Test 1: PASSING Empathy Rubric
    The bot acknowledges an angry customer's delayed order, validates their feelings,
    and proactively offers immediate tracking and resolution options.
    """
    test_case = LLMTestCase(
        input="My package was supposed to arrive yesterday for my daughter's birthday and it is still missing! This is completely unacceptable!",
        actual_output="I am truly sorry to hear that your daughter's birthday gift hasn't arrived on time. I completely understand how stressful and disappointing this is. Let me investigate this right now—could you please provide your order number so I can locate the package or arrange an expedited replacement immediately?"
    )

    assert_test(test_case, [empathy_metric])


def test_geval_empathy_failing():
    """
    Test 2: INTENTIONAL FAIL (Cold, Robotic, Defensive Tone)
    The bot is dismissive, blames transit carriers, and provides zero empathy.
    DeepEval's G-Eval deducts points and fails the threshold.
    """
    test_case = LLMTestCase(
        input="My package was supposed to arrive yesterday for my daughter's birthday and it is still missing! This is completely unacceptable!",
        actual_output="Shipping delays are beyond our control. You need to check the carrier tracking link sent to your email. We do not issue refunds for delivery carrier delays."
    )

    with pytest.raises(AssertionError):
        assert_test(test_case, [empathy_metric])


def test_geval_actionability_passing():
    """
    Test 3: PASSING Actionability Rubric
    The bot handles a lost laptop scenario with immediate, concrete security steps.
    """
    test_case = LLMTestCase(
        input="I left my company laptop in an airport taxi 10 minutes ago. What should I do right now?",
        actual_output="1. Immediately call the 24/7 IT Security Incident Line at +1-800-555-0199 to trigger a remote device lock. 2. Change your corporate SSO password from your mobile device. 3. Submit a Lost Asset report on security.internal.corp within 2 hours."
    )

    assert_test(test_case, [actionability_metric])
