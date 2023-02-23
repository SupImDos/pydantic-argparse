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

# Typing
from typing import Any, Dict, Optional, Type, TypeVar, Union

# Local
from pydantic_argparse import utils


# Constants
T = TypeVar("T")


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as a `mapping`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `mapping`.
    """
    # Check and Return
    return utils.types.is_field_a(field, collections.abc.Mapping)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
) -> Optional[utils.types.ValidatorT]:
    """Adds mapping pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.

    Returns:
        Optional[utils.types.ValidatorT]: Possible validator casting function.
    """
    # Get Default
    default = field.get_default()

    # Mapping
    if field.required:
        # Add Required Mapping Field
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreAction,
            help=utils.arguments.description(field.field_info.description),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=True,
        )

    else:
        # Add Optional Mapping Field
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreAction,
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )

    # Define Custom Type Caster
    def __arg_to_dictionary(cls: Type[Any], value: T) -> Union[T, None, Dict]:
        if not value:
            return None
        if not isinstance(value, str):
            return value
        return ast.literal_eval(value)  # type: ignore[no-any-return]

    # Return Caster
    return __arg_to_dictionary
