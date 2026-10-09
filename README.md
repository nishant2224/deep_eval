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
├── learning_notes/                     # 10-Day curriculum & SDET architectural notes
│   ├── QUICK_REVISION_CHEATSHEET.md    # ⚡ 5-min revision cheat sheet & SDET gotchas guide
│   ├── METRICS_MASTER_REFERENCE.md     # 📊 Master catalog of all metrics & failure modes
│   ├── 00_python_tooling_with_uv.md    # UV package manager guide & CLI cheatsheet
│   ├── 01_mental_model_and_foundations.md # Deterministic vs. Probabilistic testing
│   ├── 02_judge_configuration_and_framework_setup.md # Judge config & Windows gotchas
│   ├── 03_rag_faithfulness_and_hallucination.md # Day 2: Faithfulness & Hallucination
│   ├── 04_rag_context_retrieval_triad.md        # Day 3: Context Retrieval Triad
│   ├── 05_custom_business_rubrics_with_geval.md # Day 4: G-Eval Business Rubrics
│   ├── 06_building_and_testing_live_rag_aut.md  # Day 5: Live RAG Application Under Test
│   ├── 07_llm_safety_guardrails_and_red_teaming.md # Day 6: Safety, Bias & Red-Teaming
│   ├── 08_conversational_and_agent_evaluation.md # Day 7: Multi-Turn & Agent Evaluation
│   ├── 09_synthetic_dataset_generation.md      # Day 8: Synthetic Data & Benchmarks
│   ├── 10_sdet_framework_and_cicd_quality_gates.md # Day 9: CI/CD Quality Gates & Regressions
│   └── 11_portfolio_packaging_and_resume_highlights.md # Day 10: Portfolio & Resume Packaging
├── data/                               # 📦 Synthetic Datasets & Golden Benchmarks
│   └── synthetic_goldens.json          # Synthesized ground-truth test cases
├── scripts/                            # ⚙️ Offline utility & generation scripts
│   └── generate_goldens.py             # Synthesizer script for store policies
├── src/                                # 🚀 Application Under Test (AUT)
│   ├── knowledge_base/store_policies.json # Corporate knowledge base
│   └── bot.py                          # CustomerSupportRAGBot implementation
├── tests/                              # Pytest test suites
│   ├── conftest.py                     # Global fixtures, rate limiter & .env loader
│   ├── test_00_smoke.py                # Day 1: Answer Relevancy smoke tests
│   ├── test_01_rag_faithfulness.py     # Day 2: Faithfulness & Hallucination
│   ├── test_02_rag_context_triad.py    # Day 3: Context Retrieval Triad
│   ├── test_03_custom_geval.py         # Day 4: Custom Business Rubrics (G-Eval)
│   ├── test_04_live_rag_e2e.py         # Day 5: Live End-to-End RAG Testing
│   ├── test_05_safety_and_red_team.py  # Day 6: Safety, Bias & Adversarial Red-Teaming
│   ├── test_06_conversational_e2e.py   # Day 7: Multi-Turn Conversational & Role Adherence
│   ├── test_07_synthetic_goldens_e2e.py # Day 8: Live Evaluation against Synthetic Goldens
│   └── test_08_dataset_parametrized_regression.py # Day 9: Parameterized Golden Regressions
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

## 📖 10-Day Curriculum

- [x] **Day 1**: Foundations, Mental Model & Smoke Tests (`AnswerRelevancyMetric`)
- [x] **Day 2**: RAG Pipeline Evaluation Part 1 — Faithfulness & Hallucination Detection
- [x] **Day 3**: RAG Pipeline Evaluation Part 2 — Context Retrieval Triad (Precision, Recall, Relevancy)
- [x] **Day 4**: Custom Business Rubrics with G-Eval
- [x] **Day 5**: The Live Application Under Test (AUT) — Building the Customer Support RAG Bot & E2E Testing
- [x] **Day 6**: LLM Safety, Guardrails & Red-Teaming (Toxicity, Bias, Jailbreak & Injection Defense)
- [x] **Day 7**: Conversational AI & Autonomous Agent Evaluation (Multi-turn Chat & Tool Call Trajectories)
- [x] **Day 8**: Synthetic Golden Dataset Generation (`Synthesizer` from Knowledge Base)
- [x] **Day 9**: SDET Test Automation Framework & CI/CD Quality Gates (Fixtures, Parametrization, Jenkins Pipelines)
- [x] **Day 10**: Portfolio Packaging, Confident AI Dashboards & Resume Highlights

---

## 💼 SDET Resume Highlights & Interview Talking Points

Looking to showcase this framework on your resume or prepare for GenAI SDET interviews?
Check out the **[Day 10 Portfolio & Resume Guide](file:///d:/deep-eval-project/learning_notes/11_portfolio_packaging_and_resume_highlights.md)** for:
* **5 battle-tested resume bullet points** covering RAG Triad automation, G-Eval business rubrics, adversarial red-teaming, and CI/CD quality gates.
* **4-pillar interview narrative** for explaining deterministic vs. probabilistic evaluation, isolating retrieval from generation, and shift-left quality gates.

