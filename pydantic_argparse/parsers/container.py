"""Parses Container Pydantic Fields to Command-Line Arguments.

The `container` module contains the `should_parse` function, which checks
whether this module should be used to parse the field, as well as the
`parse_field` function, which parses container `pydantic` model fields to
`ArgumentParser` command-line arguments.
"""


# Standard
import argparse
import collections.abc
import enum

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as a `container`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `container`.
    """
    # Check and Return
    return (
        utils.is_field_a(field, collections.abc.Container)
        and not utils.is_field_a(field, (collections.abc.Mapping, enum.Enum, str, bytes))
    )


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds container pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Default
    default = field.get_default()

    # Container Types
    if field.required:
        # Add Required Container Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            nargs=argparse.ONE_OR_MORE,
            help=utils.argument_description(field.field_info.description),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=True,
        )

    else:
        # Add Optional Container Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            nargs=argparse.ONE_OR_MORE,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )
