"""Parses Standard Pydantic Fields to Command-Line Arguments.

The `standard` module contains the `parse_field` function, which parses
standard `pydantic` model fields to `ArgumentParser` command-line arguments.

Unlike the other `parser` modules, the `standard` module does not contain a
`should_parse` function. This is because it is the fallback case, where fields
that do not match any other types and require no special handling are parsed.
"""


# Standard
import argparse

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
) -> None:
    """Adds standard pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Default
    default = field.get_default()

    # All other types are treated in a standard way
    if field.required:
        # Add Required Standard Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,
            help=utils.argument_description(field.field_info.description),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=True,
        )

    else:
        # Add Optional Standard Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )
