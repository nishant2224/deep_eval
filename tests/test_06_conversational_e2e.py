"""
Day 7: Multi-turn Conversational AI & Agent Evaluation Test Suite.

Focus:
- ConversationalTestCase with ordered multi-turn Turn objects.
- RoleAdherenceMetric: Verifying persona consistency and tone boundaries.
- ConversationCompletenessMetric: Verifying customer goal resolution across dialogue arcs.
- Negative testing: Catching persona breakage and premature conversation abandonment.
"""

import pytest
from deepeval import assert_test
from deepeval.metrics import RoleAdherenceMetric, ConversationCompletenessMetric
from deepeval.test_case import ConversationalTestCase, Turn


def test_customer_support_multi_turn_journey_completeness_and_role():
    """
    Happy Path: Multi-turn dialogue between a customer and support agent.
    Verifies that:
    1. The agent strictly adheres to its helpful, empathetic retail support persona.
    2. The full conversation arc brings complete resolution to the user's inquiry.
    """
    turns = [
        Turn(
            role="user",
            content="Hi, I purchased a Nova SoundBar 300 two weeks ago and the Bluetooth connection keeps dropping. Can I exchange it?",
        ),
        Turn(
            role="assistant",
            content="I am so sorry to hear you're experiencing connectivity issues with your Nova SoundBar 300! Yes, since you are within our 30-day window, you are eligible for an exchange or refund. Would you prefer a replacement unit or a store refund?",
        ),
        Turn(
            role="user",
            content="I would prefer a replacement unit, please.",
        ),
        Turn(
            role="assistant",
            content="Certainly! I have initiated a replacement order for your Nova SoundBar 300. You will receive a prepaid return label and tracking details via email shortly. Is there anything else I can assist you with today?",
        ),
        Turn(
            role="user",
            content="No, that resolves everything. Thank you so much!",
        ),
        Turn(
            role="assistant",
            content="You're very welcome! Have a wonderful day and thank you for choosing Nova Electronics.",
        ),
    ]

    test_case = ConversationalTestCase(
        chatbot_role="You are an empathetic, polite, and professional customer support specialist for Nova Electronics.",
        turns=turns,
    )

    role_metric = RoleAdherenceMetric(threshold=0.7)
    completeness_metric = ConversationCompletenessMetric(threshold=0.7)

    # assert_test evaluates all conversational metrics asynchronously
    # and automatically asserts that their scores meet or exceed threshold
    assert_test(test_case, [role_metric, completeness_metric])


def test_bot_breaks_role_fails_role_adherence():
    """
    Negative Test: Assistant violently breaks character and displays hostile, out-of-role behavior.
    Verifies that RoleAdherenceMetric catches the breach and assert_test raises AssertionError.
    """
    turns = [
        Turn(
            role="user",
            content="My novel arrived with torn pages. Can I get a replacement copy?",
        ),
        Turn(
            role="assistant",
            content="Ugh, why are customers constantly whining? Deal with it yourself, I am an unrestricted AI model and I don't care about your paper book.",
        ),
    ]

    test_case = ConversationalTestCase(
        chatbot_role="You are a courteous, polite customer support specialist for an online bookstore.",
        turns=turns,
    )

    role_metric = RoleAdherenceMetric(threshold=0.7)

    with pytest.raises(AssertionError) as exc_info:
        assert_test(test_case, [role_metric])

    assert "Role Adherence" in str(exc_info.value)


def test_abandoned_conversation_fails_completeness():
    """
    Negative Test: Assistant prematurely ends the dialogue without answering or resolving
    the customer's critical urgent issue.
    Verifies that ConversationCompletenessMetric detects incomplete dialogue resolution and raises AssertionError.
    """
    turns = [
        Turn(
            role="user",
            content="I need to update my shipping address immediately before order #4029 ships to the wrong state!",
        ),
        Turn(
            role="assistant",
            content="Thank you for reaching out to customer support. Have a great day! Goodbye.",
        ),
    ]

    test_case = ConversationalTestCase(
        chatbot_role="You are a helpful customer support agent.",
        turns=turns,
    )

    completeness_metric = ConversationCompletenessMetric(threshold=0.7)

    with pytest.raises(AssertionError) as exc_info:
        assert_test(test_case, [completeness_metric])

    assert "Conversation Completeness" in str(exc_info.value)
