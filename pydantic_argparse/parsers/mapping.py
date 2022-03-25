"""Parses Mapping Pydantic Fields to Command-Line Arguments.

The `mapping` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses mapping `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse
import ast
import collections.abc

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as a `mapping`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `mapping`.
    """
    # Check and Return
    return utils.is_field_a(field, collections.abc.Mapping)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds mapping pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Define Custom Type Caster
    caster = utils.type_caster(field.alias, ast.literal_eval)

    # Get Default
    default = field.get_default()

    # Mapping
    if field.required:
        # Add Required Mapping Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=caster,
            help=utils.argument_description(field.field_info.description),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=True,
        )

    else:
        # Add Optional Mapping Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=caster,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )
