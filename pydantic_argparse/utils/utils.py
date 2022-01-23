"""utils.py

Provides utility functions for other modules.

@author Hayden Richards <SupImDos@gmail.com>
"""


# Standard
import argparse
import functools

# Typing
from typing import Any, Callable, Optional, TypeVar  # pylint: disable=wrong-import-order


# Constants
# Arbitrary 'MISSING' object is required for functions where 'None' is a valid
# and possible argument to specify.
T = TypeVar("T")
MISSING = object()


def argument_description(
    description: Optional[str],
    default: Optional[Any]=MISSING,
    ) -> str:
    """Standardises argument description.

    Args:
        description (Optional[str]): Optional description for argument.
        default (Optional[Any]): Default value for argument if applicable.

    Returns:
        str: Standardised description of the argument.
    """
    # Construct Default String
    default = f"(default: {default})" if default is not MISSING else None

    # Return Standardised Description String
    return " ".join(filter(None, [description, default]))


def argument_name(name: str) -> str:
    """Standardises argument name.

    Args:
        name (str): Name of the argument.

    Returns:
        str: Standardised name of the argument.
    """
    # Add '--', replace '_' with '-'
    return f"--{name.replace('_', '-')}"


def namespace_to_dict(namespace: argparse.Namespace) -> dict[str, Any]:
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
            dictionary[key] = namespace_to_dict(value)

    # Return
    return dictionary


def type_caster(
    name: str,
    function: Callable[..., T],
    **kwargs: Any,
    ) -> Callable[[str], T]:
    """Wraps a function to provide a type caster.

    Args:
        name (str): Name of the type caster (for nicer error messages)
        function (Callable[..., T]): Callable function for type caster.
        **kwargs (Any): Keyword arguments to pass to function.

    Returns:
        Callable[[str], T]: Type caster named partial function.
    """
    # Create Partial Function and Set Name
    function = functools.partial(function, **kwargs)
    setattr(function, "__name__", name)

    # Return
    return function
