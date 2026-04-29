"""AutoworkConfig — Pydantic model and loader for autowork.yaml (Task 7)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


class ConfigError(ValueError):
    """Raised when autowork.yaml is missing, malformed, or fails validation."""


class DomainConfig(BaseModel):
    """Configuration for a single work domain."""

    model_config = {"populate_by_name": True}

    stack: str
    validate_cmd: str = Field(alias="validate")
    docs: list[str] = []
    complexity: Literal["high", "standard", "mechanical"]

    @field_validator("validate_cmd")
    @classmethod
    def validate_nonempty(cls, v: str) -> str:
        if not v:
            raise ValueError("'validate' must be a non-empty string")
        return v


class IssueSourceConfig(BaseModel):
    """Configuration for the issue source."""

    default: Literal["auto", "github", "markdown"] = "auto"
    markdown_path: str = ".forge/issues.md"
    priority_labels: list[str] = []


class OrchestrationConfig(BaseModel):
    """Configuration for orchestration behaviour."""

    max_retries_per_criterion: int = 3
    max_review_cycles: int = 2
    commit_scope_from_domain: bool = True
    branch_prefix: dict[str, str] = {"github": "issue", "markdown": "autowork"}


class PRConfig(BaseModel):
    """Configuration for pull-request creation and merging."""

    merge_method: Literal["squash", "merge", "rebase"] = "squash"
    delete_branch_on_merge: bool = True
    review_primitive: Literal["auto", "f3", "builtin"] = "auto"


class AutoworkConfig(BaseModel):
    """Top-level Pydantic model for autowork.yaml."""

    domains: dict[str, DomainConfig]
    fallback_domain: DomainConfig = DomainConfig.model_validate(
        {"stack": "python", "validate": "pytest -x", "docs": [], "complexity": "standard"}
    )
    issue_source: IssueSourceConfig = IssueSourceConfig()
    orchestration: OrchestrationConfig = OrchestrationConfig()
    pr: PRConfig = PRConfig()


def load_config_from_dict(data: dict[str, Any]) -> AutoworkConfig:
    """Validate *data* against :class:`AutoworkConfig`.

    Args:
        data: Parsed YAML dict.

    Returns:
        A validated :class:`AutoworkConfig` instance.

    Raises:
        ConfigError: If ``domains`` is absent/empty or Pydantic validation fails.
    """
    if "domains" not in data or not data["domains"]:
        raise ConfigError("autowork.yaml must contain a non-empty 'domains' mapping.")

    try:
        return AutoworkConfig(**data)
    except (ValidationError, TypeError) as exc:
        raise ConfigError(f"autowork.yaml does not match expected schema: {exc}") from exc


def load_config(path: Path) -> AutoworkConfig:
    """Read and validate an autowork.yaml file.

    Args:
        path: Path to the autowork YAML file.

    Returns:
        A validated :class:`AutoworkConfig` instance.

    Raises:
        ConfigError: If the file is not found, contains invalid YAML, or fails
            schema validation.
    """
    if not path.is_file():
        raise ConfigError(f"autowork config not found: {path}")

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Failed to parse {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError(f"{path} must be a YAML mapping, got {type(raw).__name__}.")

    return load_config_from_dict(raw)
