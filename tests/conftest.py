"""
Pytest configuration and global fixtures.
Automatically loads environment variables from .env on test session startup.
"""

import os
import sys
import time
from pathlib import Path
import pytest
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load .env file from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")


@pytest.fixture(autouse=True)
def rate_limit_pacer():
    """
    Paces test execution by introducing a brief pause after each test.
    Prevents triggering HTTP 429 (Resource Exhausted) on free-tier LLM API keys (15 RPM).
    """
    yield
    time.sleep(4.0)


