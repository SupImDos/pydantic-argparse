"""Parses Literal Pydantic Fields to Command-Line Arguments.

The `literal` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses literal `pydantic` model fields to `ArgumentParser`
command-line arguments.
"""


# Standard
import argparse
import sys

# Third-Party
import pydantic

# Local
from pydantic_argparse import utils

# Typing
from typing import Any, Iterable, Optional, TypeVar

# Version-Guarded
if sys.version_info < (3, 8):  # pragma: <3.8 cover
    from typing_extensions import Literal, get_args
else:  # pragma: >=3.8 cover
    from typing import Literal, get_args


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
    return utils.types.is_field_a(field, Literal)


def parse_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Get choices from literal
    choices = list(get_args(field.outer_type_))

    # Get Default
    default = field.get_default()

    # Literals are treated as constant flags, or choices
    if field.required:
        # Add Required Literal Field
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreAction,
            help=utils.arguments.description(field.field_info.description),
            dest=field.alias,
            metavar=_iterable_choices_metavar(choices),
            required=True,
        )

    elif len(choices) > 1:
        # Add Optional Choice
        parser.add_argument(
            utils.arguments.name(field.alias),
            action=argparse._StoreAction,
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            metavar=_iterable_choices_metavar(choices),
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
            const=choices[0],
            help=utils.arguments.description(field.field_info.description, default),
            dest=field.alias,
            metavar=field.alias.upper(),
            required=False,
        )

    # Construct String Representation Mapping of Choices
    # This allows us O(1) parsing of choices from strings
    mapping = {str(choice): choice for choice in choices}

    # Construct and Return Validator
    return utils.pydantic.as_validator(field, lambda v: mapping[v])


def _iterable_choices_metavar(iterable: Iterable[Any]) -> str:
    """Generates a string metavar from iterable choices.

    Args:
        iterable (Iterable[Any]): Iterable object to generate metavar for.

    Returns:
        str: Generated metavar
    """
    # Generate and Return
    return f"{{{', '.join(str(i) for i in iterable)}}}"
