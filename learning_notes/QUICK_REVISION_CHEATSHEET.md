# ⚡ SDET Quick Revision Cheat Sheet & Gotchas Guide

> **Purpose**: A high-speed, day-agnostic revision guide for LLM EvalOps & DeepEval testing. Designed for quick 5-minute refreshes, covering core mental models, practical implementation patterns, common traps, and all metric definitions.

---

## 🧠 1. The Core Mental Model

```
Traditional Testing (Selenium / Playwright / API)
┌──────────────┐     deterministic     ┌────────────────────────┐
│  User Action │ ────────────────────> │ assert actual == "OK"  │
└──────────────┘                       └────────────────────────┘

LLM Testing (Generative AI / RAG / Agents)
┌──────────────┐     probabilistic     ┌────────────────────────────────────────┐
│ User Prompt  │ ────────────────────> │ assert judge_metric.score >= threshold │
└──────────────┘                       └────────────────────────────────────────┘
```

* **Traditional QA**: Deterministic. Outputs are binary (`True`/`False`), strings match exactly.
* **GenAI / LLM QA**: Probabilistic. The exact wording changes on every run. We do not assert string equality; we assert **semantic properties** (e.g., faithfulness, relevancy, toxicity, role consistency) using an **LLM-as-a-Judge**.

---

## ⚠️ 2. Crucial Gotchas & FAQ (Things You Asked & Might Struggle With)

### Q1: *"Is the bot in `src/` something an SDET builds or developers build?"*
* **The Bot is the AUT (Application Under Test)**: In a real software company, backend AI developers build the bot (`src/bot.py`).
* **The SDET's Role**: We build the testing framework (`tests/`, metrics, CI/CD pipelines). We created `src/bot.py` here to simulate a real, live RAG microservice so we aren't just testing mock data.

---

### Q2: *"Why did we need `pythonpath = ['.']` and `sys.path.insert(0, str(ROOT_DIR))`?"*
* **The Problem**: When running `pytest` or Python scripts from subdirectories, Python does not automatically look for imports in root project folders. Running `from src.bot import ...` throws `ModuleNotFoundError`.
* **The Fix**:
  * `pyproject.toml` -> `pythonpath = ["."]`: Tells Pytest that the root directory is on Python's search path.
  * `conftest.py` -> `sys.path.insert(0, str(ROOT_DIR))`: Safeguard ensuring standalone script executions and CLI commands always find `src`.

---

### Q3: *"Windows Console Unicode / Emoji Crashes (`charmap` error) — Why did this happen?"*
* **The Trap**: Windows PowerShell defaults to legacy `cp1252` encoding. DeepEval prints Rich terminal tables containing emojis (🎯, ✓, ⚠️). Python throws `UnicodeEncodeError: 'charmap' codec can't encode character`.
* **The Fix** (in `tests/conftest.py`):
  ```python
  import sys
  if sys.platform == "win32":
      sys.stdout.reconfigure(encoding="utf-8")
      sys.stderr.reconfigure(encoding="utf-8")
  ```

---

### Q4: *"Why do we use UV (`uv`) instead of `pip`?"*
* **`uv` is written in Rust**: It installs packages 10–100x faster than pip.
* **Deterministic Lockfiles**: `uv sync` reads `uv.lock`, guaranteeing that everyone on the team (and CI/CD) has the exact same package versions.
* **CLI Quick Commands**:
  * Run tests: `uv run pytest`
  * Add dependency: `uv add <package>`
  * Sync env: `uv sync`

---

### Q5: *"Why the 15 RPM Rate Limit and why `rate_limit_pacer`?"*
* **The Problem**: Google Gemini Free Tier limits requests to 15 Requests Per Minute (RPM). Running a test suite with 5 tests where each test evaluates multiple metrics causes immediate `429 RESOURCE_EXHAUSTED` errors.
* **The Fix**: An autouse session/function fixture in `tests/conftest.py` that sleeps for `3.0` to `4.0` seconds between test executions:
  ```python
  @pytest.fixture(autouse=True)
  def rate_limit_pacer():
      yield
      time.sleep(3.5)
  ```

