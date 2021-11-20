"""actions.py

Provides custom Actions classes.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import annotations


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
        """Parses arguments with the subparser, then embeds the resultant
        sub-namespace into the parent namespace.

        This subclass differs in functionality to the existing inbuilt argparse
        SubParsersAction because it nests the resultant sub-namespace into the
        parent namespace, rather than iterating through the parsed arguments to
        update the parent namespace object.

        Example:
            # Create Argument Parser
            parser = argparse.ArgumentParser()

            # Add Example '--global' Argument
            parser.add_argument("--global")

            # Add SubParsersAction
            subparsers = parser.add_subparsers()

            # Add Example 'apple' Command with '--cat' Argument
            apple = subparsers.add_parser("apple")
            apple.add_argument("--cat")

            # Add Example 'banana' Command with '--dog' Argument
            banana = subparsers.add_parser("banana")
            banana.add_argument("--dog")

        Parsing the arguments:
            * --global 1 apple --cat 2

        Resultant namespaces:
            * Original: Namespace(global=1, cat=2)
            * Custom:   Namespace(global=1, apple=Namespace(cat=2))

        This behaviour results in a final namespace structure which is much
        easier to parser, where subcommands are easily identified and nested
        into their own namespace recursively.

        Args:
            parser (argparse.ArgumentParser): Parent argument parser object.
            namespace (argparse.Namespace): Parent namespace being parsed to.
            values (Union[str, Sequence[Any], None]): Arguments to parse.
            option_string (Optional[str]): Optional option string.

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
        subnamespace, arg_strings = parser.parse_known_args(arg_strings, None)
        setattr(namespace, parser_name, subnamespace)

        # TODO (HaydenR): Move unrecognized args on the subnamespace to the top
        #                 level namespace?

        # Store any unrecognized options on the parent namespace, so that the
        # top level parser can decide what to do with them
        if arg_strings:
            vars(namespace).setdefault(argparse._UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, argparse._UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)
