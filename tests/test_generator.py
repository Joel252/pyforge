from pathlib import Path

import pytest

from pyforge.templates.generator import ProjectGenerator
from pyforge.templates.loader import load_template


def test_project_generator(tmp_path: Path) -> None:
    template_path = Path("templates/script")

    template = load_template(template_path)

    generator = ProjectGenerator(template)

    destination = tmp_path / "my-project"

    generator.generate(
        destination,
        {
            "project_name": "my-project",
            "package_name": "my_project",
            "description": "My test project",
        },
    )

    assert (destination / "README.md").exists()
    assert (destination / "pyproject.toml").exists()
    assert (destination / "src" / "my_project" / "main.py").exists()
    assert (destination / "tests" / "test_main.py").exists()


def test_generator_requires_variables(tmp_path: Path) -> None:
    template_path = tmp_path / "template"
    template_path.mkdir()

    files_path = template_path / "files"
    files_path.mkdir()

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

    (files_path / "README.md.j2").write_text(
        "# {{ project_name }}",
        encoding="utf-8",
    )

    template = load_template(template_path)
    generator = ProjectGenerator(template)

    with pytest.raises(ValueError, match="project_name"):
        generator.generate(tmp_path / "output", {})
