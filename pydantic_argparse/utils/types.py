"""Types Utility Functions for Declarative Typed Argument Parsing.

The `types` module contains various utility functions, including:

* `caster`: Constructs named `functools.partial` type casting functions.
* `is_field_a`: Checks and compares the types of `pydantic` fields.

The functionality outlined above is so common throughout the typed argument
parsing process that the functions have been refactored out into this module as
utility functions.
"""


# Standard
import functools
import sys

# Third-Party
import pydantic

# Typing
from typing import Any, Callable, Tuple, TypeVar, Union

# Version-Guarded
if sys.version_info < (3, 8):  # pragma: <3.8 cover
    from typing_extensions import get_origin
else:  # pragma: >=3.8 cover
    from typing import get_origin


# Constants
T = TypeVar("T")


def caster(
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
    # Set Name, Create Partial Function and Update Wrapper
    function.__name__ = name
    partial = functools.partial(function, **kwargs)
    functools.update_wrapper(partial, function)

    # Return
    return partial


def is_field_a(
    field: pydantic.fields.ModelField,
    types: Union[Any, Tuple[Any, ...]],
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
    field_type = get_origin(field.outer_type_) or field.outer_type_

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
