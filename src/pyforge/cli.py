from pathlib import Path

import typer
from jinja2 import TemplateNotFound
from rich.console import Console
from rich.table import Table

from pyforge import __version__
from pyforge.paths import get_builtin_templates_path
from pyforge.templates import TemplateRegistry
from pyforge.templates.generator import ProjectGenerator
from pyforge.templates.variables import VariableResolver

app = typer.Typer(
    name="pyforge",
    help="Lightweight Python project scaffolding tool.",
    no_args_is_help=True,
)

console = Console()


@app.command()
def version() -> None:
    """Show the pyforge version."""
    console.print(f"pyforge version: {__version__}")


@app.command()
def list_templates() -> None:
    """List available project templates."""
    registry = TemplateRegistry(get_builtin_templates_path())
    templates = registry.discover()

    if not templates:
        console.print("No templates found.")
        return

    table = Table(title="Available Templates")

    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Description")

    for template in templates:
        table.add_row(
            template.name,
            template.version,
            template.description,
        )

    console.print(table)


@app.command()
def new(
    name: str,
    template: str = typer.Option(
        ...,
        "--template",
        "-t",
        help="The template to use for the new project.",
    ),
) -> None:
    """Create a new project from a template."""
    registry = TemplateRegistry(get_builtin_templates_path())

    try:
        selected_template = registry.get(template)
    except TemplateNotFound:
        console.print(f"[red]Template not found:[/red] {template}")
        raise typer.Exit(code=1)

    destination = Path.cwd() / name

    if destination.exists():
        console.print(f"[red]Destination already exists:[/red] {destination}")
        raise typer.Exit(code=1)

    package_name = name.replace("-", "_")

    resolver = VariableResolver(
        selected_template,
        {
            "project_name": name,
            "package_name": package_name,
        },
    )

    context = resolver.resolve()

    generator = ProjectGenerator(selected_template)
    generator.generate(destination, context)

    console.print(f"[green]Created project:[/green] {destination}")


if __name__ == "__main__":
    app()
