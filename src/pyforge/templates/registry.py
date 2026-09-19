from pathlib import Path

from pyforge.templates.loader import TemplateLoadError, load_template
from pyforge.templates.models import Template


class TemplateNotFoundError(Exception):
    """Raised when a template cannot be found."""


class DuplicateTemplateError(Exception):
    """Raised when multiple templates use the same name."""


class TemplateRegistry:
    """Registry for managing project templates."""

    def __init__(self, templates_path: Path) -> None:
        self.templates_path = templates_path

    def discover(self) -> list[Template]:
        """Discover and return a list of available templates."""
        templates: list[Template] = []
        names: set[str] = set()

        if not self.templates_path.exists():
            return templates

        for template_path in self.templates_path.iterdir():
            if not template_path.is_dir():
                continue

            try:
                template = load_template(template_path)
            except TemplateLoadError:
                continue  # Skip templates that fail to load

            if template.name in names:
                raise DuplicateTemplateError(
                    f"Duplicate template name found: {template.name}"
                )

            names.add(template.name)
            templates.append(template)

        return sorted(templates, key=lambda t: t.name)

    def get(self, name: str) -> Template:
        """Get a template by name."""
        for template in self.discover():
            if template.name == name:
                return template

        raise TemplateNotFoundError(f"Template not found: {name}")
