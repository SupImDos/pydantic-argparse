"""json.py

Provides functions to parse json fields.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import annotations


# Standard
import argparse
import ast

# Third-Party
import pydantic

# Local
from ..utils import argument_description, argument_name, type_caster


def parse_json_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds json pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # JSON (Dictionary)
    if field.required:
        # Required
        _parse_json_field_required(parser, field)

    else:
        # Optional
        _parse_json_field_optional(parser, field)


def _parse_json_field_required(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds required json pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Define Custom Type Caster
    caster = type_caster(field.name, ast.literal_eval)

    # Add Required JSON Field
    parser.add_argument(
        argument_name(field.name),
        action=argparse._StoreAction,  # pylint: disable=protected-access
        type=caster,
        help=argument_description(field.field_info.description),
        dest=field.name,
        required=True,
    )


def _parse_json_field_optional(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds optional json pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Define Custom Type Caster
    caster = type_caster(field.name, ast.literal_eval)

    # Get Default
    default = field.get_default()

    # Add Optional JSON Field
    parser.add_argument(
        argument_name(field.name),
        action=argparse._StoreAction,  # pylint: disable=protected-access
        type=caster,
        default=default,
        help=argument_description(field.field_info.description, default),
        dest=field.name,
        required=False,
    )
