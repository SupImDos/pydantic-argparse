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
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic

# Local
from .. import utils

# Typing
from typing import Optional

# Version-Guarded
if sys.version_info < (3, 8):  # pragma: <3.8 cover
    from typing_extensions import Literal, get_args
else:  # pragma: >=3.8 cover
    from typing import Literal, get_args


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
    # Extract Choices
    choices = get_args(field.outer_type_)

    # Compute Argument Intrinsics
    is_flag = len(choices) == 1 and not bool(field.required)
    is_inverted = is_flag and field.get_default() is not None and field.allow_none

    # Determine Argument Properties
    metavar = f"{{{', '.join(str(c) for c in choices)}}}"
    action = argparse._StoreConstAction if is_flag else argparse._StoreAction
    const = (
        {} if not is_flag else {"const": None} if is_inverted else {"const": choices[0]}
    )

    # Add Literal Field
    parser.add_argument(
        utils.arguments.name(field, is_inverted),
        action=action,
        help=utils.arguments.description(field),
        dest=field.alias,
        metavar=metavar,
        required=bool(field.required),
        **const,  # type: ignore[arg-type]
    )

    # Construct String Representation Mapping of Choices
    # This allows us O(1) parsing of choices from strings
    mapping = {str(choice): choice for choice in choices}

    # Construct and Return Validator
    return utils.pydantic.as_validator(field, lambda v: mapping[v])