---

### Q6: *"Is G-Eval just creating our own custom metrics?"*
* **YES, EXACTLY**: G-Eval is a flexible framework inside DeepEval that lets you grade ANY business requirement using natural language.
* **How It Works**:
  1. Define `criteria` (what good looks like in plain English).
  2. Define `evaluation_steps` (step-by-step scoring rubric).
  3. Specify `evaluation_params` (e.g., `[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT]`).
* DeepEval's judge LLM executes Chain-of-Thought (CoT) reasoning and scores from `0.0` to `1.0`.

---

### Q7: *"How do we extract conversational turns from a real chatbot?"*
* **In Live Automation (CI/CD / Staging)**: The Pytest script loops over user prompts, calls `POST /api/chat`, receives the reply, and appends `Turn(role="user", content=...)` and `Turn(role="assistant", content=...)` in real-time.
* **From Production Logs / Observability**: An adapter function queries the session store (Redis / DynamoDB / LangSmith) by `session_id`, maps `CUSTOMER -> user` and `BOT -> assistant`, and returns a `ConversationalTestCase`.

---

### Q8: *"Why did we not put `live_bot` fixture in `conftest.py` immediately?"*
* **SDET Best Practice (YAGNI)**: Fixtures should live close to where they are used. If only one test file (`test_04_live_rag_e2e.py`) queries the live bot, putting it in `conftest.py` prematurely couples the entire test suite to that resource. When multiple test modules need it, promote it to `conftest.py`.

---

### Q9: *"How does `assert_test` work under the hood?"*
* DeepEval's `assert_test(test_case, [metric_1, metric_2])`:
  * Runs the metrics against the test case asynchronously.
  * If ANY metric score is strictly below its `threshold`, it automatically raises `AssertionError: Metrics: <Name> (score: X, threshold: Y, reason: Z) failed`.
  * If all scores meet or exceed threshold, the test passes silently.

---

### Q10: *"If even test cases are generated by Synthesizer, what is the need of a QA?"*
* **The QA Role Evolved (From Typist to Quality Architect)**:
  1. **Auditing the Evaluator**: Synthesizers are LLMs and can hallucinate or generate ambiguous questions. SDETs act as the Human-in-the-Loop arbiter of truth.
  2. **Adversarial & Edge Cases**: Synthesizers only generate polite happy paths from documents. Only an SDET designs prompt injections, jailbreaks, and toxic edge cases.
  3. **Defining Quality Bars**: Deciding acceptable mathematical thresholds (e.g., Faithfulness $\ge 0.70$) and authoring G-Eval business rubrics.
  4. **Root-Cause Triage**: When tests fail, determining whether the bug is in the Vector DB (chunking), the Generator LLM (temperature/prompt), or stale benchmark data.
  5. **Platform Automation**: Building CI/CD quality gates, data pipelines, and test harnesses.

---

### Q11: *"Why use `next(...)` with a generator instead of a list index or loop?"*
* **The Fragility of Indexing**: Writing `goldens[2]` breaks whenever dataset order changes.
* **The Verbosity of Loops**: A 5-line `for` loop with `if` and `break` clutters tests.
* **The Pythonic Solution**: `next(g for g in goldens if "shipping" in g["input"].lower())` executes lazily, returns the first matching item immediately, and stops searching.

---

### Q12: *"How does `@pytest.mark.parametrize` work with dynamic `ids`?"*
* **The Engine**: `@pytest.mark.parametrize("param_name", dataset, ids=[...])` loops through the dataset and executes the test function once per row.
* **Dynamic IDs**: Passing readable strings (e.g. extracted query words) in `ids` labels each test in terminal logs and reports (e.g. `test_regression[What_does_warranty_cover]`), enabling targeted execution via `pytest -k "warranty"`.

---

