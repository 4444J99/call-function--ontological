"""Report formatting for ontological analyses.

Produces human-readable text reports or structured JSON output from
a FullAnalysis. The text format is designed for terminal display and
documentation; the JSON format is for machine consumption.
"""

from __future__ import annotations

import json
from typing import Any

from application.analyzer import FullAnalysis
from core.ontology import Domain


def _section_header(title: str, char: str = "=") -> str:
    """Create a section header with underline."""
    return f"\n{title}\n{char * len(title)}"


def _indent(text: str, level: int = 2) -> str:
    """Indent a block of text."""
    prefix = " " * level
    return "\n".join(prefix + line for line in text.splitlines())


def format_text_report(analysis: FullAnalysis) -> str:
    """Format a FullAnalysis as a human-readable text report.

    Args:
        analysis: The complete ontological analysis to format.

    Returns:
        A multi-line string suitable for terminal display.
    """
    lines: list[str] = []
    name = analysis.function_name

    # Title
    lines.append(f"ONTOLOGICAL ANALYSIS: {name}")
    lines.append("=" * (len("ONTOLOGICAL ANALYSIS: ") + len(name)))
    lines.append("")

    # --- Four Causes ---
    lines.append(_section_header("I. ARISTOTELIAN FOUR CAUSES"))
    for cause in analysis.four_causes.all_causes:
        lines.append(f"\n  [{cause.cause_type.upper()} CAUSE] ({cause.confidence} confidence)")
        lines.append(_indent(cause.summary, 4))
        if cause.evidence:
            lines.append(_indent("Evidence:", 4))
            for e in cause.evidence:
                lines.append(_indent(f"- {e}", 6))

    # --- Dasein ---
    lines.append(_section_header("\nII. HEIDEGGERIAN PHENOMENOLOGY"))

    lines.append("\n  [DASEIN — World Assumptions]")
    for wa in analysis.dasein.world_assumptions:
        lines.append(_indent(f"- [{wa.aspect}] {wa.description}", 4))
        lines.append(_indent(f"  (derived from: {wa.derived_from})", 4))

    lines.append("\n  [ZUHANDENHEIT — Transparency Conditions]")
    for tc in analysis.dasein.transparency_conditions:
        lines.append(_indent(f"- {tc}", 4))

    lines.append("\n  [VORHANDENHEIT — Breakdown Conditions]")
    for bc in analysis.dasein.breakdown_conditions:
        lines.append(_indent(f"- [{bc.severity.upper()}] {bc.trigger}", 4))
        lines.append(_indent(f"  -> {bc.consequence}", 4))

    # --- Semiotics ---
    lines.append(_section_header("\nIII. PEIRCEAN SEMIOTICS"))
    for comp in analysis.semiotics.all_components:
        lines.append(f"\n  [{comp.component.upper()}]")
        lines.append(_indent(comp.summary, 4))
        if comp.evidence:
            lines.append(_indent("Evidence:", 4))
            for e in comp.evidence:
                lines.append(_indent(f"- {e}", 6))

    # --- Grounding ---
    lines.append(_section_header("\nIV. SYNTHETIC GROUNDING"))
    gr = analysis.grounding
    lines.append(
        f"\n  Coverage: {gr.applicable_count}/{len(gr.mappings)} concepts "
        f"({gr.coverage_ratio:.1%})"
    )

    for domain in Domain:
        domain_mappings = gr.mappings_by_domain(domain)
        if domain_mappings:
            lines.append(f"\n  [{domain.value.upper()}]")
            for m in domain_mappings:
                status = "APPLIES" if m.applies else "N/A"
                lines.append(_indent(f"[{status}] {m.concept.name}", 4))
                lines.append(_indent(f"Anchor: {m.anchor}", 6))
                lines.append(_indent(f"  {m.explanation}", 6))

    # Footer
    lines.append("")
    lines.append("-" * 60)
    lines.append(f"End of ontological analysis for '{name}'.")
    lines.append("")

    return "\n".join(lines)


def format_json_report(analysis: FullAnalysis, indent: int = 2) -> str:
    """Format a FullAnalysis as a JSON string.

    Args:
        analysis: The complete ontological analysis to format.
        indent: JSON indentation level.

    Returns:
        A JSON string.
    """
    return analysis.to_json(indent=indent)


def format_summary(analysis: FullAnalysis) -> str:
    """Format a brief one-paragraph summary of the analysis.

    Args:
        analysis: The complete ontological analysis to format.

    Returns:
        A concise summary string.
    """
    name = analysis.function_name
    gr = analysis.grounding
    fc = analysis.four_causes

    return (
        f"Ontological analysis of '{name}': "
        f"{gr.applicable_count}/{len(gr.mappings)} concepts grounded "
        f"({gr.coverage_ratio:.0%} coverage). "
        f"Material: {fc.material.confidence} confidence. "
        f"Final cause: {fc.final.summary[:80]}... "
        f"World assumptions: {len(analysis.dasein.world_assumptions)}. "
        f"Breakdown conditions: {len(analysis.dasein.breakdown_conditions)}."
    )
