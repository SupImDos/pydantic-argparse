"""command.py

Provides functions to parse command fields.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import annotations


# Standard
import argparse

# Third-Party
import pydantic


def parse_command_field(
    subparser: argparse._SubParsersAction,
    field: pydantic.fields.ModelField,
    ) -> None:
    """Adds command pydantic field to argument parser.

    Args:
        subparser: (argparse._SubParsersAction): Sub-parser to add to.
        field (pydantic.fields.ModelField): Field to be added to parser.
    """
    # Add Command
    subparser.add_parser(
        field.name,
        help=field.field_info.description,
        model=field.outer_type_,
    )
