# Module 02: Judge Configuration, Framework Setup & Troubleshooting

## 1. The LLM-as-a-Judge Infrastructure

DeepEval does not evaluate your application using static assertions; it sends your test cases and scoring rubrics to an **Evaluation Judge Model** to grade them on a scale of `0.0` to `1.0`.

While OpenAI (`gpt-4o` / `gpt-4o-mini`) is the default judge, in production and enterprise test automation you often need to support multiple LLM providers:
- **Google Gemini** (cost-effective, high rate limits on free tier)
- **Local Ollama** (data-privacy sensitive, runs completely offline)
- **Azure OpenAI / AWS Bedrock** (enterprise cloud compliance)

---

## 2. Environment Variables & `.env` Anatomy

DeepEval provides a unified configuration registry that reads from environment variables. Here is how our project is configured:

```env
# ==========================================
# Google Gemini as Judge
# ==========================================
USE_GEMINI_MODEL="Y"
GEMINI_MODEL_NAME="gemini-3.5-flash-lite"
PYTHONIOENCODING="utf-8"
PYTHONUTF8="1"
GOOGLE_API_KEY=AQ.Ab8RN6LoBZ2CBY...
```

### Breakdown of Each Parameter:

1. **`USE_GEMINI_MODEL="Y"` (The Global Switch)**:
   - By default, DeepEval metric classes (`AnswerRelevancyMetric`, `FaithfulnessMetric`, etc.) instantiate an `OpenAIModel` judge.
   - Setting `USE_GEMINI_MODEL="Y"` instructs DeepEval globally to instantiate `GeminiModel` instead across your entire test suite without needing to modify your test scripts.

2. **`GEMINI_MODEL_NAME="gemini-3.5-flash-lite"` (Model Identifier)**:
   - Sets the specific model version to use for scoring.
   - *Production Lesson*: Cloud LLM providers frequently deprecate model endpoints (e.g., `gemini-1.5-flash` was retired for new users in favor of `gemini-3.5-flash-lite`). Keeping this in `.env` allows you to upgrade or swap model versions instantly across all tests with zero code changes.

3. **`GOOGLE_API_KEY` (Secret Management)**:
   - Authenticates against Google AI Studio.
   - Kept in `.env` (which is excluded from Git via `.gitignore`), while [.env.example](file:///d:/deep-eval-project/.env.example) serves as the public template for the team.

4. **`PYTHONIOENCODING="utf-8"` & `PYTHONUTF8="1"`**:
   - Instructs Python runtime and child processes to strictly utilize UTF-8 character encoding.

---

## 3. Pytest Framework Bootstrapping (`conftest.py`)

In enterprise test frameworks, tests should focus purely on business validation logic rather than boilerplates like loading environment variables or configuring system paths.

We use [`tests/conftest.py`](file:///d:/deep-eval-project/tests/conftest.py) to handle session setup automatically:

```python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 1. Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 2. Load .env file from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")
```

### Why This Design Matters to an SDET:
* **Zero Boilerplate in Tests**: Individual test files (`test_00_smoke.py`, `test_01_rag_faithfulness.py`) never need to import `load_dotenv` or manually locate `.env`.
* **Guaranteed Execution Order**: Pytest executes `conftest.py` *before* collecting or running test functions, ensuring environment credentials exist before any metric class is initialized.

---

## 4. Real-World Troubleshooting & Cross-Platform Gotchas

During Day 1 setup on Windows, we encountered and resolved three classic environment challenges that every SDET working with LLM tooling should know:

### Gotcha A: Windows PowerShell `UnicodeEncodeError` (`\u26a0`)
* **Symptom**:
  ```text
  UnicodeEncodeError: 'charmap' codec can't encode character '\u26a0' in position 0
  ```
* **Root Cause**: Windows PowerShell and CMD default to legacy code page `cp1252` instead of standard UTF-8. DeepEval uses the `rich` library to render console tables, progress indicators, and Unicode icons (`🎯`, `⚠️ \u26a0`, `✓`). Because `cp1252` lacks these characters, Python throws a charmap encoding error.
* **Solution**: In `tests/conftest.py`, dynamically reconfigure `sys.stdout` and `sys.stderr` to `utf-8` on Windows startup.

---

### Gotcha B: Model Retirement / 404 NOT_FOUND
* **Symptom**:
  ```text
  google.genai.errors.ClientError: 404 NOT_FOUND. 
  'models/gemini-1.5-flash is not found for API version v1beta'
  ```
* **Root Cause**: LLM model names change over time as new versions launch and older versions are phased out.
* **Debugging Technique**: Run a quick diagnostic script using the SDK client to query available models for your active API key:
  ```powershell
  uv run python -c "from google import genai; [print(m.name) for m in genai.Client().models.list()]"
  ```
* **Solution**: Set `GEMINI_MODEL_NAME="gemini-3.5-flash-lite"` in `.env`.

---

### Gotcha C: Windows File-Locking Warning (`portalocker`)
* **Symptom**:
  ```text
  Warning: Could not load test run from disk: Shared locks on Windows require the win32 extra (pywin32)
  ```
* **Root Cause**: DeepEval uses `portalocker` to cache test runs and evaluation traces to disk. On Windows, standard C runtime (`msvcrt`) does not support shared non-blocking file locks.
* **Solution**: Install the Win32 API extra via UV:
  ```powershell
  uv add "portalocker[win32]"
  ```

---

## 5. Verification: How to Confirm the Environment is Healthy

Run the smoke test anytime to verify your pipeline:

```powershell
# Using the DeepEval CLI (with terminal tables & score reasons)
uv run deepeval test run tests/test_00_smoke.py

# Or using standard Pytest
uv run pytest tests/test_00_smoke.py -v
```

A healthy run will output:
- `test_answer_relevancy_passing` -> **Score 1.0 (PASSED)**
- `test_answer_relevancy_failing` -> **Score 0.0 (FAILED)** (Handled cleanly by `pytest.raises(AssertionError)`)
- `2 passed in ~14s` with zero warnings or crashes.

---

### Navigation:
- ⬅️ **Previous**: [Module 01: Mental Model & Foundations of LLM Evaluation](file:///d:/deep-eval-project/learning_notes/01_mental_model_and_foundations.md)
- ➡️ **Next (Day 2)**: Module 03: RAG Evaluation — Faithfulness & Hallucination Detection (Upcoming)

