"""Parses Literal Pydantic Fields to Command-Line Arguments.

The `literal` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses literal `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse
import typing

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils

# Typing
from typing import Any, Iterable, Literal, TypeVar  # pylint: disable=wrong-import-order


# Constants
T = TypeVar("T")


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as a `literal`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `literal`.
    """
    # Check and Return
    return utils.is_field_a(field, Literal)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get choices from literal
    choices = list(typing.get_args(field.outer_type_))

    # Define Custom Type Caster
    caster = utils.type_caster(field.alias, _arg_to_choice, choices=choices)

    # Get Default
    default = field.get_default()

    # Literals are treated as constant flags, or choices
    if field.required:
        # Add Required Literal Field
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=caster,
            choices=choices,
            help=utils.argument_description(field.field_info.description),
            dest=field.alias,
            metavar=_iterable_choices_metavar(choices),
            required=True,
        )

    elif len(choices) > 1:
        # Add Optional Choice
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=caster,
            choices=choices,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            metavar=_iterable_choices_metavar(choices),
            required=False,
        )

    elif default is not None and field.allow_none:
        # Add Optional Flag (Default Not None)
        parser.add_argument(
            utils.argument_name(f"no-{field.alias}"),
            action=argparse._StoreConstAction,  # pylint: disable=protected-access
            const=None,
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )

    else:
        # Add Optional Flag (Default None)
        parser.add_argument(
            utils.argument_name(field.alias),
            action=argparse._StoreConstAction,  # pylint: disable=protected-access
            const=choices[0],
            default=default,
            help=utils.argument_description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
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


def _iterable_choices_metavar(iterable: Iterable[Any]) -> str:
    """Generates a string metavar from iterable choices.

    Args:
        iterable (Iterable[Any]): Iterable object to generate metavar for.

    Returns:
        str: Generated metavar
    """
    # Generate and Return
    return f"{{{', '.join(str(i) for i in iterable)}}}"
