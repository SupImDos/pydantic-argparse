"""container.py

Provides functions to parse container fields.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import annotations


# Standard
import argparse

# Third-Party
import pydantic

# Local
from ..utils import argument_description, argument_name


def parse_container_field(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds standard pydantic field to argument parser.

    Args:
        parser: (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # List, Tuple, Set, FrozenSet, Deque
    if field.required:
        # Required
        _parse_container_field_required(parser, field)

    else:
        # Optional
        _parse_container_field_optional(parser, field)


def _parse_container_field_required(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds required container pydantic field to argument parser.

    Args:
        parser: (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Add Required Container Field
    parser.add_argument(
        argument_name(field.name),
        action=argparse._StoreAction,  # pylint: disable=protected-access
        nargs=argparse.ONE_OR_MORE,
        help=argument_description(field.field_info.description),
        dest=field.name,
        required=True,
    )


def _parse_container_field_optional(
    parser: argparse.ArgumentParser,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds optional container pydantic field to argument parser.

    Args:
        parser: (argparse.ArgumentParser): Argument parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Get Default
    default = field.get_default()

    # Add Optional Container Field
    parser.add_argument(
        argument_name(field.name),
        action=argparse._StoreAction,  # pylint: disable=protected-access
        nargs=argparse.ONE_OR_MORE,
        default=default,
        help=argument_description(field.field_info.description, default),
        dest=field.name,
        required=False,
    )
