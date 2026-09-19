from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    """Renderer for Jinja2 templates."""

    def __init__(self, template_path: Path) -> None:
        self.template_path = template_path
        self.environment = Environment(
            loader=FileSystemLoader(template_path),
            keep_trailing_newline=True,
        )

    def render_file(
        self, source: Path, destination: Path, context: dict[str, str]
    ) -> None:
        template = self.environment.get_template(
            source.relative_to(self.template_path).as_posix()
        )

        content = template.render(**context)

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
