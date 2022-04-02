"""Utility Functions for Declarative Typed Argument Parsing.

The `utils` module contains various utility functions, including:

* `argument_name`: Formats argument names.
* `argument_description`: Formats argument descriptions.
* `namespace_to_dict`: Recursively parses `argparse.Namespace`s to `dict`s.
* `type_caster`: Constructs named `functools.partial` type casting functions.
* `is_field_a`: Checks and compares the types of `pydantic` fields.

The functionality outlined above is so common throughout the typed argument
parsing process that the functions have been refactored out into this module as
utility functions.
"""


# Standard
import argparse
import functools
import typing

# Third-Party
import pydantic

# Typing
from typing import Any, Callable, Optional, TypeVar, Union  # pylint: disable=wrong-import-order


# Constants
# Arbitrary `MISSING` object is required for functions where `None` is a valid
# and possible argument to specify.
T = TypeVar("T")
MISSING = TypeVar("MISSING")


def argument_name(name: str) -> str:
    """Standardises argument name.

    Examples:
        ```python
        argument_name("hello") == "--hello"
        argument_name("hello_world") == "--hello-world"
        ```

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

    Examples:
        ```python
        argument_description("hello") == "hello"
        argument_description("hello", None) == "hello (default: None)"
        argument_description("hello", 42) == "hello (default: 42)"
        ```

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


def is_field_a(
    field: pydantic.fields.ModelField,
    types: Union[Any, tuple[Any, ...]],
    ) -> bool:
    """Checks whether the subject *is* any of the supplied types.

    The checks are performed as follows:

    1. `field` *is* one of the `types`
    2. `field` *is an instance* of one of the `types`
    3. `field` *is a subclass* of one of the `types`

    If any of these conditions are `True`, then the function returns `True`,
    else `False`.

    Args:
        field (pydantic.fields.ModelField): Subject field to check type of.
        types (Union[Any, tuple[Any, ...]]): Type(s) to compare field against.

    Returns:
        bool: Whether the field *is* considered one of the types.
    """
    # Create tuple if only one type was provided
    if not isinstance(types, tuple):
        types = (types, )

    # Get field type, or origin if applicable
    field_type = typing.get_origin(field.outer_type_) or field.outer_type_

    # Check `isinstance` and `issubclass` validity
    # In order for `isinstance` and `issubclass` to be valid, all arguments
    # should be instances of `type`, otherwise `TypeError` *may* be raised.
    is_valid = all(isinstance(t, type) for t in (*types, field_type))

    # Perform checks and return
    return (
        field_type in types
        or (is_valid and isinstance(field_type, types))
        or (is_valid and issubclass(field_type, types))
    )
