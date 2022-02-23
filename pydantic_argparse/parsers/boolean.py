"""Parses Boolean Pydantic Fields to Command-Line Arguments.

The `boolean` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses boolean `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as a `boolean`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `boolean`.
    """
    # Check and Return
    return utils.is_field_a(field, bool)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds boolean pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Default
    default = field.get_default()

    # Booleans can be treated as required or optional flags
    if field.required:
        # Add Required Boolean Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse.BooleanOptionalAction,
            help=utils.argument_description(field.field_info.description),
            dest=field.alias,
            required=True,
        )

    elif default:
        # Add Optional Boolean Field (Default True)
        parser.add_argument(
            utils.argument_name(f"no-{field.alias}"),
            action=argparse._StoreFalseAction,  # pylint: disable=protected-access
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            required=False,
        )

    else:
        # Add Optional Boolean Field (Default False)
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreTrueAction,  # pylint: disable=protected-access
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            required=False,
        )
