# Module 03: RAG Evaluation Part 1 — Faithfulness & Hallucination Detection

## 1. What is RAG & Why Must SDETs Test It?

**RAG (Retrieval-Augmented Generation)** is the industry-standard architecture for enterprise AI applications. Instead of training an LLM on private company data, RAG works in two stages:
1. **Retrieve**: When a user asks a question, a search engine (usually a Vector Database) fetches relevant snippets from internal documents (`retrieval_context`).
2. **Generate**: The LLM reads the retrieved context and answers the user's question based strictly on those documents.

### The RAG Testing Challenge for SDETs
In traditional API testing, you test whether an endpoint returns the right database record. In RAG testing, you must verify:
* Did the LLM answer **strictly using the retrieved documents**?
* Did the LLM **hallucinate** extra information from its pre-trained public memory that is NOT in your company documents?

---

## 2. Faithfulness vs. Hallucination in DeepEval

DeepEval provides two complementary metrics to catch hallucinations:

| Metric | What It Measures | Required `LLMTestCase` Fields | Pass/Fail Logic |
| :--- | :--- | :--- | :--- |
| **`FaithfulnessMetric`** | Measures if all claims made in the `actual_output` can be directly inferred from the `retrieval_context`. | `input`, `actual_output`, `retrieval_context` | Score $\in [0.0, 1.0]$. Higher is better. Fails if `< threshold` (e.g., 0.7). |
| **`HallucinationMetric`** | Measures if the `actual_output` contradicts or contains fabrications outside the `contexts`. | `input`, `actual_output`, `contexts` | Score $\in [0.0, 1.0]$. Lower is better (0.0 means 0% hallucination). Fails if `> threshold`. |

### How `FaithfulnessMetric` Calculates Scores Under the Hood:
1. **Extract Claims**: The judge LLM extracts every individual factual claim from the `actual_output`.
2. **Verify Against Context**: The judge checks each claim one by one against the provided `retrieval_context`.
3. **Compute Score**:
   $$\text{Faithfulness Score} = \frac{\text{Number of Faithful Claims}}{\text{Total Claims Made}}$$
4. **Generate Chain-of-Thought Reason**: If points are deducted, DeepEval lists the exact unfaithful claims in `metric.reason`.

---

## 3. Real-World Enterprise Example

Suppose you are testing an internal HR Support Bot:

### Retrieved Company Knowledge (`retrieval_context`):
> *"Employees receive 20 days of paid annual leave. Sick leave is accrued at 1 day per month worked. Unused annual leave expires on December 31st and cannot be rolled over."*

### Scenario 1: 100% Faithful Output (Pass)
* **Actual Output**: *"You get 20 days of paid annual leave each year, and sick leave accumulates at 1 day per month. Any unused annual leave expires on December 31st."*
* **Evaluation**: All claims are explicitly backed by the context. Score = `1.0`.

### Scenario 2: Hallucination / Unfaithful Output (Fail)
* **Actual Output**: *"You get 20 days of paid annual leave and 1 day of sick leave per month. You can also roll over up to 5 unused leave days into the next calendar year."*
* **Evaluation**: The rollover claim directly contradicts and invents policy details not present in the context.
* **DeepEval Score**: `0.66` (Fail).
* **DeepEval Reason**: *"The claim that employees can roll over up to 5 days contradicts the context which states unused leave cannot be rolled over."*

---

## 4. DeepEval Test Implementation Pattern

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric

def test_hr_bot_faithfulness():
    metric = FaithfulnessMetric(threshold=0.8)
    
    test_case = LLMTestCase(
        input="Can I roll over unused leave to next year?",
        actual_output="No, unused annual leave expires on December 31st and cannot be rolled over.",
        retrieval_context=[
            "Employees receive 20 days of paid annual leave.",
            "Unused annual leave expires on December 31st and cannot be rolled over."
        ]
    )
    
    assert_test(test_case, [metric])
```

---

### Navigation:
- ⬅️ **Previous**: [Module 02: Judge Configuration, Framework Setup & Troubleshooting](file:///d:/deep-eval-project/learning_notes/02_judge_configuration_and_framework_setup.md)
- ➡️ **Next (Day 3)**: Module 04: RAG Evaluation Part 2 — Context Triad (Precision, Recall & Relevancy)
