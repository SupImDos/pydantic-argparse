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
    """Checks whether this field should be parsed as a `literal`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether this field should be parsed as a `literal`.
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
    caster = utils.type_caster(field.name, ast.literal_eval)

    # Get Default
    default = field.get_default()

    # Mapping
    if field.required:
        # Add Required Mapping Field
        parser.add_argument(
            utils.argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=caster,
            help=utils.argument_description(field.field_info.description),
            dest=field.name,
            metavar=field.name.upper(),
            required=True,
        )

    else:
        # Add Optional Mapping Field
        parser.add_argument(
            utils.argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=caster,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.name,
            metavar=field.name.upper(),
            required=False,
        )
