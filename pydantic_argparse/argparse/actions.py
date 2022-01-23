"""actions.py

Provides custom Actions classes.

@author Hayden Richards <SupImDos@gmail.com>
"""


# Standard
import argparse

# Typing
from typing import Any, Optional, Sequence, Union, cast


class SubParsersAction(argparse._SubParsersAction):  # pylint: disable=protected-access
    """Custom SubParsersAction."""
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str]=None,
        ) -> None:
        """Parses arguments with the specified subparser, then embeds the
        resultant sub-namespace into the supplied parent namespace.

        This subclass differs in functionality from the existing standard
        argparse SubParsersAction because it nests the resultant sub-namespace
        directly into the parent namespace, rather than iterating through and
        updating the parent namespace object with each argument individually.

        Example:
            # Create Argument Parser
            parser = argparse.ArgumentParser()

            # Add Example Global Argument
            parser.add_argument("--time")

            # Add SubParsersAction
            subparsers = parser.add_subparsers()

            # Add Example 'walk' Command with Arguments
            walk = subparsers.add_parser("walk")
            walk.add_argument("--speed")
            walk.add_argument("--distance")

            # Add Example 'talk' Command with Arguments
            talk = subparsers.add_parser("talk")
            talk.add_argument("--volume")
            talk.add_argument("--topic")

        Parsing the arguments:
            * --time 3 walk --speed 7 --distance 42

        Resultant namespaces:
            * Original: Namespace(time=3, speed=7, distance=42)
            * Custom:   Namespace(time=3, walk=Namespace(speed=7, distance=42))

        This behaviour results in a final namespace structure which is much
        easier to parse, where subcommands are easily identified and nested
        into their own namespace recursively.

        Args:
            parser (argparse.ArgumentParser): Parent argument parser object.
            namespace (argparse.Namespace): Parent namespace being parsed to.
            values (Union[str, Sequence[Any], None]): Arguments to parse.
            option_string (Optional[str]): Optional option string (not used).

        Raises:
            argparse.ArgumentError: Raised if subparser name does not exist.
        """
        # Check values object is a sequence
        # In order to not violate the Liskov Substitution Principle (LSP), the
        # function signature for __call__ must match the base Action class. As
        # such, this function signature also accepts 'str' and 'None' types for
        # the values argument. However, in reality, this should only ever be a
        # list of strings here, so we just do a type cast.
        values = cast(list[str], values)

        # Get Parser Name and Remaining Argument Strings
        parser_name, *arg_strings = values

        # Try select the parser
        try:
            # Select the parser
            parser = self._name_parser_map[parser_name]

        except KeyError as exc:
            # Parser doesn't exist, raise an exception
            raise argparse.ArgumentError(
                self,
                f"unknown parser {parser_name} (choices: {', '.join(self._name_parser_map)})"
            ) from exc

        # Parse all the remaining options into a sub-namespace, then embed this
        # sub-namespace into the parent namespace
        subnamespace, arg_strings = parser.parse_known_args(arg_strings)
        setattr(namespace, parser_name, subnamespace)

        # Store any unrecognized options on the parent namespace, so that the
        # top level parser can decide what to do with them
        if arg_strings:
            vars(namespace).setdefault(argparse._UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, argparse._UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)
