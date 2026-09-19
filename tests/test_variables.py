from pathlib import Path

from pyforge.templates.models import (
    Template,
    TemplateVariable,
)
from pyforge.templates.variables import VariableResolver


def test_variable_resolver_keeps_initial_context() -> None:
    template = Template(
        name="example",
        version="1.0.0",
        description="Example",
        path=Path("."),
        variables=(
            TemplateVariable(
                name="description",
                required=True,
            ),
        ),
        files=(),
    )

    resolver = VariableResolver(
        template,
        {
            "description": "Existing description",
        },
    )

    context = resolver.resolve()

    assert context["description"] == "Existing description"
