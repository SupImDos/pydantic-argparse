"""Parses Container Pydantic Fields to Command-Line Arguments.

The `container` module contains the `should_parse` function, which checks
whether this module should be used to parse the field, as well as the
`parse_field` function, which parses container `pydantic` model fields to
`ArgumentParser` command-line arguments.
"""


# Standard
import argparse
import collections.abc
import typing

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether this field should be parsed as a `container`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether this field should be parsed as a `container`.
    """
    # Get Field Type or Origin
    field_type = typing.get_origin(field.outer_type_) or field.outer_type_

    # Check and Return
    return all(
        (
            isinstance(field_type, type) and issubclass(field_type, collections.abc.Container),
            isinstance(field_type, type) and not issubclass(field_type, collections.abc.Mapping),
            field_type not in (str, bytes),
        )
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
            utils.argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            nargs=argparse.ONE_OR_MORE,
            help=utils.argument_description(field.field_info.description),
            dest=field.name,
            metavar=field.name.upper(),
            required=True,
        )

    else:
        # Add Optional Container Field
        parser.add_argument(
            utils.argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            nargs=argparse.ONE_OR_MORE,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.name,
            metavar=field.name.upper(),
            required=False,
        )
