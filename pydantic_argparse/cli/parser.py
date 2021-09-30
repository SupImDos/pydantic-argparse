#!/usr/bin/env python3
"""parser.py

Provides custom argument parser class.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Standard
import argparse
import collections
import enum

# Third-Party
import pydantic
import typing_inspect

# Typing
from typing import Generic, Literal, Optional, TypeVar  # pylint: disable=wrong-import-order


# Constants
PydanticModel = TypeVar("PydanticModel", bound=pydantic.BaseModel)


class ArgumentParser(argparse.ArgumentParser, Generic[PydanticModel]):
    """Custom Argument Parser.

    Args:
        prog (str): Program name for CLI.
        description (str): Program description for CLI.
        version (str): Program version string for CLI.
        model (type[PydanticModel]): Pydantic argument model class.
    """
    def __init__(
        self,
        prog: str,
        description: str,
        version: str,
        model: type[PydanticModel],
        ) -> None:
        """Constructs Custom Argument Parser."""
        # Initialise Super Class
        super().__init__(
            prog=prog,
            description=description,
            add_help=False,  # Disable the automatic help flag.
        )

        # Set Version and Model
        self.version = version
        self.model = model

        # Add Arguments Groups
        self._required_group = self.add_argument_group("required arguments")
        self._optional_group = self.add_argument_group("optional arguments")
        self._help_group = self.add_argument_group("help")

        # Add Arguments from model
        self._add_model(model)

        # Add Help and Version Flags
        self._help_group.add_argument(
            "-h",
            "--help",
            action=argparse._HelpAction,
            help="show this help message and exit",
        )
        self._help_group.add_argument(
            "-v",
            "--version",
            action=argparse._VersionAction,
            help="show program's version number and exit",
        )

    def parse_typed_args(
        self,
        args: Optional[list[str]]=None,
        ) -> PydanticModel:
        """Parses command line arguments.

        Args:
            args (Optional[list[str]]): Optional list of arguments to parse

        Returns:
            PydanticModel: Typed arguments.
        """
        # Call Super Class Method
        namespace = self.parse_args(args, None)

        # Handle Possible Validation Errors
        try:
            # Convert Namespace to Pydantic Model
            model = self.model.parse_obj(namespace.__dict__)

        except pydantic.ValidationError as exc:
            # Catch exception, and use the ArgumentParser.error() method
            # to report it to the user
            super().error(str(exc))

        # Return
        return model

    def _add_model(self, model: type[PydanticModel]) -> None:
        """Adds pydantic model to argument parser.

        Args:
            model (type[PydanticModel]): Pydantic model class to add to the
                argument parser.
        """
        # Add Arguments to Parser
        for field in model.__fields__.values():
            # Get Field Type and Possible Origin
            field_type = field.outer_type_
            field_origin = typing_inspect.get_origin(field_type)

            # Switch on Field Type
            if field_type is bool:
                # Booleans are always treated as optional flags
                self._optional_group.add_argument(
                    f"--{field.name.replace('_', '-')}",
                    action=argparse.BooleanOptionalAction,
                    default=bool(field.default),
                    help=field.field_info.description,
                    dest=field.name,
                    required=False,
                )

            elif field_origin in (collections.deque, frozenset, list, set, tuple):
                # Deque, FrozenSet, List, Set Tuple
                if field.required:
                    self._required_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._AppendAction,  # pylint: disable=protected-access
                        help=field.field_info.description,
                        dest=field.name,
                        required=True,
                    )

                else:
                    self._optional_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._AppendAction,  # pylint: disable=protected-access
                        default=field.default,
                        help=field.field_info.description,
                        dest=field.name,
                        required=False,
                    )

            elif field_origin is Literal:
                # Literal types are treated as constant flags
                constants = typing_inspect.get_args(field_type)
                if len(constants) > 1:
                    self._optional_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._StoreAction,  # pylint: disable=protected-access
                        choices=constants,
                        default=field.default,
                        help=f"{field.field_info.description} (default: {field.default})",
                        dest=field.name,
                        required=bool(field.required),
                    )
                else:
                    self._optional_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._StoreConstAction,  # pylint: disable=protected-access
                        const=constants[0],
                        default=field.default,
                        help=f"{field.field_info.description} (default: {field.default})",
                        dest=field.name,
                        required=False,
                    )

            elif isinstance(field_type, type) and issubclass(field_type, enum.Enum):
                # Enums are treated as choices
                if field.required:
                    self._required_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._StoreAction,  # pylint: disable=protected-access
                        type=field_type,
                        choices=field_type,
                        help=field.field_info.description,
                        dest=field.name,
                        required=True,
                    )

                else:
                    self._optional_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._StoreAction,  # pylint: disable=protected-access
                        type=field_type,
                        choices=field_type,
                        default=field.default,
                        help=f"{field.field_info.description} (default: {field.default})",
                        dest=field.name,
                        required=False,
                    )

            else:
                # All other types are treated normally
                if field.required:
                    self._required_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._StoreAction,  # pylint: disable=protected-access
                        help=field.field_info.description,
                        dest=field.name,
                        required=True,
                    )

                else:
                    self._optional_group.add_argument(
                        f"--{field.name.replace('_', '-')}",
                        action=argparse._StoreAction,  # pylint: disable=protected-access
                        default=field.default,
                        help=f"{field.field_info.description} (default: {field.default})",
                        dest=field.name,
                        required=False,
                    )
