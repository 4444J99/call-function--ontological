#!/usr/bin/env python3
"""Demo script: load the OpenAI schema and run ontological analysis.

Usage:
    python examples/sample_analysis.py

This script demonstrates the full analysis pipeline by loading the
example OpenAI function-calling schema and printing both the text
report and a brief JSON summary.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure project root is on sys.path.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from application.analyzer import OntologicalAnalyzer
from application.grounding_report import format_summary, format_text_report


def main() -> None:
    """Load the sample schema and run the full analysis pipeline."""
    schema_path = Path(__file__).resolve().parent / "openai_schema.json"

    if not schema_path.exists():
        print(f"Error: schema file not found at {schema_path}", file=sys.stderr)
        sys.exit(1)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    print(f"Analyzing schema: {schema['name']}")
    print(f"Description: {schema.get('description', 'N/A')}")
    print()

    # Run analysis.
    analyzer = OntologicalAnalyzer()
    result = analyzer.analyze(schema)

    # Print full text report.
    print(format_text_report(result))

    # Print brief summary.
    print("\n--- SUMMARY ---")
    print(format_summary(result))

    # Print JSON (abbreviated).
    print("\n--- JSON OUTPUT (grounding section only) ---")
    print(json.dumps(result.grounding.to_dict(), indent=2))


if __name__ == "__main__":
    main()
