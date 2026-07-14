"""Optional request guardrail integration.

NeMo rails are not configured in this repository, so this hook transparently
passes requests through until a rails configuration is added.
"""
import logfire


def initialize_rails() -> None:
    """Initialise available guardrails without blocking application startup."""
    logfire.info("No NeMo guardrail configuration found; guardrails are in pass-through mode.")


def guard(query: str) -> tuple[bool, str]:
    """Return whether a query is blocked and an optional safe response."""
    return False, ""
