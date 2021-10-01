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
PydanticModelT = TypeVar("PydanticModelT", bound=pydantic.BaseModel)
EnumT = TypeVar("EnumT", bound=enum.Enum)


class ArgumentParser(argparse.ArgumentParser, Generic[PydanticModelT]):
    """Custom Typed Argument Parser.

    Args:
        prog (str): Program name for CLI.
        description (str): Program description for CLI.
        version (str): Program version string for CLI.
        model (type[PydanticModelT]): Pydantic argument model class.
    """
    def __init__(
        self,
        prog: str,
        description: str,
        version: str,
        model: type[PydanticModelT],
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

        # Add Arguments from Model
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
        ) -> PydanticModelT:
        """Parses command line arguments.

        Args:
            args (Optional[list[str]]): Optional list of arguments to parse

        Returns:
            PydanticModelT: Typed arguments.
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

    def _add_model(self, model: type[PydanticModelT]) -> None:
        """Adds pydantic model to argument parser.

        Args:
            model (type[PydanticModelT]): Pydantic model class to add to the
                argument parser.
        """
        # Loop through fields in model
        for field in model.__fields__.values():
            # Add Field
            self._add_field(field)

    def _add_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # Get Field Type and Possible Origin
        field_type = field.outer_type_
        field_origin = typing_inspect.get_origin(field_type)

        # Switch on Field Type
        if field_type is bool:
            # Add Boolean Field
            self._add_boolean_field(field)

        elif field_origin in (collections.deque, frozenset, list, set, tuple):
            # Add Container Field
            self._add_container_field(field)

        elif field_origin is Literal:
            # Add Literal Field
            self._add_literal_field(field)

        elif isinstance(field_type, type) and issubclass(field_type, enum.Enum):
            # Add Enum Field
            self._add_enum_field(field)

        else:
            # Add Other Standard Field
            self._add_standard_field(field)

    def _add_boolean_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds boolean pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # Booleans are always treated as optional flags
        self._optional_group.add_argument(
            _argument_name(field.name),
            action=argparse.BooleanOptionalAction,
            default=bool(field.default),
            help=field.field_info.description,
            dest=field.name,
            required=False,
        )

    def _add_container_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds container pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # Deque, FrozenSet, List, Set Tuple
        if field.required:
            # Required
            self._required_group.add_argument(
                _argument_name(field.name),
                action=argparse._AppendAction,  # pylint: disable=protected-access
                help=field.field_info.description,
                dest=field.name,
                required=True,
            )

        else:
            # Optional
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._AppendAction,  # pylint: disable=protected-access
                default=field.default,
                help=field.field_info.description,
                dest=field.name,
                required=False,
            )

    def _add_literal_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds literal pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # Get choices from literal
        choices = typing_inspect.get_args(field.outer_type_)

        # Literals are treated as constant flags, or choices
        if len(choices) == 1:
            # Optional Flag
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreConstAction,  # pylint: disable=protected-access
                const=choices[0],
                default=field.default,
                help=field.field_info.description,
                dest=field.name,
                required=False,
            )

        elif field.required:
            # Required
            self._required_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                type=type(choices[0]),
                choices=choices,
                help=field.field_info.description,
                dest=field.name,
                required=True,
            )

        else:
            # Optional
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                type=type(choices[0]),
                choices=choices,
                default=field.default,
                help=f"{field.field_info.description} (default: {field.default})",
                dest=field.name,
                required=False,
            )

    def _add_enum_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds enum pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # Enums are treated as choices
        if field.required:
            # Required
            self._required_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                type=lambda arg: _enum_name_to_member(arg, field.outer_type_),
                choices=field.outer_type_,
                help=field.field_info.description,
                dest=field.name,
                required=True,
            )

        else:
            # Optional
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                type=lambda arg: _enum_name_to_member(arg, field.outer_type_),
                choices=field.outer_type_,
                default=field.default,
                help=f"{field.field_info.description} (default: {field.default})",
                dest=field.name,
                required=False,
            )

    def _add_standard_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds standard pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # All other types are treated in a standard way
        if field.required:
            # Required
            self._required_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                help=field.field_info.description,
                dest=field.name,
                required=True,
            )

        else:
            # Optional
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                default=field.default,
                help=f"{field.field_info.description} (default: {field.default})",
                dest=field.name,
                required=False,
            )


def _enum_name_to_member(name: str, enum_type: type[EnumT]) -> EnumT:
    """Converts enum member name to actual enum member.

    Args:
        name (str): Name of enum member.
        enum_type (type[EnumT]): Enum type.

    Returns:
        EnumT: Member from specified enum.

    Raises:
        ValueError: Raised if enum member does not exist.
    """
    try:
        return enum_type[name]
    except KeyError as exc:
        raise ValueError from exc


def _argument_name(name: str) -> str:
    """Standardises argument name.

    Args:
        name (str): Name of the argument.

    Returns:
        str: Standardised name of the argument.
    """
    # Add '--', replace '_' with '-'
    return f"--{name.replace('_', '-')}"
