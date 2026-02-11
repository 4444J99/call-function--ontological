"""OntologicalAnalyzer: unified analysis pipeline.

This module provides the top-level analyzer that takes a function description
(as a dict or JSON string) and orchestrates all three philosophical analyses
(Aristotelian four causes, Heideggerian phenomenology, Peircean semiotics),
then synthesizes grounding and telos bridge assessments.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from core.dasein import DaseinAnalysis, analyze_dasein
from core.four_causes import FourCausesReport, analyze_four_causes
from core.grounding import GroundingReport, ground_function
from core.semiotics import SemioticAnalysis, analyze_semiotics


@dataclass
class FullAnalysis:
    """Complete ontological analysis of a function-calling schema.

    Attributes:
        function_name: The analyzed function's name.
        four_causes: Aristotelian four-causes analysis.
        dasein: Heideggerian phenomenological analysis.
        semiotics: Peircean semiotic analysis.
        grounding: Synthetic grounding report mapping all 12 concepts.
    """

    function_name: str
    four_causes: FourCausesReport
    dasein: DaseinAnalysis
    semiotics: SemioticAnalysis
    grounding: GroundingReport

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full analysis to a plain dictionary."""
        return {
            "function_name": self.function_name,
            "four_causes": self.four_causes.to_dict(),
            "dasein": self.dasein.to_dict(),
            "semiotics": self.semiotics.to_dict(),
            "grounding": self.grounding.to_dict(),
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize the full analysis to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


class OntologicalAnalyzer:
    """Orchestrates all ontological analyses for a function-calling schema.

    Usage:
        analyzer = OntologicalAnalyzer()
        result = analyzer.analyze(schema_dict)
        print(result.to_json())

    The analyzer is stateless; each call to analyze() is independent.
    """

    def analyze(self, schema: dict[str, Any] | str) -> FullAnalysis:
        """Run all analyses on a function-calling schema.

        Args:
            schema: Either a dict representing the function-calling schema,
                or a JSON string that will be parsed into a dict.

        Returns:
            A FullAnalysis containing all four sub-analyses.

        Raises:
            ValueError: If the schema is missing required fields.
            json.JSONDecodeError: If a string schema is not valid JSON.
        """
        if isinstance(schema, str):
            schema = json.loads(schema)

        function_name = schema.get("name", "")
        if not function_name:
            raise ValueError("Schema must include a 'name' field.")

        four_causes = analyze_four_causes(schema)
        dasein = analyze_dasein(schema)
        semiotics = analyze_semiotics(schema)
        grounding = ground_function(schema)

        return FullAnalysis(
            function_name=function_name,
            four_causes=four_causes,
            dasein=dasein,
            semiotics=semiotics,
            grounding=grounding,
        )

    def analyze_json(self, json_string: str) -> FullAnalysis:
        """Convenience method: analyze a JSON string.

        Args:
            json_string: A JSON string representing the function schema.

        Returns:
            A FullAnalysis.
        """
        return self.analyze(json_string)

    def analyze_file(self, filepath: str) -> FullAnalysis:
        """Analyze a function schema from a JSON file.

        Args:
            filepath: Path to a JSON file containing the function schema.

        Returns:
            A FullAnalysis.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            schema = json.load(f)
        return self.analyze(schema)
