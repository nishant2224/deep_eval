# Module 00: Modern Python Tooling & Package Management with UV

## 1. What is UV?

[UV](https://github.com/astral-sh/uv) is an extremely fast Python package and project manager developed by Astral (the creators of Ruff), written in **Rust**.

In modern Python engineering and Test Automation, UV acts as a single drop-in replacement for:
- **`pip`** & **`pip-tools`** (dependency installation & compilation)
- **`virtualenv`** / **`venv`** (virtual environment creation)
- **`pyenv`** (installing and switching Python runtime versions)
- **`poetry`** / **`pipenv`** (project management, lockfiles, and packaging)

---

## 2. Why SDETs & GenAI Engineers Use UV Over Pip

As an SDET building test automation frameworks, UV provides distinct architectural advantages:

| Problem with Traditional `pip` + `venv` | Solution with `uv` | SDET Benefit |
| :--- | :--- | :--- |
| **Slow installation**: Installing heavy ML/eval libraries (`torch`, `deepeval`, `scipy`) takes 2-5 minutes. | **10-100x faster**: UV uses global disk caching, parallel HTTP downloads, and Rust-level resolution. | CI/CD test runs start in seconds, saving compute minutes on GitHub Actions. |
| **"Works on my machine" flakiness**: `pip install -r requirements.txt` can resolve different sub-dependencies on CI vs. local. | **Deterministic `uv.lock`**: Every transitive package version is pinned and checksummed. | Eliminates flaky test failures caused by third-party package updates. |
| **Manual Venv Activation**: Forgetting to activate `source .venv/bin/activate` or `.\.venv\Scripts\activate.ps1`. | **Ephemeral & Contextual execution**: `uv run <command>` runs directly inside the venv without manual activation. | Simplifies automation scripts and IDE integration. |
| **Python Version Drift**: Colleague has Python 3.14, CI has 3.11, framework requires 3.12. | **Built-in Python Management**: UV downloads and manages CPython versions directly (`uv python install 3.12`). | Zero need for external tools like Pyenv or system-level Python reinstalls. |

---

## 3. The 3 Core Files in a Modern UV Project

In this repository, you will see three key configuration files:

```
deep-eval-project/
├── pyproject.toml      # The human-readable project manifest (PEP 621)
├── uv.lock             # The machine-generated deterministic lockfile
└── .venv/              # The isolated virtual environment
```

### A. `pyproject.toml`
Declares direct dependencies and test configuration:
```toml
[project]
name = "enterprise-llm-evalops"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "deepeval>=4.2.8",
    "pytest>=8.0.0",
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v -s --tb=short"
```

### B. `uv.lock`
Similar to `package-lock.json` in Playwright/Node.js or `Gemfile.lock` in Ruby:
- It tracks the **exact** versions of all direct and indirect dependencies (e.g., `pydantic==2.13.5`, `requests==2.34.2`).
- **Never edit this file manually.** It is generated and updated automatically by `uv add`, `uv remove`, or `uv lock`.

### C. `.venv`
The isolated folder containing the Python binaries and installed libraries. UV manages this folder automatically.

---

## 4. Daily SDET Cheat Sheet

### Running Tests and Commands
Always prefix commands with `uv run` to ensure they execute inside the project's virtual environment:

```powershell
# Run the entire Pytest test suite
uv run pytest

# Run a specific DeepEval test file
uv run deepeval test run tests/test_00_smoke.py

# Run a one-off python script
uv run python path/to/script.py
```

### Managing Dependencies

```powershell
# Add a new runtime dependency (updates pyproject.toml and uv.lock, installs into .venv)
uv add langchain

# Add a development/test-only dependency (e.g. linter, formatter)
uv add --dev ruff

# Remove a dependency
uv remove langchain

# Synchronize the .venv to match uv.lock exactly (removes unlisted packages)
uv sync
```

### Managing Python Versions

```powershell
# List all Python versions installed or available for download
uv python list

# Install a specific CPython version directly
uv python install 3.12

# Create or recreate a virtual environment with a specific Python version
uv venv --python 3.12
```

---

## 5. Running One-Off Tools with `uvx` (UV Executive)

Just like `npx` in Node.js, UV has **`uvx`** to run CLI tools without installing them into your project's dependencies:

```powershell
# Run the Ruff linter without adding it to pyproject.toml
uvx ruff check .

# Format code according to PEP 8
uvx ruff format .
```

---

## 6. How This Integrates into CI/CD (GitHub Actions Preview)

When building our Day 9 CI/CD quality gate, using UV reduces pipeline setup time from ~90 seconds to under 10 seconds:

```yaml
- name: Install UV
  uses: astral-sh/setup-uv@v3
  with:
    enable-cache: true

- name: Set up Python
  run: uv python install 3.12

- name: Install Dependencies
  run: uv sync --frozen

- name: Run DeepEval Quality Gate
  run: uv run deepeval test run tests/test_00_smoke.py
```
*(The `--frozen` flag guarantees that CI refuses to run if `uv.lock` is out of sync with `pyproject.toml`, preventing silent configuration drift).*

---

### Navigation:
- ➡️ **Next**: [Module 01: Mental Model & Foundations of LLM Evaluation](file:///d:/deep-eval-project/learning_notes/01_mental_model_and_foundations.md)

