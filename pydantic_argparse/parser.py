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
import ast
from collections import deque
import enum
import functools
import sys

# Third-Party
import pydantic
import typing_inspect

# Typing
from typing import Any, Callable, Generic, Literal, NoReturn, Optional, TypeVar  # pylint: disable=wrong-import-order


# Constants
PydanticModelT = TypeVar("PydanticModelT", bound=pydantic.BaseModel)
EnumT = TypeVar("EnumT", bound=enum.Enum)
AnyT = TypeVar("AnyT")
Missing = object()


class ArgumentParser(argparse.ArgumentParser, Generic[PydanticModelT]):
    """Custom Typed Argument Parser."""
    def __init__(
        self,
        model: type[PydanticModelT],
        prog: Optional[str]=None,
        description: Optional[str]=None,
        version: Optional[str]=None,
        epilog: Optional[str]=None,
        add_help: bool=True,
        exit_on_error: bool=True,
        ) -> None:
        """Custom Typed Argument Parser.

        Args:
            model (type[PydanticModelT]): Pydantic argument model class.
            prog (Optional[str]): Program name for CLI.
            description (Optional[str]): Program description for CLI.
            version (Optional[str]): Program version string for CLI.
            epilog (Optional[str]): Optional text following help message.
            add_help (bool): Whether to add a -h/--help flag.
            exit_on_error (bool): Whether to exit on error.
        """
        # Initialise Super Class
        super().__init__(
            prog=prog,
            description=description,
            epilog=epilog,
            exit_on_error=exit_on_error,
            add_help=False,  # Always disable the automatic help flag.
        )

        # Set Add Help and Exit on Error Flag
        self.add_help = add_help
        self.exit_on_error = exit_on_error

        # Set Version and Model
        self.version = version
        self.model = model

        # Add Arguments Groups
        self._required_group = self.add_argument_group("required arguments")
        self._optional_group = self.add_argument_group("optional arguments")
        self._help_group = self.add_argument_group("help")

        # Add Help and Version Flags
        if self.add_help:
            self._add_help_flag()
        if self.version:
            self._add_version_flag()

        # Add Arguments from Model
        self._add_model(model)

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
            self.error(str(exc))

        # Return
        return model

    def error(self, message: str) -> NoReturn:
        """Prints a usage message to stderr and exits.

        Args:
            message (str): Message to print to the user.

        Raises:
            argparse.ArgumentError: Raised if not exiting on error.
        """
        # Print usage message
        self.print_usage(sys.stderr)

        # Check whether parser should exit
        if self.exit_on_error:
            self.exit(2, f"{self.prog}: error: {message}\n")

        # Raise Error
        raise argparse.ArgumentError(None, f"{self.prog}: error: {message}")

    def _add_help_flag(self) -> None:
        """Adds help flag to argparser."""
        # Add help flag
        self._help_group.add_argument(
            "-h",
            "--help",
            action=argparse._HelpAction,  # pylint: disable=protected-access
            help="show this help message and exit",
        )

    def _add_version_flag(self) -> None:
        """Adds version flag to argparser."""
        # Add version flag
        self._help_group.add_argument(
            "-v",
            "--version",
            action=argparse._VersionAction,  # pylint: disable=protected-access
            help="show program's version number and exit",
        )

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

        elif field_origin in (list, tuple, set, frozenset, deque):
            # Add Container Field
            self._add_container_field(field)

        elif field_origin is dict:
            # Add Dictionary (JSON) Field
            self._add_json_field(field)

        elif field_origin is Literal:
            # Add Literal Field
            self._add_literal_field(field)

        elif isinstance(field_type, enum.EnumMeta):
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
        # Booleans can be treated as required or optional flags
        if field.required:
            # Required
            self._add_boolean_field_required(field)

        else:
            # Optional
            self._add_boolean_field_optional(field)

    def _add_boolean_field_required(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds required boolean pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Add Required Boolean Field
        self._required_group.add_argument(
            _argument_name(field.name),
            action=argparse.BooleanOptionalAction,
            help=_argument_description(field.field_info.description),
            dest=field.name,
            required=True,
        )

    def _add_boolean_field_optional(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds optional boolean pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Get Default
        default = field.get_default()

        # Add Optional Boolean Field
        if default:
            # Optional (Default True)
            self._optional_group.add_argument(
                _argument_name("no-" + field.name),
                action=argparse._StoreFalseAction,  # pylint: disable=protected-access
                default=default,
                help=_argument_description(field.field_info.description, default),
                dest=field.name,
                required=False,
            )

        else:
            # Optional (Default False)
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreTrueAction,  # pylint: disable=protected-access
                default=default,
                help=_argument_description(field.field_info.description, default),
                dest=field.name,
                required=False,
            )

    def _add_container_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds container pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # List, Tuple, Set, FrozenSet, Deque
        if field.required:
            # Required
            self._add_container_field_required(field)

        else:
            # Optional
            self._add_container_field_optional(field)

    def _add_container_field_required(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds required container pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Add Required Container Field
        self._required_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            nargs="+",
            help=_argument_description(field.field_info.description),
            dest=field.name,
            required=True,
        )

    def _add_container_field_optional(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds optional container pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Get Default
        default = field.get_default()

        # Add Optional Container Field
        self._optional_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            nargs="+",
            default=default,
            help=_argument_description(field.field_info.description, default),
            dest=field.name,
            required=False,
        )

    def _add_json_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds json pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # JSON (Dictionary)
        if field.required:
            # Required
            self._add_json_field_required(field)

        else:
            # Optional
            self._add_json_field_optional(field)

    def _add_json_field_required(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds required json pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Define Custom Type Caster
        type_caster = _type_caster(field.name, ast.literal_eval)

        # Add Required JSON Field
        self._required_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=type_caster,
            help=_argument_description(field.field_info.description),
            dest=field.name,
            required=True,
        )

    def _add_json_field_optional(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds optional json pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Define Custom Type Caster
        type_caster = _type_caster(field.name, ast.literal_eval)

        # Get Default
        default = field.get_default()

        # Add Optional JSON Field
        self._optional_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=type_caster,
            default=default,
            help=_argument_description(field.field_info.description, default),
            dest=field.name,
            required=False,
        )

    def _add_literal_field(self, field: pydantic.fields.ModelField) -> None:
        """Adds literal pydantic field to argument parser.

        Args:
            field (pydanic.fields.ModelField): Field to be added to parser.
        """
        # Literals are treated as constant flags, or choices
        if field.required:
            # Required
            self._add_literal_field_required(field)

        else:
            # Optional
            self._add_literal_field_optional(field)

    def _add_literal_field_required(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds required literal pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Get choices from literal
        choices = list(typing_inspect.get_args(field.outer_type_))

        # Define Custom Type Caster
        type_caster = _type_caster(field.name, _arg_to_choice, choices=choices)

        # Add Required Literal Field
        self._required_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=type_caster,
            choices=choices,
            help=_argument_description(field.field_info.description),
            dest=field.name,
            required=True,
        )

    def _add_literal_field_optional(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds optional literal pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Get choices from literal
        choices = list(typing_inspect.get_args(field.outer_type_))

        # Define Custom Type Caster
        type_caster = _type_caster(field.name, _arg_to_choice, choices=choices)

        # Get Default
        default = field.get_default()

        # Add Optional Literal Field
        if len(choices) == 1:
            # Optional Flag
            if default is not None and field.allow_none:
                # Optional Flag (Default Not None)
                self._optional_group.add_argument(
                    _argument_name("no-" + field.name),
                    action=argparse._StoreConstAction,  # pylint: disable=protected-access
                    const=None,
                    default=default,
                    help=_argument_description(field.field_info.description, default),
                    dest=field.name,
                    required=False,
                )

            else:
                # Optional Flag (Default None)
                self._optional_group.add_argument(
                    _argument_name(field.name),
                    action=argparse._StoreConstAction,  # pylint: disable=protected-access
                    const=choices[0],
                    default=default,
                    help=_argument_description(field.field_info.description, default),
                    dest=field.name,
                    required=False,
                )

        else:
            # Optional Choice
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                type=type_caster,
                choices=choices,
                default=default,
                help=_argument_description(field.field_info.description, default),
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
            self._add_enum_field_required(field)

        else:
            # Optional
            self._add_enum_field_optional(field)

    def _add_enum_field_required(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds required enum pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Get Enum Type
        enum_type: type[enum.Enum] = field.outer_type_

        # Define Custom Type Caster
        type_caster = _type_caster(field.name, _arg_to_enum_member, enum_type=enum_type)

        # Add Required Enum Field
        self._required_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            type=type_caster,
            choices=enum_type,
            help=_argument_description(field.field_info.description),
            dest=field.name,
            required=True,
        )

    def _add_enum_field_optional(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds optional enum pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Get Enum Type
        enum_type: type[enum.Enum] = field.outer_type_

        # Define Custom Type Caster
        type_caster = _type_caster(field.name, _arg_to_enum_member, enum_type=enum_type)

        # Get Default
        default = field.get_default()

        # Add Optional Enum Field
        if len(enum_type) == 1:
            # Optional Flag
            if default is not None and field.allow_none:
                # Optional Flag (Default Not None)
                self._optional_group.add_argument(
                    _argument_name("no-" + field.name),
                    action=argparse._StoreConstAction,  # pylint: disable=protected-access
                    const=None,
                    default=default,
                    help=_argument_description(field.field_info.description, default),
                    dest=field.name,
                    required=False,
                )

            else:
                # Optional Flag (Default None)
                self._optional_group.add_argument(
                    _argument_name(field.name),
                    action=argparse._StoreConstAction,  # pylint: disable=protected-access
                    const=list(enum_type)[0],
                    default=default,
                    help=_argument_description(field.field_info.description, default),
                    dest=field.name,
                    required=False,
                )

        else:
            # Optional Choice
            self._optional_group.add_argument(
                _argument_name(field.name),
                action=argparse._StoreAction,  # pylint: disable=protected-access
                type=type_caster,
                choices=enum_type,
                default=default,
                help=_argument_description(field.field_info.description, default),
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
            self._add_standard_field_required(field)

        else:
            # Optional
            self._add_standard_field_optional(field)

    def _add_standard_field_required(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds required standard pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Add Required Standard Field
        self._required_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            help=_argument_description(field.field_info.description),
            dest=field.name,
            required=True,
        )

    def _add_standard_field_optional(
        self,
        field: pydantic.fields.ModelField,
        ) -> None:
        """Adds optional standard pydantic field to argument parser.

        Args:
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Get Default
        default = field.get_default()

        # Add Optional Standard Field
        self._optional_group.add_argument(
            _argument_name(field.name),
            action=argparse._StoreAction,  # pylint: disable=protected-access
            default=default,
            help=_argument_description(field.field_info.description, default),
            dest=field.name,
            required=False,
        )


def _arg_to_enum_member(
    argument: str,
    enum_type: type[EnumT],
    ) -> EnumT:
    """Attempts to convert string argument to a supplied enum member.

    Args:
        argument (str): Possible name of enum member.
        enum_type (type[EnumT]): Enum type.

    Returns:
        EnumT: Member from specified enum.

    Raises:
        ValueError: Raised if enum member does not exist.
    """
    # Attempt to convert string argument to enum member
    try:
        return enum_type[argument]
    except KeyError as exc:
        raise ValueError from exc


def _arg_to_choice(
    argument: str,
    choices: list[AnyT],
    ) -> AnyT:
    """Attempts to convert string argument to a supplied choice.

    Args:
        argument (str): Possible choice.
        choices (list[AnyT]): List of choices.

    Returns:
        AnyT: Selected choice.

    Raises:
        ValueError: Raised if argument is not one of the choices.
    """
    # Attempt to convert string argument to one of choices
    for choice in choices:
        if str(choice) == argument:
            return choice

    # Raise Error
    raise ValueError


def _type_caster(
    name: str,
    function: Callable[..., AnyT],
    **kwargs: Any,
    ) -> Callable[[str], AnyT]:
    """Wraps a function to provide a type caster.

    Args:
        name (str): Name of the type caster (for nicer error messages)
        function (Callable[..., AnyT]): Callable function for type caster.
        **kwargs (Any): Keyword arguments to pass to function.

    Returns:
        Callable[[str], AnyT]: Type caster named partial function.
    """
    # Create Partial Function and Set Name
    function = functools.partial(function, **kwargs)
    setattr(function, "__name__", name)

    # Return
    return function


def _argument_name(name: str) -> str:
    """Standardises argument name.

    Args:
        name (str): Name of the argument.

    Returns:
        str: Standardised name of the argument.
    """
    # Add '--', replace '_' with '-'
    return f"--{name.replace('_', '-')}"


def _argument_description(
    description: Optional[str],
    default: Optional[Any]=Missing,
    ) -> str:
    """Standardises argument description.

    Args:
        description (Optional[str]): Optional description for argument.
        default (Optional[Any]): Default value for argument if applicable.

    Returns:
        str: Standardised description of the argument.
    """
    # Construct Default String
    default = f"(default: {default})" if default is not Missing else None

    # Return Standardised Description String
    return " ".join(filter(None, [description, default]))
