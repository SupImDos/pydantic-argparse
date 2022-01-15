"""literal.py

Provides functions to parse literal fields.

@author Hayden Richards <SupImDos@gmail.com>
"""


# Standard
import argparse

# Third-Party
import pydantic
import typing_inspect

# Local
from pydantic_argparse import utils

# Typing
from typing import TypeVar  # pylint: disable=wrong-import-order


# Constants
T = TypeVar("T")


def parse_literal_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Literals are treated as constant flags, or choices
    if field.required:
        # Required
        _parse_literal_field_required(parser, field)

    else:
        # Optional
        _parse_literal_field_optional(parser, field)


def _parse_literal_field_required(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds required literal pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get choices from literal
    choices = list(typing_inspect.get_args(field.outer_type_))

    # Define Custom Type Caster
    caster = utils.type_caster(field.name, _arg_to_choice, choices=choices)

    # Add Required Literal Field
    parser.add_argument(
        utils.argument_name(field.name),
        action=argparse._StoreAction,  # pylint: disable=protected-access
        type=caster,
        choices=choices,
        help=utils.argument_description(field.field_info.description),
        dest=field.name,
        metavar=field.name.upper(),
        required=True,
    )


def _parse_literal_field_optional(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds optional literal pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get choices from literal
    choices = list(typing_inspect.get_args(field.outer_type_))

    # Define Custom Type Caster
    caster = utils.type_caster(field.name, _arg_to_choice, choices=choices)

    # Get Default
    default = field.get_default()

    # Add Optional Literal Field
    if len(choices) == 1:
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
                const=choices[0],
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
            choices=choices,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.name,
            metavar=field.name.upper(),
            required=False,
        )


def _arg_to_choice(
    argument: str,
    choices: list[T],
    ) -> T:
    """Attempts to convert string argument to a supplied choice.

    Args:
        argument (str): Possible choice.
        choices (list[T]): List of choices.

    Returns:
        T: Selected choice.

    Raises:
        ValueError: Raised if argument is not one of the choices.
    """
    # Attempt to convert string argument to one of choices
    for choice in choices:
        if str(choice) == argument:
            return choice

    # Raise Error
    raise ValueError
