"""
Script: Generate Synthetic Golden Dataset
-----------------------------------------
Reads company policy context chunks from src/knowledge_base/store_policies.json,
uses DeepEval's Synthesizer to generate realistic ground-truth test cases (Goldens),
and exports the dataset to data/synthetic_goldens.json.
"""

import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure root directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env")

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from deepeval.synthesizer import Synthesizer


def generate_and_save_dataset():
    kb_path = ROOT_DIR / "src" / "knowledge_base" / "store_policies.json"
    data_dir = ROOT_DIR / "data"
    data_dir.mkdir(exist_ok=True)

    print(f"📖 Loading knowledge base from: {kb_path}")
    with open(kb_path, "r", encoding="utf-8") as f:
        policies = json.load(f)

    # Selecting key policies for golden test generation
    selected_topics = [
        "Returns and Refunds",
        "Warranty and Hardware Repairs",
        "Shipping Speeds and Costs",
    ]
    contexts = [
        [doc["content"]]
        for doc in policies
        if doc["topic"] in selected_topics
    ]

    print(f"🎯 Generating synthetic goldens for {len(contexts)} policy context chunks...")
    synthesizer = Synthesizer()
    goldens = synthesizer.generate_goldens_from_contexts(
        contexts=contexts,
        max_goldens_per_context=1,
        include_expected_output=True,
        _send_data=False,
    )

    print(f"✅ Generated {len(goldens)} synthetic golden test cases.")

    # Save to JSON
    saved_path = synthesizer.save_as(
        file_type="json",
        directory=str(data_dir),
        file_name="synthetic_goldens",
    )
    print(f"💾 Dataset successfully saved to: {saved_path}")

    for idx, golden in enumerate(goldens, 1):
        print(f"\n--- [Golden #{idx}] ---")
        print(f"Query (Input):    {golden.input}")
        print(f"Expected Answer:  {golden.expected_output}")
        print(f"Context:          {golden.context}")


if __name__ == "__main__":
    generate_and_save_dataset()
