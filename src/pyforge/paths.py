from pathlib import Path


def get_builtin_templates_path() -> Path:
    """Get the path to the built-in templates directory."""
    return Path(__file__).resolve().parents[2] / "templates"
