"""Declarative and Typed Argument Parser.

The `parser` module contains the `ArgumentParser` class, which provides a
declarative method of defining command-line interfaces.

The procedure to declaratively define a typed command-line interface is:

1. Define `pydantic` arguments model
2. Create typed `ArgumentParser`
3. Parse typed arguments

The resultant arguments object returned is an instance of the defined
`pydantic` model. This means that the arguments object and its attributes will
be compatible with an IDE, linter or type checker.
"""


# Standard
import argparse
import sys

# Third-Party
import pydantic

# Local
from pydantic_argparse import parsers
from pydantic_argparse import utils
from . import actions

# Typing
from typing import Any, Generic, NoReturn, Optional, TypeVar  # pylint: disable=wrong-import-order


# Constants
PydanticModelT = TypeVar("PydanticModelT", bound=pydantic.BaseModel)


class ArgumentParser(argparse.ArgumentParser, Generic[PydanticModelT]):
    """Declarative and Typed Argument Parser.

    The `ArgumentParser` declaratively generates a command-line interface using
    the `pydantic` model specified upon instantiation.

    The `ArgumentParser` provides the following `argparse` functionality:

    * Required Arguments
    * Optional Arguments
    * Subcommands

    All arguments are *named*, and positional arguments are not supported.

    The `ArgumentParser` provides the method `parse_typed_args()` to parse
    command line arguments and return an instance of its bound `pydantic`
    model, populated with the parsed and validated user supplied command-line
    arguments.
    """

    # Argument Group Names
    COMMANDS = "commands"
    REQUIRED = "required arguments"
    OPTIONAL = "optional arguments"
    HELP = "help"

    # Keyword Arguments
    KWARG_REQUIRED = "required"

    # Exit Codes
    EXIT_ERROR = 2

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
        """Instantiates the Typed Argument Parser with its `pydantic` model.

        Args:
            model (type[PydanticModelT]): Pydantic argument model class.
            prog (Optional[str]): Program name for CLI.
            description (Optional[str]): Program description for CLI.
            version (Optional[str]): Program version string for CLI.
            epilog (Optional[str]): Optional text following help message.
            add_help (bool): Whether to add a `-h`/`--help` flag.
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

        # Set Model
        self.model = model

        # Set Add Help and Exit on Error Flag
        self.add_help = add_help
        self.exit_on_error = exit_on_error

        # Set Version and Model
        self.version = version
        self.model = model

        # Add Arguments Groups
        self._subcommands: Optional[argparse._SubParsersAction] = None
        self._required_group = self.add_argument_group(ArgumentParser.REQUIRED)
        self._optional_group = self.add_argument_group(ArgumentParser.OPTIONAL)
        self._help_group = self.add_argument_group(ArgumentParser.HELP)

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

        If `args` are not supplied by the user, then they are automatically
        retrieved from the `sys.argv` command-line arguments.

        Args:
            args (Optional[list[str]]): Optional list of arguments to parse.

        Returns:
            PydanticModelT: Populated instance of typed arguments model.

        Raises:
            argparse.ArgumentError: Raised upon error, if not exiting on error.
            SystemExit: Raised upon error, if exiting on error.
        """
        # Call Super Class Method
        namespace = self.parse_args(args)

        # Convert Namespace to Dictionary
        arguments = utils.namespace_to_dict(namespace)

        # Handle Possible Validation Errors
        try:
            # Convert Namespace to Pydantic Model
            model = self.model.parse_obj(arguments)

        except pydantic.ValidationError as exc:
            # Catch exception, and use the ArgumentParser.error() method
            # to report it to the user
            self.error(str(exc))

        # Return
        return model

    def add_argument(
        self,
        *args: Any,
        **kwargs: Any,
        ) -> argparse.Action:
        """Adds an argument to the ArgumentParser.

        Args:
            *args (Any): Positional args to be passed to super class method.
            **kwargs (Any): Keyword args to be passed to super class method.

        Returns:
            argparse.Action: Action generated by the argument.
        """
        # Check whether required or optional
        if kwargs.get(ArgumentParser.KWARG_REQUIRED):
            # Required
            group = self._required_group

        else:
            # Optional
            group = self._optional_group

        # Return Action
        return group.add_argument(*args, **kwargs)

    def error(self, message: str) -> NoReturn:
        """Prints a usage message to `stderr` and exits if required.

        Args:
            message (str): Message to print to the user.

        Raises:
            argparse.ArgumentError: Raised if not exiting on error.
            SystemExit: Raised if exiting on error.
        """
        # Print usage message
        self.print_usage(sys.stderr)

        # Check whether parser should exit
        if self.exit_on_error:
            self.exit(ArgumentParser.EXIT_ERROR, f"{self.prog}: error: {message}\n")

        # Raise Error
        raise argparse.ArgumentError(None, f"{self.prog}: error: {message}")

    def _commands(self) -> argparse._SubParsersAction:
        """Creates and Retrieves Subcommands Action for the ArgumentParser.

        Returns:
            argparse._SubParsersAction: SubParsersAction for the subcommands.
        """
        # Check for Existing Sub-Commands Group
        if not self._subcommands:
            # Add Sub-Commands Group
            self._subcommands = self.add_subparsers(
                title=ArgumentParser.COMMANDS,
                action=actions.SubParsersAction,
                required=True,
            )

            # Shuffle Group to the Top for Help Message
            self._action_groups.insert(0, self._action_groups.pop())

        # Return
        return self._subcommands

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
            field (pydantic.fields.ModelField): Field to be added to parser.
        """
        # Switch on Field Type
        if parsers.command.should_parse(field):
            # Add Command
            parsers.command.parse_field(self._commands(), field)

        elif parsers.boolean.should_parse(field):
            # Add Boolean Field
            parsers.boolean.parse_field(self, field)

        elif parsers.container.should_parse(field):
            # Add Container Field
            parsers.container.parse_field(self, field)

        elif parsers.mapping.should_parse(field):
            # Add Mapping Field
            parsers.mapping.parse_field(self, field)

        elif parsers.literal.should_parse(field):
            # Add Literal Field
            parsers.literal.parse_field(self, field)

        elif parsers.enum.should_parse(field):
            # Add Enum Field
            parsers.enum.parse_field(self, field)

        else:
            # Add Standard Field
            parsers.standard.parse_field(self, field)
