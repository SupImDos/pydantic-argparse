"""command.py

Provides functions to parse command fields.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import annotations


# Standard
import argparse

# Third-Party
import pydantic

# Typing
from typing import Optional  # pylint: disable=wrong-import-order


def parse_command_field(
    grandparent_command: Optional[str],
    subparser: argparse._SubParsersAction,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds command pydantic field to argument parser.

    Args:
        grandparent_command (Optional[str]): Grandparent command for parser.
        subparser: (argparse._SubParsersAction): Sub-parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Construct Parent Command with Prefix
    parent_command = ".".join(filter(None, (grandparent_command, field.name)))

    # Add Command
    subparser.add_parser(
        field.name,
        help=field.field_info.description,
        model=field.outer_type_,
        parent_command=parent_command,
    )
