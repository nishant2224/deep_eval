# DeepEval Metrics Master Reference Guide

> A living reference catalog of all LLM evaluation metrics in this framework. This file is continuously updated as new testing modules are added.

---

## 📊 Complete Metrics Overview Table

| # | Metric Name | Category | Required `LLMTestCase` Fields | Question It Answers | Example Failure Mode |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **`AnswerRelevancyMetric`** | Generation (LLM) | `input`, `actual_output` | *"Did the LLM directly answer the user's question without talking about unrelated topics?"* | User asks *"How do I reset my password?"*, and the bot replies with subscription pricing plans. |
| **2** | **`FaithfulnessMetric`** | Generation (LLM) | `input`, `actual_output`, `retrieval_context` | *"Are all factual claims in the answer strictly backed by the retrieved company documents?"* | Policy allows 14-day returns; bot tells the customer they have 60 days and free return shipping. |
| **3** | **`HallucinationMetric`** | Generation (LLM) | `input`, `actual_output`, `context` | *"Did the LLM directly contradict or state untruths against reference facts?"* | Policy states water damage is excluded; bot promises full liquid damage warranty coverage. |
| **4** | **`ContextualRelevancyMetric`** | Retrieval (Search Engine) | `input`, `actual_output`, `retrieval_context` | *"How clean is the retrieved context? Does it contain excessive irrelevant noise or fluff?"* | User asks about holiday store hours; search engine also fetches the corporate cafeteria lunch menu. |
| **5** | **`ContextualRecallMetric`** | Retrieval (Search Engine) | `input`, `actual_output`, `expected_output`, `retrieval_context` | *"Did the search engine retrieve ALL the required facts from the golden ground truth?"* | Golden answer requires 30-day return policy AND 2-year warranty; search engine only fetched the return policy. |
| **6** | **`ContextualPrecisionMetric`** | Retrieval (Search Engine) | `input`, `actual_output`, `expected_output`, `retrieval_context` | *"Are the most relevant chunks ranked at the very top (Rank #1) rather than buried at the bottom?"* | The exact return drop-off address is buried at chunk #5 behind 4 generic packaging sustainability FAQs. |
| **7** | **`GEval` (Custom Rubrics)** | Custom Business Logic | Configured via `evaluation_params` (e.g. `[INPUT, ACTUAL_OUTPUT]`) | *"Does the LLM satisfy custom company Acceptance Criteria (empathy, actionability, brevity, brand voice)?"* | Angry customer complaint receives a cold, defensive reply blaming transit carriers with zero empathy. |

---

## 🔍 Understanding `evaluation_params` & `SingleTurnParams`

In G-Eval, you must explicitly specify which fields the Judge LLM is allowed to inspect:

```python
evaluation_params = [SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT]
```

### Why do we need to specify this?
1. **Controlling the Judge's Focus**: If you are evaluating **Empathy**, the judge only needs to see what the user said (`INPUT`) and how the bot replied (`ACTUAL_OUTPUT`). Giving it documents or ground truth would waste tokens and distract the judge.
2. **Preventing Information Leaks**: If you are evaluating whether the bot answered without looking at secret system prompts or metadata, you restrict the judge's view strictly to what the user experienced.
3. **Optimizing Token Costs**: Sending only the necessary fields keeps API costs low and ensures faster evaluation speed.

### Available Parameters in `SingleTurnParams`:

| Parameter | What It Represents in `LLMTestCase` | When to Include It in `evaluation_params` |
| :--- | :--- | :--- |
| **`SingleTurnParams.INPUT`** | The user's prompt / question. | Almost always. The judge needs context on what was asked. |
| **`SingleTurnParams.ACTUAL_OUTPUT`** | What your LLM / AI application generated. | Almost always. This is the text being graded. |
| **`SingleTurnParams.EXPECTED_OUTPUT`** | The human-curated "Golden" ground-truth answer. | When evaluating **Correctness**, **Completeness**, or **Factual Similarity** against a known standard. |
| **`SingleTurnParams.RETRIEVAL_CONTEXT`** | The list of document snippets fetched from your Vector DB. | When evaluating **Groundedness**, **Context Adherence**, or **Custom RAG extraction**. |
| **`SingleTurnParams.CONTEXT`** | General reference context / ground-truth knowledge. | Similar to retrieval context; used for factual verification. |
| **`SingleTurnParams.TOOLS_CALLED`** | List of tool / API calls made by an AI Agent. | When evaluating **Agent Decision-Making** or tool call accuracy. |

---

## 🛠️ Detailed Metric Deep-Dives

### 1. `AnswerRelevancyMetric`
* **Target**: LLM Generator
* **Threshold**: Typically `0.7` to `0.8` (Scale: 0.0 - 1.0)
* **How It Evaluates**: Extracts statements from `actual_output` and asks if each statement is relevant to the `input`.
* **SDET Action**: If failing, refine system prompt instructions: *"Only answer what is explicitly asked. Do not volunteer promotional or unrelated info."*

---

### 2. `FaithfulnessMetric`
* **Target**: LLM Generator (RAG)
* **Threshold**: Typically `0.8` to `1.0`
* **How It Evaluates**: Breaks `actual_output` into atomic claims; checks if each claim can be logically deduced from `retrieval_context`.
* **SDET Action**: If failing, tune temperature (set `temperature=0.0`) and reinforce prompt: *"Answer ONLY using the provided documents. If the document does not say, state 'I do not have this information'."*

---

### 3. `HallucinationMetric`
* **Target**: LLM Generator
* **Threshold**: Modern DeepEval uses `0.7` to `1.0` (higher = better alignment)
* **How It Evaluates**: Evaluates whether any statement in `actual_output` directly contradicts `context`.
* **SDET Action**: If failing, check for prompt injection or model hallucination on negative constraints.

---

### 4. `ContextualRelevancyMetric`
* **Target**: Vector Database / Search Engine
* **Threshold**: Typically `0.7`
* **How It Evaluates**: Calculates the ratio of relevant sentences to total sentences in `retrieval_context`.
* **SDET Action**: If failing, reduce chunk size during document ingestion or apply similarity threshold filters.

---

### 5. `ContextualRecallMetric`
* **Target**: Vector Database / Search Engine
* **Threshold**: Typically `0.8`
* **How It Evaluates**: Checks what fraction of the `expected_output` facts were successfully retrieved in `retrieval_context`.
* **SDET Action**: If failing, increase `top_k` retrieved documents, improve chunk overlap, or use Hybrid Search (BM25 keyword search + Vector embeddings).

---

### 6. `ContextualPrecisionMetric`
* **Target**: Search Ranking / Reranker
* **Threshold**: Typically `0.7` to `0.8`
* **How It Evaluates**: Rewards relevant documents appearing at Rank #1 and penalizes relevant documents buried at lower ranks.
* **SDET Action**: If failing, add a **Cross-Encoder Reranker** (e.g. Cohere Rerank, BGE Reranker) after the initial vector search.

---

### 7. `GEval` (Custom Business Rubrics)
* **Target**: Custom Business Rules / Brand Voice / SLAs
* **Threshold**: Custom (e.g. `0.75`)
* **How It Evaluates**: Takes natural language `criteria` and `evaluation_steps`, uses Chain-of-Thought (CoT) reasoning, and grades adherence.
* **SDET Action**: Write modular rubrics for Empathy, Actionability, Mobile Conciseness, and PII avoidance.
