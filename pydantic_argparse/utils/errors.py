"""Errors Utility Functions for Declarative Typed Argument Parsing.

The `errors` module contains various utility functions, including:

* `format`: Formats error messages.

The functionality outlined above is so common throughout the typed argument
parsing process that the functions have been refactored out into this module as
utility functions.
"""


# Third-Party
import pydantic


def format(error: pydantic.ValidationError) -> str:  # noqa: A001
    """Formats a `pydantic` Validation Error into a human readable format.

    Args:
        error (pydantic.ValidationError): Validation Error to be formatted.

    Returns:
        str: `pydantic` Validation error in a human readable format.
    """
    # Format and Return
    return str(error)
