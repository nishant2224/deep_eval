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

---

## 3. Real-World Positive & Negative Scenarios

### A. ContextualRelevancyMetric (Noise & Bloat Detection)
* **Goal**: Measure whether the search engine retrieved focused paragraphs or stuffed the prompt with useless junk.
* **User Prompt**: *"What are your store hours on Christmas Day?"*

* **✅ Positive Scenario (PASS - Score 1.0)**:
  * **Retrieved Chunks**:
    * Chunk 1: *"Holiday Schedule: Retail stores are closed on Christmas Day (December 25th) and Thanksgiving Day."*
  * **Why it passes**: 100% of the retrieved text directly addresses Christmas Day hours. Minimal token waste.

* **❌ Negative Scenario (FAIL - Score 0.25)**:
  * **Retrieved Chunks**:
    * Chunk 1: *"Our company was founded in 2012 by two college roommates."* *(Junk)*
    * Chunk 2: *"The corporate cafeteria serves breakfast from 8 AM to 10 AM."* *(Junk)*
    * Chunk 3: *"Job openings in logistics are posted every Monday."* *(Junk)*
    * Chunk 4: *"Stores are closed on Christmas Day."* *(The only useful sentence)*
  * **Why it fails**: 75% of the retrieved text is irrelevant noise.

---

### B. ContextualRecallMetric (Completeness of Retrieved Facts)
* **Goal**: Measure whether the search engine retrieved *every* required fact from the golden expected output.
* **User Prompt**: *"How do I qualify for the Student Discount?"*
* **Golden Ground Truth (`expected_output`)**:
  > *"To qualify, you must have an active `.edu` email address AND upload a copy of your valid student ID card."*

* **✅ Positive Scenario (PASS - Score 1.0)**:
  * **Retrieved Chunks**:
    * Chunk 1: *"Student discounts require signing up with a verified `.edu` email address."*
    * Chunk 2: *"Applicants must upload a photo of their current semester student ID."*
  * **Why it passes**: Both conditions from the ground-truth answer were retrieved. 100% recall.

* **❌ Negative Scenario (FAIL - Score 0.5)**:
  * **Retrieved Chunks**:
    * Chunk 1: *"Student discounts require signing up with a verified `.edu` email address."*
    *(Search engine completely missed Chunk 2 about the Student ID card!)*
  * **Why it fails**: The retriever missed half of the required facts, forcing the LLM to give an incomplete answer.

---

### C. ContextualPrecisionMetric (Ranking Quality & "Lost in the Middle")
* **Goal**: Measure whether the most directly useful chunk was placed at the top (Rank #1) rather than buried at the bottom.
* **User Prompt**: *"Where do I drop off my return package?"*
* **Golden Ground Truth (`expected_output`)**:
  > *"You must drop off returns at any authorized UPS Store or FedEx Dropbox."*

* **✅ Positive Scenario (PASS - Score 1.0)**:
  * **Rank #1 Chunk**: *"Drop-off locations: Return packages must be handed over at any authorized UPS Store or FedEx Dropbox."*
  * **Rank #2 Chunk**: *"Make sure the return barcode label is affixed to the outside of the box."*
  * **Rank #3 Chunk**: *"Packages typically take 3 to 5 business days to reach our warehouse."*
  * **Why it passes**: The direct answer is at Rank #1. The LLM sees it immediately.

* **❌ Negative Scenario (FAIL - Score 0.3)**:
  * **Rank #1 Chunk**: *"Our packaging uses 100% recycled biodegradable cardboard."*
  * **Rank #2 Chunk**: *"Shipping carrier rates are subject to annual adjustments."*
  * **Rank #3 Chunk**: *"Return packages must be dropped off at any authorized UPS Store or FedEx Dropbox."*
  * **Why it fails**: The direct answer was buried at Rank #3. Because of the **"Lost in the Middle"** phenomenon, LLMs frequently overlook information placed at the bottom of long context windows.

---

## 4. The SDET Diagnostic Matrix: Which Metric When?

| What broke in your AI Application? | Who is at fault? | Metric to Add to Pytest |
| :--- | :--- | :--- |
| Bot promised the user a $50 discount that doesn't exist. | **The LLM** (Hallucination) | `FaithfulnessMetric` |
| Bot told the user the store is open 24/7 when the policy says 9 AM - 9 PM. | **The LLM** (Direct Contradiction) | `HallucinationMetric` |
| Vector search is fetching 10 pages of unrelated text for every simple question. | **The Retriever** (Noisy Search) | `ContextualRelevancyMetric` |
| Bot gave a half-complete answer because search missed the second document. | **The Retriever** (Incomplete Search) | `ContextualRecallMetric` |
| The search found the right document, but ranked it at #5 behind 4 generic FAQs. | **The Retriever** (Bad Ranking Order) | `ContextualPrecisionMetric` |

---

## 5. Summary Comparison Table

| Metric | Testing Target | What a Low Score Indicates | SDET Fix Recommendation |
| :--- | :--- | :--- | :--- |
| **`ContextualRelevancy`** | Noise & Fluff | Context contains irrelevant pages/paragraphs. | Reduce chunk size, filter out irrelevant metadata. |
| **`ContextualRecall`** | Completeness | Context is missing critical paragraphs needed to answer. | Increase `top_k`, improve embedding model or hybrid search (BM25 + Vector). |
| **`ContextualPrecision`** | Ranking Order | Important documents are buried at the bottom of the list. | Add a **Reranker** (e.g. Cohere Rerank / BGE Cross-Encoder). |


---

## 6. Pytest Implementation Blueprint

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
