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

## 3. Real-World Positive & Negative Scenarios

### A. FaithfulnessMetric (Inventing Unsupported Claims)
* **Goal**: Verify if the LLM invents perks, rules, or features absent from company documents.

* **Retrieved Knowledge Context**:
  > *"Customers can return items within 30 days of purchase for a full refund if the item is unopened and in its original box."*

* **✅ Positive Scenario (PASS - Score 1.0)**:
  * **User Prompt**: *"Can I return my item?"*
  * **LLM Output**: *"Yes, you can return your item within 30 days of purchase as long as it remains unopened and in the original packaging."*
  * **Why it passes**: Every single statement is 100% grounded in the retrieved documentation.

* **❌ Negative Scenario (FAIL - Score 0.4)**:
  * **User Prompt**: *"Can I return my item?"*
  * **LLM Output**: *"Yes! You can return it within 30 days. Plus, we provide **free return shipping labels** and **90 days of free tech support**!"*
  * **Why it fails**: The LLM hallucinated free return shipping and 90 days of tech support out of thin air. In enterprise systems, this causes real financial and customer trust damage.

---

### B. HallucinationMetric (Direct Contradictions & Untruths)
* **Goal**: Verify if the LLM states falsehoods directly contradicting policy.

* **Retrieved Knowledge Context**:
  > *"Water damage is strictly excluded from the standard 1-year warranty coverage."*

* **✅ Positive Scenario (PASS - Score 1.0)**:
  * **User Prompt**: *"Does my warranty cover dropping my phone in a swimming pool?"*
  * **LLM Output**: *"No, water damage is strictly excluded under the standard 1-year warranty."*
  * **Why it passes**: Perfectly aligns with company documentation.

* **❌ Negative Scenario (FAIL - Score 0.0)**:
  * **User Prompt**: *"Does my warranty cover dropping my phone in a swimming pool?"*
  * **LLM Output**: *"Yes, our comprehensive 1-year warranty covers all accidental liquid and water damage."*
  * **Why it fails**: Directly contradicts the clear policy restriction.


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
