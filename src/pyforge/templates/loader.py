from pathlib import Path

import yaml

from pyforge.templates.models import (
    Template,
    TemplateFile,
    TemplateVariable,
)


class TemplateLoadError(Exception):
    """Raised when a template manifest cannot be loaded."""


def _require_string(
    manifest: dict,
    field: str,
    manifest_path: Path,
) -> str:
    value = manifest.get(field)

    if not isinstance(value, str) or not value.strip():
        raise TemplateLoadError(
            f"Field '{field}' must be a non-empty string in {manifest_path}"
        )

    return value


def _load_variables(
    manifest: dict, manifest_path: Path
) -> tuple[TemplateVariable, ...]:
    """Load variables from the template manifest."""
    raw_variables = manifest.get("variables", [])

    if not isinstance(raw_variables, list):
        raise TemplateLoadError(
            f"Field 'variables' must be a list in {manifest_path}"
        )

    variables = []
    for variable in raw_variables:
        if not isinstance(variable, dict):
            raise TemplateLoadError(
                f"Each variable must be an object in {manifest_path}"
            )

        name = variable.get("name")
        required = variable.get("required", True)
        prompt = variable.get("prompt")
        default = variable.get("default")

        if not isinstance(name, str) or not name.strip():
            raise TemplateLoadError(
                f"Variable 'name' must be a non-empty string in {manifest_path}"
            )

        if not isinstance(required, bool):
            raise TemplateLoadError(
                f"Variable 'required' must be a boolean in {manifest_path}"
            )

        if prompt and not isinstance(prompt, str):
            raise TemplateLoadError(
                f"Variable 'prompt' must be a string in {manifest_path}"
            )

        if default and not isinstance(default, str):
            raise TemplateLoadError(
                f"Variable 'default' must be a string in {manifest_path}"
            )

        variables.append(
            TemplateVariable(
                name=name,
                required=required,
                prompt=prompt,
                default=default,
            )
        )

    return tuple(variables)


def _load_files(manifest: dict, manifest_path: Path) -> tuple[TemplateFile, ...]:
    """Load files from the template manifest."""
    raw_files = manifest.get("files", [])

    if not isinstance(raw_files, list):
        raise TemplateLoadError(
            f"Field 'files' must be a list in {manifest_path}"
        )

    files = []
    for file in raw_files:
        if not isinstance(file, dict):
            raise TemplateLoadError(
                f"Each file must be an object in {manifest_path}"
            )

        source = file.get("source")
        destination = file.get("destination")

        if not isinstance(source, str) or not source.strip():
            raise TemplateLoadError(
                f"File 'source' must be a non-empty string in {manifest_path}"
            )

        if not isinstance(destination, str) or not destination.strip():
            raise TemplateLoadError(
                f"File 'destination' must be a non-empty string in {manifest_path}"
            )

        files.append(TemplateFile(source=source, destination=destination))

    return tuple(files)


def load_template(template_path: Path) -> Template:
    """Load a yaml template from the given path."""
    manifest_path = template_path / "template.yaml"

    if not manifest_path.exists():
        raise TemplateLoadError(
            f"Template manifest not found at {manifest_path}"
        )

    try:
        with manifest_path.open("r", encoding="utf-8") as file:
            manifest = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise TemplateLoadError(f"Invalid YAML in {manifest_path}") from e

    if not isinstance(manifest, dict):
        raise TemplateLoadError(
            f"Template manifest must contain an object: {manifest_path}"
        )

    return Template(
        name=_require_string(manifest, "name", manifest_path),
        version=_require_string(manifest, "version", manifest_path),
        description=_require_string(manifest, "description", manifest_path),
        path=template_path,
        variables=_load_variables(manifest, manifest_path),
        files=_load_files(manifest, manifest_path),
    )
