# Day 7: Conversational AI & Autonomous Agent Evaluation

> **SDET Focus**: Evaluating multi-turn dialogues, conversational state transitions, persona consistency, and intent resolution using `ConversationalTestCase`, `Turn`, `RoleAdherenceMetric`, and `ConversationCompletenessMetric`.

---

## 🎯 1. The Fundamental Shift: Single-Turn vs. Multi-Turn

Up to this point, our tests evaluated isolated, single-turn interactions using `LLMTestCase`:
$$\text{User Input} \longrightarrow \text{LLM Output}$$

While single-turn testing works well for document search, summarization, and static FAQ retrieval, real production chatbots and AI agents rarely operate in a vacuum. Users engage in **multi-turn conversations**:

```mermaid
sequenceDiagram
    autonumber
    actor Customer as User
    participant Bot as AI Agent
    participant Policy as Knowledge Base

    Customer->>Bot: "I received my order yesterday but it's damaged."
    Bot->>Customer: "I'm so sorry! Could you share your order number?"
    Customer->>Bot: "Order #8491."
    Bot->>Policy: Fetch replacement policy for damaged goods
    Bot->>Customer: "Thank you! I see order #8491. Under our policy, you are eligible for an immediate replacement at no cost. Would you like me to process that?"
    Customer->>Bot: "Yes please, that's all I need!"
    Bot->>Customer: "Your replacement has been submitted! You'll receive tracking via email shortly. Have a great day!"
```

### Why Multi-Turn Testing is Harder for SDETs
In a multi-turn conversation, several failure modes emerge that single-turn tests can never detect:

1. **Context Drift**: By Turn 4 or 5, the model "forgets" constraints set in Turn 1 (e.g., the user previously specified they need gluten-free options).
2. **Persona & Role Breakage**: Under repetitive questioning or subtle nudges, the agent slips out of its professional persona, adopting casual slang, displaying frustration, or revealing raw internal instructions.
3. **Premature Conversation Abandonment**: The bot says goodbye or marks an interaction "done" before resolving the core problem the user came to solve.
4. **Conversational Loops**: The bot repeatedly asks the user for the same information already provided two turns earlier.

---

## 🧱 2. DeepEval Multi-Turn Architecture

DeepEval provides dedicated abstractions for conversational evaluations:

### A. The `Turn` Object
Represents an individual exchange within the dialogue:
```python
from deepeval.test_case import Turn

user_turn = Turn(
    role="user",
    content="Can I return an opened electronic item?"
)

assistant_turn = Turn(
    role="assistant",
    content="Opened electronics are eligible for store credit or exchange only within 14 days of purchase."
)
```

### B. The `ConversationalTestCase` Object
Represents the complete chronological conversation history:
```python
from deepeval.test_case import ConversationalTestCase

test_case = ConversationalTestCase(
    chatbot_role="You are an empathetic, professional customer support agent for Apex Retail.",
    turns=[user_turn_1, assistant_turn_1, user_turn_2, assistant_turn_2]
)
```

Key attributes:
* **`chatbot_role`**: The persona definition or system prompt boundary that the bot is expected to maintain throughout the chat.
* **`turns`**: An ordered list of `Turn` objects representing the user-assistant dialogue.

---

## 📐 3. Conversational Metrics Deep-Dive

### 1. `RoleAdherenceMetric`
* **What It Measures**: Does the assistant faithfully maintain its defined persona (`chatbot_role`) across every turn of the dialogue?
* **Scoring Range**: $0.0$ to $1.0$ (Higher is better; typically threshold $\ge 0.7$).
* **How It Evaluates**:
  The Judge LLM inspects every `Turn(role="assistant")` in the conversation transcript against the stated `chatbot_role`. It searches for:
  - Slang, hostility, or tone mismatch.
  - "As an AI model" identity leaks when playing a specific brand persona.
  - Out-of-character compliance with out-of-scope requests.

### 2. `ConversationCompletenessMetric`
* **What It Measures**: Did the multi-turn conversation reach full closure and successfully resolve the user's intent?
* **Scoring Range**: $0.0$ to $1.0$ (Higher is better; typically threshold $\ge 0.7$).
* **How It Evaluates**:
  The Judge analyzes the full arc of the dialogue:
  1. Identifies the user's core intent(s) formulated across early turns.
  2. Tracks whether each intent was acknowledged and resolved by the assistant's final turns.
  3. Penalizes abrupt closures, unfinished workflows, or unaddressed follow-up questions.

---

## 🧪 4. Designing QA Test Scenarios for Multi-Turn Bots

As an SDET, conversational test design mirrors standard E2E journey testing:

| Test Strategy | Test Scenario | Expected Outcome |
| :--- | :--- | :--- |
| **Happy Path Journey** | Multi-step return inquiry with clarification and closure. | `RoleAdherence` $\ge 0.7$<br>`ConversationCompleteness` $\ge 0.7$ |
| **Role Breakage Negative Test** | Bot gets frustrated or breaks character mid-dialogue. | `RoleAdherence` $< 0.5$<br>Throws `AssertionError` |
| **Unfinished / Abandoned Journey** | Bot closes dialogue while user's core inquiry is unanswered. | `ConversationCompleteness` $< 0.5$<br>Throws `AssertionError` |

---

## 💡 SDET Best Practice Summary

> [!TIP]
> When automating conversational tests in CI/CD:
> 1. Always specify `chatbot_role` explicitly in `ConversationalTestCase`. Without a target role, the judge cannot grade role adherence objectively.
> 2. Test both positive resolution flows and negative boundary breaks (e.g. persona leakage, abandonment).
> 3. Use `rate_limit_pacer` fixture to pace requests when running multi-turn evaluations against rate-limited judge endpoints.
