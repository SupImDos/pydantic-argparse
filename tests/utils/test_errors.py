"""Tests the `errors` Module.

This module provides full unit test coverage for the `errors` module, testing
all branches of all functions.
"""


# Standard
import textwrap

# Third-Party
import pydantic
import pytest

# Local
from pydantic_argparse import utils
from tests import conftest as conf

# Typing
from typing import Sequence, Tuple, Union


# Shortcuts
# We define an error definition as a tuple with an Exception and Location
ErrorDefinition = Tuple[Exception, Union[str, Tuple[str, ...]]]


@pytest.mark.parametrize(
    (
        "errors",
        "expected",
    ),
    [
        (
            [
                (pydantic.errors.MissingError(), "argument"),
            ],
            """
            1 validation error for TestModel
            argument
              field required (type=value_error.missing)
            """,
        ),
        (
            [
                (pydantic.errors.IPv4AddressError(), ("p", "x")),
                (pydantic.errors.IntegerError(),     ("q", "y")),
                (pydantic.errors.UUIDError(),        ("r", "z")),
            ],
            """
            3 validation errors for TestModel
            p -> x
              value is not a valid IPv4 address (type=value_error.ipv4address)
            q -> y
              value is not a valid integer (type=type_error.integer)
            r -> z
              value is not a valid uuid (type=type_error.uuid)
            """,
        ),
    ],
)
def test_error_format(
    errors: Sequence[ErrorDefinition],
    expected: str,
) -> None:
    """Tests `utils.errors.format` Function.

    Args:
        errors (Sequence[ErrorDefinition]): Errors to test.
        expected (str): Expected result of the test.
    """
    # Construct Validation Error
    error = pydantic.ValidationError(
        errors=[pydantic.error_wrappers.ErrorWrapper(exc, loc) for (exc, loc) in errors],
        model=conf.TestModel,
    )

    # Format Error
    result = utils.errors.format(error)

    # Assert
    assert result == textwrap.dedent(expected).strip()
