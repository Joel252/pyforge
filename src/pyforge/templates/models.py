from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TemplateVariable:
    """Represents a variable in a project template."""

    name: str
    required: bool = True
    prompt: str | None = None
    default: str | None = None


@dataclass(frozen=True)
class TemplateFile:
    """Represents a file in a project template."""

    source: str
    destination: str


@dataclass(frozen=True)
class Template:
    """Represents a project template."""

    name: str
    version: str
    description: str
    path: Path
    variables: tuple[TemplateVariable, ...]
    files: tuple[TemplateFile, ...]
