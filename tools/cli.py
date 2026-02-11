"""CLI entry point for ontological function-calling analysis.

Commands:
    analyze <json_file>  — Analyze a function-calling schema and print JSON.
    report <json_file>   — Generate a full human-readable grounding report.
    concepts             — List all 12 ontological concepts.

Usage:
    python -m tools.cli analyze examples/openai_schema.json
    python -m tools.cli report examples/openai_schema.json
    python -m tools.cli concepts
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure the project root is on sys.path so imports work when run as a script.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from application.analyzer import OntologicalAnalyzer
from application.grounding_report import format_json_report, format_text_report
from core.ontology import ALL_CONCEPTS, CONCEPTS_BY_DOMAIN, Domain


def _cmd_analyze(args: argparse.Namespace) -> None:
    """Run analysis and print JSON output."""
    schema = _load_schema(args.json_file)
    analyzer = OntologicalAnalyzer()
    result = analyzer.analyze(schema)
    print(format_json_report(result))


def _cmd_report(args: argparse.Namespace) -> None:
    """Run analysis and print human-readable text report."""
    schema = _load_schema(args.json_file)
    analyzer = OntologicalAnalyzer()
    result = analyzer.analyze(schema)
    print(format_text_report(result))


def _cmd_concepts(args: argparse.Namespace) -> None:
    """List all 12 ontological concepts."""
    print(f"{'#':<4} {'Name':<20} {'Domain':<15} Description")
    print("-" * 78)
    for i, concept in enumerate(ALL_CONCEPTS, 1):
        # Truncate description for display.
        desc = concept.description[:40] + "..." if len(concept.description) > 40 else concept.description
        print(f"{i:<4} {concept.name:<20} {concept.domain.value:<15} {desc}")

    print(f"\nTotal: {len(ALL_CONCEPTS)} concepts across {len(CONCEPTS_BY_DOMAIN)} domains.")
    for domain, concepts in CONCEPTS_BY_DOMAIN.items():
        names = ", ".join(c.name for c in concepts)
        print(f"  {domain.value}: {names}")


def _load_schema(filepath: str) -> dict:
    """Load a JSON schema from a file path."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    if not path.suffix == ".json":
        print(f"Warning: file does not have .json extension: {filepath}", file=sys.stderr)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="ontological",
        description="Ontological analysis of function-calling schemas.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # analyze
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a function-calling schema (JSON output).",
    )
    analyze_parser.add_argument(
        "json_file",
        help="Path to a JSON file containing the function schema.",
    )
    analyze_parser.set_defaults(func=_cmd_analyze)

    # report
    report_parser = subparsers.add_parser(
        "report",
        help="Generate a full human-readable grounding report.",
    )
    report_parser.add_argument(
        "json_file",
        help="Path to a JSON file containing the function schema.",
    )
    report_parser.set_defaults(func=_cmd_report)

    # concepts
    concepts_parser = subparsers.add_parser(
        "concepts",
        help="List all 12 ontological concepts.",
    )
    concepts_parser.set_defaults(func=_cmd_concepts)

    return parser


def main() -> None:
    """Main entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
