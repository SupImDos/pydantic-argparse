"""Arguments Utility Functions for Declarative Typed Argument Parsing.

The `arguments` module contains utility functions used for formatting argument
names and formatting argument descriptions.
"""

from pydantic_argparse.compatibility import pydantic

from typing import List


def names(field: pydantic.fields.ModelField, invert: bool = False) -> List[str]:
    """Standardises the argument name and any custom aliases.

    Args:
        field (pydantic.fields.ModelField): Field to construct name for.
        invert (bool): Whether to invert the name by prepending `--no-`.

    Returns:
        List[str]: Standardised names for the argument.
    """
    # Add any custom aliases first
    # We trust that the user has provided these correctly
    flags: List[str] = []
    flags.extend(field.field_info.extra.get("aliases", []))

    # Construct prefix, prepend it, replace '_' with '-'
    prefix = "--no-" if invert else "--"
    flags.append(f"{prefix}{field.alias.replace('_', '-')}")

    # Return the standardised name and aliases
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
