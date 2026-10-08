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
├── learning_notes/                     # 10-Day curriculum and SDET architectural notes
│   ├── 00_python_tooling_with_uv.md    # UV package manager guide & CLI cheatsheet
│   ├── 01_mental_model_and_foundations.md # Deterministic vs. Probabilistic testing
│   └── 02_judge_configuration_and_framework_setup.md # Judge config & Windows gotchas
├── tests/                              # Pytest test suites
│   ├── conftest.py                     # Global fixtures & environment bootstrap
│   └── test_00_smoke.py                # Baseline smoke tests (Answer Relevancy)
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
- [ ] **Day 5**: LLM Safety, Guardrails & Red-Teaming (Toxicity, Bias, Prompt Injection)
- [ ] **Day 6**: Conversational & AI Agent Evaluation (Multi-turn conversations & trajectories)
- [ ] **Day 7**: Synthetic Golden Dataset Generation (`Synthesizer`)
- [ ] **Day 8**: SDET Test Automation Framework Architecture (Parametrization & Fixtures)
- [ ] **Day 9**: CI/CD Quality Gates (GitHub Actions PR blocking)
- [ ] **Day 10**: Portfolio Packaging, Dashboards & Resume Highlights
