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
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic

# Local
from .. import utils

# Typing
from typing import Optional, Type


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
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds enum pydantic field to argument parser.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Extract Enum
    enum_type: Type[enum.Enum] = field.outer_type_

    # Compute Argument Intrinsics
    is_flag = len(enum_type) == 1 and not bool(field.required)
    is_inverted = is_flag and field.get_default() is not None and field.allow_none

    # Determine Argument Properties
    metavar = f"{{{', '.join(e.name for e in enum_type)}}}"
    action = argparse._StoreConstAction if is_flag else argparse._StoreAction
    const = (
        {}
        if not is_flag
        else {"const": None}
        if is_inverted
        else {"const": list(enum_type)[0]}
    )

    # Add Enum Field
    parser.add_argument(
        utils.arguments.name(field, is_inverted),
        action=action,
        help=utils.arguments.description(field),
        dest=field.alias,
        metavar=metavar,
        required=bool(field.required),
        **const,  # type: ignore[arg-type]
    )

    # Construct and Return Validator
    return utils.pydantic.as_validator(field, lambda v: enum_type[v])
