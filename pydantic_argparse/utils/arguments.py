"""Arguments Utility Functions for Declarative Typed Argument Parsing.

The `arguments` module contains various utility functions, including:

* `name`: Formats argument names.
* `description`: Formats argument descriptions.

The functionality outlined above is so common throughout the typed argument
parsing process that the functions have been refactored out into this module as
utility functions.
"""


# Typing
from typing import Any, Optional, TypeVar


# Constants
# Arbitrary `MISSING` object is required for functions where `None` is a valid
# and possible argument to specify.
MISSING = TypeVar("MISSING")


def name(name: str) -> str:
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
    # Prepend '--', replace '_' with '-'
    return f"--{name.replace('_', '-')}"


def description(
    description: Optional[str],
    default: Optional[Any] = MISSING,
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
