"""Parses Enum Pydantic Fields to Command-Line Arguments.

The `enum` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses enum `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse
import enum

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils

# Typing
from typing import Type, TypeVar


# Constants
EnumT = TypeVar("EnumT", bound=enum.Enum)


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as an `enum`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as an `enum`.
    """
    # Check and Return
    return utils.types.is_field_a(field, enum.Enum)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
) -> None:
    """Adds enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Enum Type
    enum_type: Type[enum.Enum] = field.outer_type_

    # Define Custom Type Caster
    caster = utils.types.caster(field.alias, _arg_to_enum_member, enum_type=enum_type)

    # Get Default
    default = field.get_default()

    # Enums are treated as choices
    if field.required:
        # Add Required Enum Field
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreAction,
            type=caster,
            choices=enum_type,
            help=utils.arguments.description(field.field_info.description),
            dest=field.alias,
            metavar=_enum_choices_metavar(enum_type),
            required=True,
        )

    elif len(enum_type) > 1:
        # Add Optional Choice
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreAction,
            type=caster,
            choices=enum_type,
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            metavar=_enum_choices_metavar(enum_type),
            required=False,
        )

    elif default is not None and field.allow_none:
        # Add Optional Flag (Default Not None)
        parser.add_argument(
            utils.arguments.name(f"no-{field.alias}"),
            action=argparse._StoreConstAction,
            const=None,
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )

    else:
        # Add Optional Flag (Default None)
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreConstAction,
            const=list(enum_type)[0],
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )


def _arg_to_enum_member(
    argument: str,
    enum_type: Type[EnumT],
) -> EnumT:
    """Attempts to convert string argument to a supplied enum member.

    Args:
        argument (str): Possible name of enum member.
        enum_type (type[EnumT]): Enum type.

    Returns:
        EnumT: Member from specified enum.

    Raises:
        ValueError: Raised if enum member does not exist.
    """
    # Attempt to convert string argument to enum member
    try:
        return enum_type[argument]
    except KeyError as exc:
        raise ValueError from exc


def _enum_choices_metavar(enum_type: Type[EnumT]) -> str:
    """Generates a string metavar from enum choices.

    Args:
        enum_type (type[EnumT]): Enum type to generate metavar for.

    Returns:
        str: Generated metavar
    """
    # Generate and Return
    return f"{{{', '.join(e.name for e in enum_type)}}}"
