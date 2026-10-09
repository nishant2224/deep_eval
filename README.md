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
├── learning_notes/                     # SDET architectural documentation & reference guides
│   ├── QUICK_REVISION_CHEATSHEET.md    # ⚡ 5-min revision cheat sheet & SDET gotchas guide
│   ├── METRICS_MASTER_REFERENCE.md     # 📊 Master catalog of all metrics & failure modes
│   ├── 00_python_tooling_with_uv.md    # UV package manager guide & CLI cheatsheet
│   ├── 01_mental_model_and_foundations.md # Deterministic vs. Probabilistic testing
│   ├── 02_judge_configuration_and_framework_setup.md # Judge config & Windows gotchas
│   ├── 03_rag_faithfulness_and_hallucination.md # Faithfulness & Hallucination
│   ├── 04_rag_context_retrieval_triad.md        # Context Retrieval Triad
│   ├── 05_custom_business_rubrics_with_geval.md # G-Eval Business Rubrics
│   ├── 06_building_and_testing_live_rag_aut.md  # Live RAG Application Under Test
│   ├── 07_llm_safety_guardrails_and_red_teaming.md # Safety, Bias & Red-Teaming
│   ├── 08_conversational_and_agent_evaluation.md # Multi-Turn & Agent Evaluation
│   ├── 09_synthetic_dataset_generation.md      # Synthetic Data & Benchmarks
│   ├── 10_sdet_framework_and_cicd_quality_gates.md # CI/CD Quality Gates & Regressions
│   └── 11_portfolio_packaging_and_resume_highlights.md # Portfolio & Resume Packaging
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

## 💼 SDET Resume Highlights & Interview Talking Points

Looking to showcase this framework on your resume or prepare for GenAI SDET interviews?
Check out the **[Portfolio & Resume Guide](file:///d:/deep-eval-project/learning_notes/11_portfolio_packaging_and_resume_highlights.md)** for:
* **5 battle-tested resume bullet points** covering RAG Triad automation, G-Eval business rubrics, adversarial red-teaming, and CI/CD quality gates.
* **4-pillar interview narrative** for explaining deterministic vs. probabilistic evaluation, isolating retrieval from generation, and shift-left quality gates.