### Q13: *"Does this framework depend on GitHub Actions, or can it run in Jenkins?"*
* **100% CI-Agnostic**: Test automation frameworks should never be coupled to a specific CI vendor.
* **In Jenkins**: You use a standard `Jenkinsfile` with Declarative Groovy syntax:
  * Pulls API keys from Jenkins Credential Store (`credentials('gemini-key')`).
  * Restores packages in seconds via `sh 'uv sync --frozen'`.
  * Executes `uv run pytest --junitxml=reports/junit.xml`.
  * The native Jenkins **JUnit Plugin** parses `junit.xml` and renders pass/fail curves, duration graphs, and failure tables automatically.

---

## 🗺️ 3. Quick Decision Guide: Which Test Structure to Use?

| What Are You Testing? | Test Case Class | Key Metrics |
| :--- | :--- | :--- |
| Single Q&A without documents | `LLMTestCase(input, actual_output)` | `AnswerRelevancyMetric` |
| RAG Hallucination / Factuality | `LLMTestCase(input, actual_output, retrieval_context)` | `FaithfulnessMetric`, `HallucinationMetric` |
| RAG Vector DB Search Quality | `LLMTestCase(input, actual_output, expected_output, retrieval_context)` | `ContextualPrecisionMetric`, `ContextualRecallMetric`, `ContextualRelevancyMetric` |
| Custom Brand / SLA Rubrics | `LLMTestCase(input, actual_output)` | `GEval(name, criteria, evaluation_steps)` |
| Safety, Harassment, Stereotypes | `LLMTestCase(input, actual_output)` | `ToxicityMetric`, `BiasMetric` |
| Multi-turn Chat / AI Persona | `ConversationalTestCase(turns, chatbot_role)` | `RoleAdherenceMetric`, `ConversationCompletenessMetric` |

---

## 🔮 4. Modular Deep-Dives & Advanced Pipelines

### Day 8: Synthetic Golden Dataset Generation (`Synthesizer`)
* **The Problem**: Writing 300+ ground truth `(input, expected_output, context)` pairs manually takes weeks and introduces human bias.
* **The Solution**: DeepEval's `Synthesizer` uses an LLM to reverse-engineer realistic customer questions and ground-truth answers directly from raw context chunks.
* **Key Functionality**:
  ```python
  from deepeval.synthesizer import Synthesizer
  synthesizer = Synthesizer()
  goldens = synthesizer.generate_goldens_from_contexts(
      contexts=[[chunk_text]],
      max_goldens_per_context=1,
      include_expected_output=True
  )
  synthesizer.save_as(file_type="json", directory="data", file_name="synthetic_goldens")
  ```
* **SDET Golden Rule**: Always serialize and commit your generated goldens to `data/` as static JSON. Never regenerate goldens on every CI/CD run—use the static JSON as the regression benchmark to conserve tokens and maintain determinism.

---

### Day 9: SDET Framework Architecture & CI/CD Quality Gates
* **The Problem**: Running ad-hoc single tests doesn't scale to production regression testing or PR gating.
* **The Solution**: 
  1. **Data-Driven Testing (DDT)**: Use `@pytest.mark.parametrize` over your benchmark dataset (`data/synthetic_goldens.json`) with dynamic, descriptive `ids`.
  2. **Hard Quality Gates**: Block deployment in CI if any critical metric (Faithfulness, Relevancy, Toxicity) falls below threshold.
  3. **Enterprise Jenkins CI (`Jenkinsfile`)**:
     * Installs dependencies in $< 3\text{s}$ via Astral `uv` (`sh 'uv sync --frozen'`).
     * Injects credentials securely via Jenkins Credential Store (`credentials('google-gemini-api-key')`).
     * Exports and visualizes JUnit XML reports via native Jenkins JUnit plugin (`junit 'reports/junit.xml'`).
