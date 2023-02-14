"""Errors Utility Functions for Declarative Typed Argument Parsing.

The `errors` module contains a utility function used for formatting `pydantic`
Validation Errors to human readable messages.
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
