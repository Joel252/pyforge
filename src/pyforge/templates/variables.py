import typer

from pyforge.templates.models import Template, TemplateVariable


class VariableResolver:
    """"""

    def __init__(self, template: Template, initial_context: dict[str, str]) -> None:
        self.template = template
        self.context = dict(initial_context)

    @staticmethod
    def _ask(variable: TemplateVariable) -> str | None:
        """"""
        prompt = variable.prompt or variable.name

        return typer.prompt(
            prompt,
            default=variable.default or "",
            show_default=bool(variable.default),
        )

    def resolve(self) -> dict[str, str]:
        """"""

        for variable in self.template.variables:
            if variable.name in self.context:
                continue

            value = self._ask(variable)

            if value:
                self.context[variable.name] = value

        return self.context
