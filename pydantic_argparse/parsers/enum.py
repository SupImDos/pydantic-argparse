"""enum.py

Provides functions to parse enum fields.

@author Hayden Richards <SupImDos@gmail.com>
"""


# Standard
import argparse
import enum

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils

# Typing
from typing import TypeVar  # pylint: disable=wrong-import-order


# Constants
EnumT = TypeVar("EnumT", bound=enum.Enum)


def parse_enum_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Enums are treated as choices
    if field.required:
        # Required
        _parse_enum_field_required(parser, field)

    else:
        # Optional
        _parse_enum_field_optional(parser, field)


def _parse_enum_field_required(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds required enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Enum Type
    enum_type: type[enum.Enum] = field.outer_type_

    # Define Custom Type Caster
    caster = utils.type_caster(field.name, _arg_to_enum_member, enum_type=enum_type)

    # Add Required Enum Field
    parser.add_argument(
        utils.argument_name(field.name),
        action=argparse._StoreAction,  # pylint: disable=protected-access
        type=caster,
        choices=enum_type,
        help=utils.argument_description(field.field_info.description),
        dest=field.name,
        metavar=field.name.upper(),
        required=True,
    )


def _parse_enum_field_optional(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds optional enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Enum Type
    enum_type: type[enum.Enum] = field.outer_type_

    # Define Custom Type Caster
    caster = utils.type_caster(field.name, _arg_to_enum_member, enum_type=enum_type)

    # Get Default
    default = field.get_default()

    # Add Optional Enum Field
    if len(enum_type) == 1:
        # Optional Flag
        if default is not None and field.allow_none:
            # Optional Flag (Default Not None)
            parser.add_argument(
                utils.argument_name("no-" + field.name),
                action=argparse._StoreConstAction,  # pylint: disable=protected-access
                const=None,
                default=default,
                help=utils.argument_description(field.field_info.description, default),
                dest=field.name,
                metavar=field.name.upper(),
                required=False,
            )

        else:
            # Optional Flag (Default None)
            parser.add_argument(
                utils.argument_name(field.name),
                action=argparse._StoreConstAction,  # pylint: disable=protected-access
                const=list(enum_type)[0],
                default=default,
                help=utils.argument_description(field.field_info.description, default),
                dest=field.name,
                metavar=field.name.upper(),
                required=False,
            )

    else:
        # Optional Choice
        parser.add_argument(
            utils.argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=caster,
            choices=enum_type,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.name,
            metavar=field.name.upper(),
            required=False,
        )


def _arg_to_enum_member(
    argument: str,
    enum_type: type[EnumT],
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
