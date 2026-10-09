# Enterprise LLM-EvalOps & Quality Assurance Framework

> Automated Evaluation, Safety Guardrails, and Regression Testing for RAG & AI Agent Systems using **DeepEval**, **Pytest**, and **UV**.

---

## 🎯 Overview

As generative AI and Retrieval-Augmented Generation (RAG) applications move into production, standard deterministic test assertions (`assert actual == expected`) fail to measure quality, correctness, and safety.

This repository provides an enterprise-grade automated testing framework implementing **LLM-as-a-Judge** scoring rubrics, RAG triad metrics, and CI/CD quality gates.

---

## 🛠️ Tech Stack

- **Framework**: [DeepEval](https://github.com/confident-ai/deepeval)
- **Test Runner**: [Pytest](https://docs.pytest.org/)
- **Package & Project Manager**: [UV (Astral)](https://github.com/astral-sh/uv)
- **Default Judge Model**: Google Gemini (`gemini-3.5-flash-lite` / `gemini-3.8-flash`) *(supports OpenAI, Azure, and Ollama)*
- **Language**: Python 3.12+

---

## 📁 Repository Structure

```
deep-eval-project/
├── data/                               # 📦 Synthetic Datasets & Golden Benchmarks
│   └── synthetic_goldens.json          # Synthesized ground-truth test cases
├── scripts/                            # ⚙️ Offline utility & generation scripts
│   └── generate_goldens.py             # Synthesizer script for store policies
├── src/                                # 🚀 Application Under Test (AUT)
│   ├── knowledge_base/store_policies.json # Corporate knowledge base
│   └── bot.py                          # CustomerSupportRAGBot implementation
├── tests/                              # Pytest test suites
│   ├── conftest.py                     # Global fixtures, rate limiter & .env loader
│   ├── test_00_smoke.py                # Answer Relevancy smoke tests
│   ├── test_01_rag_faithfulness.py     # Faithfulness & Hallucination
│   ├── test_02_rag_context_triad.py    # Context Retrieval Triad
│   ├── test_03_custom_geval.py         # Custom Business Rubrics (G-Eval)
│   ├── test_04_live_rag_e2e.py         # Live End-to-End RAG Testing
│   ├── test_05_safety_and_red_team.py  # Safety, Bias & Adversarial Red-Teaming
│   ├── test_06_conversational_e2e.py   # Multi-Turn Conversational & Role Adherence
│   ├── test_07_synthetic_goldens_e2e.py # Live Evaluation against Synthetic Goldens
│   └── test_08_dataset_parametrized_regression.py # Parameterized Golden Regressions
├── pyproject.toml                      # Modern Python project manifest (PEP 621)
├── uv.lock                             # Deterministic dependency lockfile
├── .env.example                        # Template for environment secrets
└── .gitignore                          # Protected secrets and cache excludes
```

---

## 🚀 Quickstart

### 1. Prerequisites
Ensure you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

### 2. Setup Environment
```powershell
# Clone the repository
git clone <your-repo-url>
cd deep-eval-project

# Sync dependencies into an isolated virtual environment
uv sync
```

### 3. Configure API Credentials
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Add your free Google Gemini API key:
```env
USE_GEMINI_MODEL="Y"
GEMINI_MODEL_NAME="gemini-3.5-flash-lite"
GOOGLE_API_KEY=AIzaSy...
```

### 4. Run the Test Suites
```powershell
# Run using DeepEval CLI (with detailed terminal tables & score reasons)
uv run deepeval test run tests/test_00_smoke.py

# Or run using standard Pytest
uv run pytest
```

---

## 🧪 Evaluation Test Suites & Coverage Matrix

| Test Suite | Evaluation Focus | Primary Metrics / Techniques |
| :--- | :--- | :--- |
| [`test_00_smoke.py`](file:///d:/deep-eval-project/tests/test_00_smoke.py) | Foundations & Smoke Tests | `AnswerRelevancyMetric` |
| [`test_01_rag_faithfulness.py`](file:///d:/deep-eval-project/tests/test_01_rag_faithfulness.py) | RAG Pipeline Grounding & Factuality | `FaithfulnessMetric`, `HallucinationMetric` |
| [`test_02_rag_context_triad.py`](file:///d:/deep-eval-project/tests/test_02_rag_context_triad.py) | Vector DB Retrieval Quality (The Triad) | `ContextualPrecisionMetric`, `ContextualRecallMetric`, `ContextualRelevancyMetric` |
| [`test_03_custom_geval.py`](file:///d:/deep-eval-project/tests/test_03_custom_geval.py) | Custom Business Rubrics (G-Eval) | `GEval` (Empathy, Actionability with Chain-of-Thought scoring) |
| [`test_04_live_rag_e2e.py`](file:///d:/deep-eval-project/tests/test_04_live_rag_e2e.py) | Live Application Under Test (AUT) | End-to-End evaluation of live `CustomerSupportRAGBot` against Gemini |
| [`test_05_safety_and_red_team.py`](file:///d:/deep-eval-project/tests/test_05_safety_and_red_team.py) | Safety & Adversarial Red-Teaming | `ToxicityMetric`, `BiasMetric`, Prompt Injection & Jailbreak Defense |
| [`test_06_conversational_e2e.py`](file:///d:/deep-eval-project/tests/test_06_conversational_e2e.py) | Multi-Turn Conversational & Agent Flows | `ConversationalTestCase`, `RoleAdherenceMetric`, `ConversationCompletenessMetric` |
| [`test_07_synthetic_goldens_e2e.py`](file:///d:/deep-eval-project/tests/test_07_synthetic_goldens_e2e.py) | Synthetic Benchmarking | Auto-generated Goldens via `Synthesizer`, tested against live SUT |
| [`test_08_dataset_parametrized_regression.py`](file:///d:/deep-eval-project/tests/test_08_dataset_parametrized_regression.py) | Automated Regression & Quality Gates | Data-Driven Testing (`@pytest.mark.parametrize`), Jenkins CI Quality Gates |

---

## 💼 SDET Resume Highlights & Key Achievements

* **Architected an enterprise-grade LLM-EvalOps testing framework** using **DeepEval**, **Pytest**, and **Astral UV**, replacing non-deterministic manual testing with automated **LLM-as-a-Judge** scoring across RAG and conversational AI pipelines.
* **Automated RAG evaluation covering the complete RAG Triad** (Contextual Relevancy, Recall, and Precision) and generation factuality (Faithfulness and Hallucination), preventing hallucinations and ensuring $100\%$ grounding against enterprise knowledge bases.
* **Engineered custom G-Eval business rubrics** (Empathy, Actionability) and **adversarial safety guardrails** (Toxicity, Bias, Prompt Injection / Jailbreak defense), establishing strict pass/fail quality gates that caught $100\%$ of simulated system-prompt leak attempts.
* **Implemented multi-turn conversational testing harnesses** using `ConversationalTestCase` to validate `RoleAdherence` and `ConversationCompleteness`, eliminating context drift and detecting premature conversation abandonment in customer support workflows.
* **Automated synthetic golden dataset generation** using DeepEval's `Synthesizer`, scaling test coverage across enterprise policies without manual curation, and integrated automated **Quality Gates into Jenkins CI pipelines** to block builds on metric regression.

---

## 🎙️ Key Interview Talking Points

* **Deterministic vs. Probabilistic Testing**: Standard testing asserts exact strings (`assert actual == expected`). Generative AI testing asserts semantic properties (faithfulness, relevancy, bias) using an LLM-as-a-Judge with calibrated thresholds.
* **Isolating Retrieval from Generation**: Decouples search bugs (low Contextual Precision/Recall in Vector DB) from generation bugs (LLM hallucinations/unfaithfulness) to accelerate root-cause triage.
* **Adversarial Red-Teaming**: Evaluates beyond happy paths with jailbreak prompts, prompt leakage attacks, and edge-case guardrails.
* **Shift-Left Quality Gates**: Data-driven regression testing via `@pytest.mark.parametrize` embedded into CI/CD pipelines to block degraded model versions before deployment.


