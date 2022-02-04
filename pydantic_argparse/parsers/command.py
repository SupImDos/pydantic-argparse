"""Parses Nested Pydantic Model Fields to Sub-Commands.

The `command` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses nested `pydantic` model fields to `ArgumentParser`
sub-commands.
"""


# Standard
import argparse

# Third-Party
import pydantic


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether this field should be parsed as a `command`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether this field should be parsed as a `command`.
    """
    # Check and Return
    return isinstance(field.outer_type_, pydantic.main.ModelMetaclass)


def parse_field(
    subparser: argparse._SubParsersAction,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds command pydantic field to argument parser.

    Args:
        subparser (argparse._SubParsersAction): Sub-parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Add Command
    subparser.add_parser(
        field.name,
        help=field.field_info.description,
        model=field.outer_type_,
        exit_on_error=False,  # Allow top level parser to handle exiting
    )
