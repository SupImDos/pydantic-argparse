"""Namespaces Utility Functions for Declarative Typed Argument Parsing.

The `namespaces` module contains various utility functions, including:

* `to_dict`: Recursively parses `argparse.Namespace`s to `dict`s.

The functionality outlined above is so common throughout the typed argument
parsing process that the functions have been refactored out into this module as
utility functions.
"""


# Standard
import argparse

# Typing
from typing import Any, Dict


def to_dict(namespace: argparse.Namespace) -> Dict[str, Any]:
    """Converts a nested namespace to a dictionary recursively.

    Args:
        namespace (argparse.Namespace): Namespace object to convert.

    Returns:
        dict[str, Any]: Nested dictionary generated from namespace.
    """
    # Get Dictionary from Namespace Vars
    dictionary = vars(namespace)

    # Loop Through Dictionary
    for (key, value) in dictionary.items():
        # Check for Namespace Objects
        if isinstance(value, argparse.Namespace):
            # Recurse
            dictionary[key] = to_dict(value)

    # Return
    return dictionary
