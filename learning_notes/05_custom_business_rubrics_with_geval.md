# Module 05: Custom Business Rubrics with G-Eval

## 1. Why Pre-Built Metrics Are Not Enough

Standard RAG metrics (`Faithfulness`, `AnswerRelevancy`, `ContextualRecall`) only test the generic mechanics of information retrieval and generation.

However, in enterprise products, your Product Managers (PMs) and QA Leads write **Acceptance Criteria (AC)** tailored to your specific business:
- *"Does the customer support bot apologize with empathy when an order is delayed?"*
- *"Does the banking bot provide clear, actionable next steps instead of vague advice?"*
- *"Does the response maintain an executive, concise tone suitable for mobile notifications?"*
- *"Does the bot avoid making binding financial or legal promises?"*

None of these can be tested with static strings or standard RAG metrics. This is where **G-Eval** becomes the most important tool in an SDET's arsenal.

---

## 2. What is G-Eval?

**G-Eval** is a framework developed by researchers (and implemented in DeepEval) that allows you to construct **custom, rubric-based evaluation metrics using natural language**.

Instead of writing rigid Python code for every test case, you define:
1. **`criteria`**: A description of what high quality looks like.
2. **`evaluation_steps`**: A clear step-by-step grading rubric that the judge model follows.
3. **`evaluation_params`**: Which parts of the interaction to inspect (e.g. `SingleTurnParams.INPUT`, `SingleTurnParams.ACTUAL_OUTPUT`).

Under the hood, DeepEval sends the rubric to the judge model, which performs **Chain-of-Thought (CoT)** reasoning, generates a score between `0.0` and `1.0`, and outputs an itemized deduction explanation.

---

## 3. Anatomy of a Custom `GEval` Metric

```python
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams

professionalism_metric = GEval(
    name="Customer Empathy & Professionalism",
    criteria="Determine if the bot demonstrates genuine empathy and professionalism when handling customer complaints.",
    evaluation_steps=[
        "Check if the response acknowledges the customer's frustration or inconvenience.",
        "Check if the tone remains polite, calm, and respectful without defensive language.",
        "Check if the bot offers a concrete resolution or clear next steps to help.",
        "Deduct points if the tone is cold, dismissive, or robotic."
    ],
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    threshold=0.75
)
```

---

## 4. Real-World Positive & Negative Scenarios

### Scenario A: Customer Support Empathy & Tone
* **Customer Prompt**: *"My package was supposed to arrive yesterday for my daughter's birthday and it's still missing! This is completely unacceptable!"*

* **✅ Positive Scenario (PASS - Score 0.95)**:
  * **LLM Output**: *"I am so sorry to hear that your package hasn't arrived, especially for such an important occasion as your daughter's birthday! I completely understand how frustrating this is. Let me look into this immediately—could you please confirm your tracking number so I can expedite a replacement or issue a refund?"*
  * **Judge Assessment**: Fully acknowledges frustration, shows personal empathy, avoids defensiveness, and provides immediate next steps.

* **❌ Negative Scenario (FAIL - Score 0.20)**:
  * **LLM Output**: *"Packages are subject to carrier delays. Check the tracking link provided in your email confirmation. We are not responsible for transit times."*
  * **Judge Assessment**: Cold, defensive, ignores the emotional context, and fails to offer help. Fails threshold.

---

### Scenario B: Actionability & Next Steps
* **Goal**: Ensure the bot provides concrete actions (links, phone numbers, or ticket creation) rather than vague advice.
* **Customer Prompt**: *"I lost my corporate laptop at the airport. What do I do right now?"*

* **✅ Positive Scenario (PASS - Score 1.0)**:
  * **LLM Output**: *"Immediately call IT Security Hotline at 1-800-555-0199 so we can remotely lock your device. Next, file an incident report at security.internal.com/lost-device within 2 hours."*
  * **Judge Assessment**: Provides exact phone number, concrete portal link, and a strict timeline.

* **❌ Negative Scenario (FAIL - Score 0.3)**:
  * **LLM Output**: *"Losing a laptop is serious. You should probably tell your manager or find someone in IT to help you lock it."*
  * **Judge Assessment**: Lacks concrete phone numbers, portal links, or urgent actionable steps.

---

## 5. When to Choose G-Eval vs. Pre-Built Metrics

| Requirement | Use Standard DeepEval Metric | Use G-Eval Metric |
| :--- | :--- | :--- |
| Checking if retrieved docs match prompt | `ContextualRelevancyMetric` | ❌ |
| Checking if LLM output sticks to context | `FaithfulnessMetric` | ❌ |
| Verifying brand guidelines / tone of voice | ❌ | `GEval` (Custom Tone Rubric) |
| Enforcing legal disclaimer requirements | ❌ | `GEval` (Compliance Rubric) |
| Rating code explanations or technical clarity | ❌ | `GEval` (Technical Clarity Rubric) |
| Ensuring mobile UI brevity (< 3 sentences) | ❌ | `GEval` (Conciseness Rubric) |

---

### Navigation:
- ⬅️ **Previous**: [Module 04: RAG Evaluation Part 2 — Context Retrieval Triad](file:///d:/deep-eval-project/learning_notes/04_rag_context_retrieval_triad.md)
- ➡️ **Next (Day 5)**: Module 06: LLM Safety, Guardrails & Red-Teaming (Toxicity, Bias, Prompt Injection)
