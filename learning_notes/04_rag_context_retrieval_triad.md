# Module 04: RAG Evaluation Part 2 — The Context Retrieval Triad

## 1. Why Test the Retriever? (Garbage In = Garbage Out)

In Day 2, we tested the **Generation Layer** (Did the LLM stick to the provided context?).

In Day 3, we test the **Retrieval Layer** (Did our search engine / Vector Database retrieve the right documents?).

> **The Golden Rule of RAG**:  
> Even the smartest LLM in the world will produce a wrong or incomplete answer if your search engine hands it irrelevant noise, incomplete paragraphs, or misranked documents.

---

## 2. The Context Triad Explained

DeepEval evaluates the retrieval pipeline using three complementary metrics known as the **Context Triad**:

```
                         ┌─────────────────────────────────┐
                         │   THE RAG CONTEXT TRIAD         │
                         └────────────────┬────────────────┘
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         ▼                                ▼                                ▼
1. Contextual Relevancy          2. Contextual Recall            3. Contextual Precision
   "Is there too much               "Did we miss any                "Are the best docs
     irrelevant noise?"               critical facts?"                 ranked at the top?"
```

---

### A. Contextual Relevancy (`ContextualRelevancyMetric`)

* **What it asks**: *"How much fluff or irrelevant text was retrieved?"*
* **Why it matters**: 
  - Irrelevant context wastes money (higher token costs).
  - Bloated context confuses the LLM, leading to hallucinations.
* **Calculation**:
  $$\text{Contextual Relevancy} = \frac{\text{Number of Relevant Sentences in Context}}{\text{Total Sentences in Context}}$$
* **Required Test Case Fields**: `input`, `actual_output`, `retrieval_context`.

---

### B. Contextual Recall (`ContextualRecallMetric`)

* **What it asks**: *"Did the search engine retrieve ALL the facts required to answer the question completely?"*
* **Why it matters**: 
  - If a user asks *"What are the refund terms for shoes and electronics?"*, but the search engine only retrieves the shoe policy, the LLM will miss the electronics part.
* **Calculation**: DeepEval compares the `retrieval_context` against your **`expected_output`** (the golden ground truth answer).
  $$\text{Contextual Recall} = \frac{\text{Number of Claims in Expected Output Attributed to Context}}{\text{Total Claims in Expected Output}}$$
* **Required Test Case Fields**: `input`, `actual_output`, `expected_output`, `retrieval_context`.

---

### C. Contextual Precision (`ContextualPrecisionMetric`)

* **What it asks**: *"Are the most relevant chunks positioned at the top of the search results?"*
* **Why it matters (The "Lost in the Middle" Phenomenon)**:
  - Research shows that LLMs pay the most attention to text at the **very beginning** and **very end** of their prompt.
  - If your retriever fetches 5 documents and the critical answer is buried at Rank #3 or #4, the LLM will often ignore it.
  - A high Contextual Precision score ensures your retriever ranks the most important documents at Rank #1.
* **Calculation**: Weighted Precision score rewarding relevant chunks appearing higher up in the `retrieval_context` list.
* **Required Test Case Fields**: `input`, `actual_output`, `expected_output`, `retrieval_context`.

---

## 3. Summary Comparison Table

| Metric | Testing Target | What a Low Score Indicates | SDET Fix Recommendation |
| :--- | :--- | :--- | :--- |
| **`ContextualRelevancy`** | Noise & Fluff | Context contains irrelevant pages/paragraphs. | Reduce chunk size, filter out irrelevant metadata. |
| **`ContextualRecall`** | Completeness | Context is missing critical paragraphs needed to answer. | Increase `top_k`, improve embedding model or hybrid search (BM25 + Vector). |
| **`ContextualPrecision`** | Ranking Order | Important documents are buried at the bottom of the list. | Add a **Reranker** (e.g. Cohere Rerank / BGE Cross-Encoder). |

---

## 4. Pytest Implementation Blueprint

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
)

def test_retrieval_pipeline_quality():
    test_case = LLMTestCase(
        input="What is the employee travel reimbursement policy?",
        actual_output="Employees can claim up to $75 daily for meals and must submit receipts within 30 days.",
        expected_output="Employees are reimbursed up to $75 per day for meals and must submit all receipts within 30 days of travel.",
        retrieval_context=[
            "Meal expenses are reimbursable up to $75 per day during business travel.",
            "All travel expense claims and receipts must be submitted within 30 days of trip completion.",
            "Office supplies must be ordered via the procurement portal." # Irrelevant noise
        ]
    )

    metrics = [
        ContextualRelevancyMetric(threshold=0.7),
        ContextualRecallMetric(threshold=0.8),
        ContextualPrecisionMetric(threshold=0.8),
    ]

    assert_test(test_case, metrics)
```

---

### Navigation:
- ⬅️ **Previous**: [Module 03: RAG Evaluation Part 1 — Faithfulness & Hallucination](file:///d:/deep-eval-project/learning_notes/03_rag_faithfulness_and_hallucination.md)
- ➡️ **Next (Day 4)**: Module 05: Custom Business Rubrics with G-Eval
