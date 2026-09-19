from pathlib import Path

import pytest

from pyforge.templates.loader import TemplateLoadError, load_template
from pyforge.templates.registry import (
    DuplicateTemplateError,
    TemplateNotFoundError,
    TemplateRegistry,
)


def test_load_template(tmp_path: Path) -> None:
    template_path = tmp_path / "example"
    template_path.mkdir()

    (template_path / "template.yaml").write_text(
        """
name: example
version: 1.0.0
description: Example template

variables:
  - name: project_name
    required: true

files:
  - source: README.md.j2
    destination: README.md
""",
        encoding="utf-8",
    )

    template = load_template(template_path)

    assert len(template.variables) == 1
    assert template.variables[0].name == "project_name"
    assert template.variables[0].required is True

    assert len(template.files) == 1
    assert template.files[0].source == "README.md.j2"
    assert template.files[0].destination == "README.md"


def test_missing_manifest(tmp_path: Path) -> None:
    template_path = tmp_path / "example"
    template_path.mkdir()

    try:
        load_template(template_path)
    except TemplateLoadError as exc:
        assert "Template manifest not found" in str(exc)
    else:
        raise AssertionError("Expected TemplateLoadError")


def test_missing_required_field(tmp_path: Path) -> None:
    template_path = tmp_path / "example"
    template_path.mkdir()

    (template_path / "template.yaml").write_text(
        """
name: example
version: 1.0.0
""",
        encoding="utf-8",
    )

    try:
        load_template(template_path)
    except TemplateLoadError as exc:
        assert "description" in str(exc)
    else:
        raise AssertionError("Expected TemplateLoadError")


def test_registry_discovers_valid_templates(tmp_path: Path) -> None:
    template_path = tmp_path / "example"
    template_path.mkdir()

    (template_path / "template.yaml").write_text(
        """
name: example
version: 1.0.0
description: Example template
""",
        encoding="utf-8",
    )

    registry = TemplateRegistry(tmp_path)

    templates = registry.discover()

    assert len(templates) == 1
    assert templates[0].name == "example"


def test_registry_get_template(tmp_path: Path) -> None:
    template_path = tmp_path / "example"
    template_path.mkdir()

    (template_path / "template.yaml").write_text(
        """
name: example
version: 1.0.0
description: Example template
""",
        encoding="utf-8",
    )

    registry = TemplateRegistry(tmp_path)

    template = registry.get("example")

    assert template.name == "example"


def test_registry_template_not_found(tmp_path: Path) -> None:
    registry = TemplateRegistry(tmp_path)

    with pytest.raises(TemplateNotFoundError):
        registry.get("does-not-exist")


def test_registry_duplicate_template_name(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    first.mkdir()
    second.mkdir()

    manifest = """
name: example
version: 1.0.0
description: Example template
"""

    (first / "template.yaml").write_text(
        manifest,
        encoding="utf-8",
    )

    (second / "template.yaml").write_text(
        manifest,
        encoding="utf-8",
    )

    registry = TemplateRegistry(tmp_path)

    with pytest.raises(DuplicateTemplateError):
        registry.discover()