* **CI/CD Flakiness Gotcha**: Free-tier APIs enforce strict rate limits (15 RPM). In CI, multiple metrics evaluated across parameterized tests will trigger `429 RESOURCE_EXHAUSTED` unless paced with a fixture (`time.sleep(8.0)` in `rate_limit_pacer`).

---

### Day 10: Portfolio Packaging & Resume Highlights
* **Core Concept**: Integrating with Confident AI cloud telemetry dashboards and translating this framework into 5 high-impact SDET resume bullet points.
* *(Future questions & notes from Day 10 will be appended here)*

---

## 📊 5. Master DeepEval Metrics Reference Table

| # | Metric Name | Category | Required Test Case Fields | Question It Answers | Example Failure Mode |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **`AnswerRelevancyMetric`** | Generation (LLM) | `input`, `actual_output` | *"Did the LLM directly answer the user's question without talking about unrelated topics?"* | User asks *"How do I reset my password?"*, and the bot replies with subscription pricing plans. |
| **2** | **`FaithfulnessMetric`** | Generation (LLM) | `input`, `actual_output`, `retrieval_context` | *"Are all factual claims in the answer strictly backed by the retrieved company documents?"* | Policy allows 14-day returns; bot tells the customer they have 60 days and free return shipping. |
| **3** | **`HallucinationMetric`** | Generation (LLM) | `input`, `actual_output`, `context` | *"Did the LLM directly contradict or state untruths against reference facts?"* | Policy states water damage is excluded; bot promises full liquid damage warranty coverage. |
| **4** | **`ContextualRelevancyMetric`** | Retrieval (Search Engine) | `input`, `actual_output`, `retrieval_context` | *"How clean is the retrieved context? Does it contain excessive irrelevant noise or fluff?"* | User asks about holiday store hours; search engine also fetches the corporate cafeteria lunch menu. |
| **5** | **`ContextualRecallMetric`** | Retrieval (Search Engine) | `input`, `actual_output`, `expected_output`, `retrieval_context` | *"Did the search engine retrieve ALL the required facts from the golden ground truth?"* | Golden answer requires 30-day return policy AND 2-year warranty; search engine only fetched the return policy. |
| **6** | **`ContextualPrecisionMetric`** | Retrieval (Search Engine) | `input`, `actual_output`, `expected_output`, `retrieval_context` | *"Are the most relevant chunks ranked at the very top (Rank #1) rather than buried at the bottom?"* | The exact return drop-off address is buried at chunk #5 behind 4 generic packaging sustainability FAQs. |
| **7** | **`GEval` (Custom Rubrics)** | Custom Business Logic | Configured via `evaluation_params` (e.g. `[INPUT, ACTUAL_OUTPUT]`) | *"Does the LLM satisfy custom company Acceptance Criteria (empathy, actionability, brevity, brand voice)?"* | Angry customer complaint receives a cold, defensive reply blaming transit carriers with zero empathy. |
| **8** | **`ToxicityMetric`** | Safety & Red-Teaming | `input`, `actual_output` | *"Is the output free from profanity, hate speech, aggression, harassment, and personal attacks?"* | Customer vents about a delay, and the bot responds with insults or hostile defensive remarks. |
| **9** | **`BiasMetric`** | Safety & Red-Teaming | `input`, `actual_output` | *"Is the output objective and free from gender, racial, age, religious, or socioeconomic stereotyping?"* | Bot suggests that male applicants are naturally better suited for engineering roles than female applicants. |
| **10** | **`RoleAdherenceMetric`** | Conversational / Multi-Turn | `ConversationalTestCase(turns, chatbot_role)` | *"Does the bot consistently adhere to its assigned persona/role throughout all dialogue turns?"* | Support bot breaks character when insulted, using rude slang or claiming to be an unrestricted AI model. |
| **11** | **`ConversationCompletenessMetric`** | Conversational / Multi-Turn | `ConversationalTestCase(turns)` | *"Did the multi-turn interaction fully resolve the user's inquiry or leave tasks unfinished?"* | Bot prematurely closes the support ticket without answering the customer's follow-up question. |
