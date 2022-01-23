"""boolean.py

Provides functions to parse boolean fields.

@author Hayden Richards <SupImDos@gmail.com>
"""


# Standard
import argparse

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils


def parse_boolean_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds boolean pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Booleans can be treated as required or optional flags
    if field.required:
        # Required
        _parse_boolean_field_required(parser, field)

    else:
        # Optional
        _parse_boolean_field_optional(parser, field)


def _parse_boolean_field_required(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds required boolean pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Add Required Boolean Field
    parser.add_argument(
        utils.argument_name(field.name),
        action=argparse.BooleanOptionalAction,
        help=utils.argument_description(field.field_info.description),
        dest=field.name,
        required=True,
    )


def _parse_boolean_field_optional(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds optional boolean pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Default
    default = field.get_default()

    # Add Optional Boolean Field
    if default:
        # Optional (Default True)
        parser.add_argument(
            utils.argument_name("no-" + field.name),
            action=argparse._StoreFalseAction,  # pylint: disable=protected-access
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.name,
            required=False,
        )

    else:
        # Optional (Default False)
        parser.add_argument(
            utils.argument_name(field.name),
            action=argparse._StoreTrueAction,  # pylint: disable=protected-access
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.name,
            required=False,
        )
