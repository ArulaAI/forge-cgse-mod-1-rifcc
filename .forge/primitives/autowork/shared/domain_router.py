"""Domain router for autowork — routes Issues to DomainConfig (Task 12)."""

from __future__ import annotations

from dataclasses import dataclass

from primitives.autowork.shared.config import AutoworkConfig, DomainConfig
from primitives.autowork.shared.issue_sources import Issue

_COMPLEXITY_TO_MODEL: dict[str, str] = {
    "high": "planner",
    "standard": "implementer",
    "mechanical": "inline",
}


def complexity_to_model(complexity: str) -> str:
    """Map a complexity level string to a logical model name.

    Args:
        complexity: One of ``"high"``, ``"standard"``, or ``"mechanical"``.

    Returns:
        The logical model name: ``"planner"``, ``"implementer"``, or ``"inline"``.

    Raises:
        KeyError: If *complexity* is not a recognised value.
    """
    return _COMPLEXITY_TO_MODEL[complexity]


@dataclass
class RoutedIssue:
    """An issue paired with its resolved domain config and logical model."""

    issue: Issue
    domain_key: str
    domain_config: DomainConfig
    logical_model: str


def route_issue(issue: Issue, config: AutoworkConfig) -> RoutedIssue:
    """Resolve *issue* to a domain config, falling back to ``fallback_domain``.

    Args:
        issue: The issue to route.
        config: The parsed autowork config.

    Returns:
        A :class:`RoutedIssue` with the matched domain key, config, and
        logical model derived from the domain's complexity setting.
    """
    if issue.domain in config.domains:
        domain_key = issue.domain
        domain_config = config.domains[issue.domain]
    else:
        domain_key = "fallback"
        domain_config = config.fallback_domain

    logical_model = complexity_to_model(domain_config.complexity)
    return RoutedIssue(
        issue=issue,
        domain_key=domain_key,
        domain_config=domain_config,
        logical_model=logical_model,
    )
