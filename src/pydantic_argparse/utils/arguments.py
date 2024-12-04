"""Arguments Utility Functions for Declarative Typed Argument Parsing.

The `arguments` module contains utility functions used for formatting argument
names and formatting argument descriptions.
"""

from pydantic_argparse.compatibility import pydantic


def names(field: pydantic.fields.ModelField, invert: bool = False) -> list[str]:
    """Standardises argument name.

    Args:
        field (pydantic.fields.ModelField): Field to construct name for.
        invert (bool): Whether to invert the name by prepending `--no-`.

    Returns:
        str: Standardised name of the argument.
    """
    # Construct Prefix
    prefix = "--no-" if invert else "--"

    flags = []

    # Add custom aliases
    aliases = field.field_info.extra.get("aliases", [])
    for alias in aliases:
        flags.append(f"{prefix}{alias.replace('_', '-')}")

    # Prepend prefix, replace '_' with '-'
    flags.append(f"{prefix}{field.alias.replace('_', '-')}")

    return flags


def description(field: pydantic.fields.ModelField) -> str:
    """Standardises argument description.

    Args:
        field (pydantic.fields.ModelField): Field to construct description for.

    Returns:
        str: Standardised description of the argument.
    """
    # Construct Default String
    default = f"(default: {field.get_default()})" if not field.required else None

    # Return Standardised Description String
    return " ".join(filter(None, [field.field_info.description, default]))
