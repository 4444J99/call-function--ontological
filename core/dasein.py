"""Heideggerian phenomenological analysis for function-calling schemas.

This module applies three Heideggerian concepts to function-calling:

- **Dasein** (being-in-the-world): What world-state must already exist for
  the function to make sense? What existential preconditions does it assume?
- **Zuhandenheit** (ready-to-hand): When does the function operate as a
  transparent tool, withdrawn from conscious attention?
- **Vorhandenheit** (present-at-hand): When does the function become an
  explicit object of analysis — during breakdown, debugging, or inspection?

The analysis is deterministic, based on structural inspection of the schema,
parameter constraints, and naming conventions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorldAssumption:
    """A single precondition the function assumes about the world.

    Attributes:
        aspect: What dimension of the world this assumption concerns
            (e.g., 'data_availability', 'service_reachability', 'auth_state').
        description: Human-readable statement of the assumption.
        derived_from: Which schema element(s) this was inferred from.
    """

    aspect: str
    description: str
    derived_from: str


@dataclass
class BreakdownCondition:
    """A condition under which the function shifts from ready-to-hand
    to present-at-hand (i.e., breaks down and demands explicit attention).

    Attributes:
        trigger: What causes the breakdown.
        consequence: What happens when the function breaks down.
        severity: 'minor' (recoverable) or 'major' (halts workflow).
    """

    trigger: str
    consequence: str
    severity: str = "minor"


@dataclass
class DaseinAnalysis:
    """Complete Heideggerian analysis of a function.

    Attributes:
        function_name: The analyzed function's name.
        world_assumptions: Existential preconditions (Dasein).
        transparency_conditions: When the function is ready-to-hand
            (Zuhandenheit) — operating as a transparent tool.
        breakdown_conditions: When the function becomes present-at-hand
            (Vorhandenheit) — an object of explicit analysis.
    """

    function_name: str
    world_assumptions: list[WorldAssumption] = field(default_factory=list)
    transparency_conditions: list[str] = field(default_factory=list)
    breakdown_conditions: list[BreakdownCondition] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {
            "function_name": self.function_name,
            "dasein": {
                "world_assumptions": [
                    {
                        "aspect": wa.aspect,
                        "description": wa.description,
                        "derived_from": wa.derived_from,
                    }
                    for wa in self.world_assumptions
                ]
            },
            "zuhandenheit": {
                "transparency_conditions": self.transparency_conditions,
            },
            "vorhandenheit": {
                "breakdown_conditions": [
                    {
                        "trigger": bc.trigger,
                        "consequence": bc.consequence,
                        "severity": bc.severity,
                    }
                    for bc in self.breakdown_conditions
                ]
            },
        }


# ---------------------------------------------------------------------------
# Heuristic keyword sets for world-assumption inference
# ---------------------------------------------------------------------------

_LOCATION_KEYWORDS = {"location", "city", "address", "region", "country", "place", "lat", "lng", "latitude", "longitude", "zip", "postal"}
_AUTH_KEYWORDS = {"token", "api_key", "apikey", "auth", "credentials", "secret", "password", "session"}
_ID_KEYWORDS = {"id", "user_id", "account_id", "order_id", "item_id", "resource_id", "entity_id"}
_TEMPORAL_KEYWORDS = {"date", "time", "timestamp", "start_date", "end_date", "since", "until", "after", "before"}
_NETWORK_KEYWORDS = {"url", "endpoint", "host", "uri", "domain", "webhook"}


def _infer_world_assumptions(
    function_name: str, schema: dict[str, Any]
) -> list[WorldAssumption]:
    """Infer what world-state the function assumes must already exist."""
    assumptions: list[WorldAssumption] = []
    params = schema.get("parameters", {}).get("properties", {})
    required = set(schema.get("parameters", {}).get("required", []))

    # Every function assumes a callable context.
    assumptions.append(
        WorldAssumption(
            aspect="callable_context",
            description=(
                f"A runtime environment exists in which '{function_name}' "
                f"can be invoked and its results returned to the caller."
            ),
            derived_from="function existence",
        )
    )

    for param_name, param_spec in params.items():
        lower_name = param_name.lower()

        if lower_name in _LOCATION_KEYWORDS or any(kw in lower_name for kw in _LOCATION_KEYWORDS):
            assumptions.append(
                WorldAssumption(
                    aspect="geographic_reality",
                    description=(
                        f"Parameter '{param_name}' assumes a geographic entity "
                        f"exists and is identifiable by the caller."
                    ),
                    derived_from=f"parameter '{param_name}'",
                )
            )

        if lower_name in _AUTH_KEYWORDS or any(kw in lower_name for kw in _AUTH_KEYWORDS):
            assumptions.append(
                WorldAssumption(
                    aspect="auth_state",
                    description=(
                        f"Parameter '{param_name}' assumes the caller possesses "
                        f"valid authentication credentials."
                    ),
                    derived_from=f"parameter '{param_name}'",
                )
            )

        if lower_name in _ID_KEYWORDS or lower_name.endswith("_id"):
            assumptions.append(
                WorldAssumption(
                    aspect="entity_existence",
                    description=(
                        f"Parameter '{param_name}' assumes a corresponding "
                        f"entity already exists in the system."
                    ),
                    derived_from=f"parameter '{param_name}'",
                )
            )

        if lower_name in _TEMPORAL_KEYWORDS or any(kw in lower_name for kw in _TEMPORAL_KEYWORDS):
            assumptions.append(
                WorldAssumption(
                    aspect="temporal_context",
                    description=(
                        f"Parameter '{param_name}' assumes a meaningful "
                        f"temporal reference frame."
                    ),
                    derived_from=f"parameter '{param_name}'",
                )
            )

        if lower_name in _NETWORK_KEYWORDS or any(kw in lower_name for kw in _NETWORK_KEYWORDS):
            assumptions.append(
                WorldAssumption(
                    aspect="network_reachability",
                    description=(
                        f"Parameter '{param_name}' assumes a network endpoint "
                        f"is reachable."
                    ),
                    derived_from=f"parameter '{param_name}'",
                )
            )

    # If the function has a description mentioning external services.
    description = schema.get("description", "").lower()
    service_words = ["api", "service", "server", "database", "external"]
    if any(word in description for word in service_words):
        assumptions.append(
            WorldAssumption(
                aspect="service_availability",
                description=(
                    "The function description references external services, "
                    "assuming they are available and responsive."
                ),
                derived_from="function description",
            )
        )

    return assumptions


def _infer_transparency_conditions(
    function_name: str, schema: dict[str, Any]
) -> list[str]:
    """Determine when the function operates as a transparent tool (Zuhandenheit)."""
    conditions: list[str] = [
        (
            f"When '{function_name}' is called with valid arguments and returns "
            f"the expected result, it is ready-to-hand — the caller proceeds "
            f"without reflecting on the function itself."
        ),
    ]

    params = schema.get("parameters", {}).get("properties", {})
    required = schema.get("parameters", {}).get("required", [])

    if required:
        conditions.append(
            f"Transparency holds when all required parameters "
            f"({', '.join(required)}) are provided and well-formed."
        )

    if any(p.get("enum") for p in params.values()):
        enum_params = [name for name, spec in params.items() if spec.get("enum")]
        conditions.append(
            f"Enum-constrained parameters ({', '.join(enum_params)}) guide "
            f"the caller toward valid inputs, maintaining tool transparency."
        )

    return conditions


def _infer_breakdown_conditions(
    function_name: str, schema: dict[str, Any]
) -> list[BreakdownCondition]:
    """Determine when the function becomes present-at-hand (Vorhandenheit)."""
    breakdowns: list[BreakdownCondition] = []
    params = schema.get("parameters", {}).get("properties", {})
    required = schema.get("parameters", {}).get("required", [])

    # Missing required parameters.
    if required:
        breakdowns.append(
            BreakdownCondition(
                trigger=f"Missing required parameter(s): {', '.join(required)}.",
                consequence=(
                    "The function cannot execute; the caller must stop and "
                    "inspect what went wrong — the tool becomes present-at-hand."
                ),
                severity="major",
            )
        )

    # Type mismatches.
    typed_params = [
        (name, spec.get("type", "unknown"))
        for name, spec in params.items()
        if spec.get("type")
    ]
    if typed_params:
        breakdowns.append(
            BreakdownCondition(
                trigger="A parameter is passed with an incorrect type.",
                consequence=(
                    "Schema validation fails; the caller must examine the "
                    "function specification to understand the expected types."
                ),
                severity="major",
            )
        )

    # Invalid enum values.
    enum_params = [name for name, spec in params.items() if spec.get("enum")]
    if enum_params:
        breakdowns.append(
            BreakdownCondition(
                trigger=f"Invalid enum value for parameter(s): {', '.join(enum_params)}.",
                consequence=(
                    "The caller must consult the allowed values, forcing the "
                    "function from transparent tool into explicit object of study."
                ),
                severity="minor",
            )
        )

    # General breakdown: unexpected return.
    breakdowns.append(
        BreakdownCondition(
            trigger="The function returns an error or unexpected result.",
            consequence=(
                "The caller's workflow is interrupted; they must debug, "
                "read documentation, or inspect the function — it becomes "
                "present-at-hand."
            ),
            severity="minor",
        )
    )

    return breakdowns


def analyze_dasein(schema: dict[str, Any]) -> DaseinAnalysis:
    """Perform a complete Heideggerian phenomenological analysis.

    Args:
        schema: A function-calling schema dict with at minimum 'name'.

    Returns:
        A DaseinAnalysis with world assumptions, transparency conditions,
        and breakdown conditions.

    Raises:
        ValueError: If 'name' is missing from the schema.
    """
    function_name = schema.get("name", "")
    if not function_name:
        raise ValueError("Schema must include a 'name' field.")

    return DaseinAnalysis(
        function_name=function_name,
        world_assumptions=_infer_world_assumptions(function_name, schema),
        transparency_conditions=_infer_transparency_conditions(function_name, schema),
        breakdown_conditions=_infer_breakdown_conditions(function_name, schema),
    )
