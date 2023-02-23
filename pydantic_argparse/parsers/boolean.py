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

# Typing
from typing import Optional

# Local
from pydantic_argparse import utils
from pydantic_argparse.argparse import actions


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as a `boolean`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `boolean`.
    """
    # Check and Return
    return utils.types.is_field_a(field, bool)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
) -> Optional[utils.types.ValidatorT]:
    """Adds boolean pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.

    Returns:
        Optional[utils.types.ValidatorT]: Possible validator casting function.
    """
    # Get Default
    default = field.get_default()

    # Booleans can be treated as required or optional flags
    if field.required:
        # Add Required Boolean Field
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=actions.BooleanOptionalAction,
            help=utils.arguments.description(field.field_info.description),
            dest=field.alias,
            required=True,
        )

    elif default:
        # Add Optional Boolean Field (Default True)
        parser.add_argument(
            utils.arguments.name(f"no-{field.alias}"),
            action=argparse._StoreFalseAction,
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            required=False,
        )

    else:
        # Add Optional Boolean Field (Default False)
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreTrueAction,
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            required=False,
        )

    # Return
    return None
