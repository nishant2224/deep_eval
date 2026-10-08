# Module 01: Mental Model & Foundations of LLM Evaluation

## 1. Deterministic vs. Probabilistic Testing

As an SDET with Pytest, Selenium, and Playwright experience, your testing intuition has been built around **deterministic systems**:

| Attribute | Deterministic Testing (Playwright / Selenium / APIs) | Probabilistic Testing (DeepEval / LLMs / GenAI) |
| :--- | :--- | :--- |
| **Output Nature** | Exact, predictable values (HTTP 200, specific JSON keys, exact UI text). | Varied, generative text with semantic equivalence. |
| **Assertion Strategy** | Strict equality: `assert actual == expected` or regex matching. | Semantic scoring: `assert score >= threshold` (0.0 to 1.0). |
| **Flakiness Cause** | Timing issues, race conditions, network latency, stale DOM elements. | Temperature variation, model drift, prompt ambiguity, stochastic sampling. |
| **Test Pass Criteria** | Binary: Pass or Fail. | Rubric-based: Quality grade (e.g., 0.85/1.00) with a reason explaining deductions. |

---

## 2. Why Traditional Assertion Methods Fail for GenAI

1. **Exact String Match (`==`)**:
   - Prompt: *"Summarize our refund policy."*
   - Output A: *"Full refunds are issued within 30 days."*
   - Output B: *"You can get your money back in full up to 30 days after purchase."*
   - Both are 100% correct, but `Output A == Output B` evaluates to `False`.

2. **Regex & Keyword Matching (`in`)**:
   - Prompt: *"Can I cancel my annual subscription anytime?"*
   - Output: *"No, you cannot cancel your annual subscription at any time."*
   - If your test checks `"cancel" in output and "annual subscription" in output`, the test passes despite the system giving the completely wrong answer if the policy allows cancellations!

3. **BLEU & ROUGE Scores (Traditional NLP metrics)**:
   - Built for translation and n-gram overlap.
   - They penalize paraphrasing and fail to measure semantic factual accuracy or reasoning.

---

## 3. The LLM-as-a-Judge Paradigm

DeepEval implements the **LLM-as-a-Judge** pattern:
- Instead of relying on rigid string comparisons, DeepEval sends:
  1. The **input prompt**
  2. The **actual output** from your model
  3. (Optional) The **expected output** or **retrieved knowledge context**
  4. A **metric rubric & algorithmic scoring prompt**
  to an evaluation judge model (e.g., GPT-4o, Claude 3.5, or local Ollama).
- The judge computes a score between `0.0` and `1.0` and provides a **chain-of-thought reason** for why points were deducted.

---

## 4. DeepEval Anatomy: The Core Building Blocks

### A. `LLMTestCase`
The standardized container holding all data about an interaction:
```python
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

test_case = LLMTestCase(
    input="What is your return policy?",
    actual_output="You can return any unworn item within 30 days for a full refund.",
    expected_output="Items can be returned within 30 days for a complete refund.",
    retrieval_context=["Our store allows returns within 30 days of purchase for unworn items."]
)
```

### B. `Metric`
The evaluation algorithm and threshold:
```python
from deepeval.metrics import AnswerRelevancyMetric

# Threshold is the minimum acceptable score (0.0 to 1.0)
metric = AnswerRelevancyMetric(threshold=0.7)
```

### C. `assert_test`
The Pytest-compatible assertion function:
```python
from deepeval import assert_test

# Evaluates test_case against all passed metrics. Raises AssertionError if any fail.
assert_test(test_case, [metric])
```

---

## 5. SDET Key Takeaways

1. DeepEval is built directly on top of `pytest` — your existing knowledge of fixtures, test discovery, markers, and parameterized tests transfers 100%.
2. You run tests using:
   - Standard Pytest: `uv run pytest test_file.py`
   - DeepEval CLI: `uv run deepeval test run test_file.py` (which gives formatted terminal tables and metric breakdown).
3. Every test failure in DeepEval comes with a built-in `reason`, making root-cause analysis fast and straightforward.

---

### Navigation:
- ⬅️ **Previous**: [Module 00: Modern Python Tooling & Package Management with UV](file:///d:/deep-eval-project/learning_notes/00_python_tooling_with_uv.md)
- ➡️ **Next**: [Module 02: Judge Configuration, Framework Setup & Troubleshooting](file:///d:/deep-eval-project/learning_notes/02_judge_configuration_and_framework_setup.md)

