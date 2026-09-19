from pathlib import Path

from jinja2 import Template as JinjaTemplate

from pyforge.templates.models import Template
from pyforge.templates.renderer import TemplateRenderer


class ProjectGenerator:
    """Generator for creating projects from templates."""

    def __init__(self, template: Template) -> None:
        self.template = template
        self.renderer = TemplateRenderer(template.path / "files")

    def generate(self, destination: Path, context: dict[str, str]) -> None:
        """Generate the project files from the template."""
        self._validate_context(context)

        for template_file in self.template.files:
            source = self.template.path / "files" / template_file.source

            if not source.exists():
                raise FileNotFoundError(
                    f"Template source file not found: {source}"
                )

            rendered_destination = self._render_string(
                template_file.destination, context
            )

            output_path = destination / rendered_destination

            self.renderer.render_file(source, output_path, context)

    def _validate_context(self, context: dict[str, str]) -> None:
        """Validate that all required variables are present in the context."""
        for variable in self.template.variables:
            if not variable.required:
                continue

            value = context.get(variable.name)
            if value is None or not value.strip():
                raise ValueError(
                    f"Required template variable '{variable.name}' is missing or empty."
                )

    @staticmethod
    def _render_string(value: str, context: dict[str, str]) -> str:
        """Render the string using the provided context."""
        return JinjaTemplate(value).render(**context)
