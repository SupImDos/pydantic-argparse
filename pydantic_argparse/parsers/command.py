"""Parses Nested Pydantic Model Fields to Sub-Commands.

The `command` module contains the `should_parse` function, which checks whether
this module should be used to parse the field, as well as the `parse_field`
function, which parses nested `pydantic` model fields to `ArgumentParser`
sub-commands.
"""


# Standard
import argparse

# Third-Party
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic

# Typing
from typing import Optional

# Local
from .. import utils


def should_parse(field: pydantic.fields.ModelField) -> bool:
    """Checks whether the field should be parsed as a `command`.

    Args:
        field (pydantic.fields.ModelField): Field to check.

    Returns:
        bool: Whether the field should be parsed as a `command`.
    """
    # Check and Return
    return utils.types.is_field_a(field, pydantic.BaseModel)


def parse_field(
    subparser: argparse._SubParsersAction,
    field: pydantic.fields.ModelField,
) -> Optional[utils.pydantic.PydanticValidator]:
    """Adds command pydantic field to argument parser.

    Args:
        subparser (argparse._SubParsersAction): Sub-parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.

    Returns:
        Optional[utils.pydantic.PydanticValidator]: Possible validator method.
    """
    # Add Command
    subparser.add_parser(
        field.alias,
        help=field.field_info.description,
        model=field.outer_type_,  # type: ignore[call-arg]
        exit_on_error=False,  # Allow top level parser to handle exiting
    )

    # Return
    return None
