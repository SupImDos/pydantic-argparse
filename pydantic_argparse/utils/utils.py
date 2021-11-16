"""utils.py

Provides utility functions for other modules.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import annotations


# Standard
import functools

# Typing
from typing import Any, Callable, Optional, TypeVar  # pylint: disable=wrong-import-order


# Constants
# Arbitrary 'MISSING' object is required for functions where 'None' is a valid
# and possible argument to specify.
MISSING = object()
T = TypeVar("T")


def argument_name(name: str) -> str:
    """Standardises argument name.

    Args:
        name (str): Name of the argument.

    Returns:
        str: Standardised name of the argument.
    """
    # Add '--', replace '_' with '-'
    return f"--{name.replace('_', '-')}"


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
