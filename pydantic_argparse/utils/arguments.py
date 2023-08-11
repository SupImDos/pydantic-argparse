"""Arguments Utility Functions for Declarative Typed Argument Parsing.

The `arguments` module contains utility functions used for formatting argument
names and formatting argument descriptions.
"""


# Third-Party
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic


def name(field: pydantic.fields.ModelField, invert: bool = False) -> str:
    """Standardises argument name.

    Args:
        field (pydantic.fields.ModelField): Field to construct name for.
        invert (bool): Whether to invert the name by prepending `--no-`.

    Returns:
        str: Standardised name of the argument.
    """
    # Construct Prefix
    prefix = "--no-" if invert else "--"

    # Prepend prefix, replace '_' with '-'
    return f"{prefix}{field.alias.replace('_', '-')}"


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
