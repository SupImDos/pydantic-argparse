"""Tests the `arguments` Module.

This module provides full unit test coverage for the `arguments` module,
testing all branches of all functions.
"""


# Third-Party
import pytest

# Local
from pydantic_argparse import utils

# Typing
from typing import Any, Optional


@pytest.mark.parametrize(
    (
        "name",
        "expected",
    ),
    [
        ("test", "--test"),
        ("test_two", "--test-two"),
    ],
)
def test_argument_name(
    name: str,
    expected: str,
) -> None:
    """Tests `utils.arguments.name` Function.

    Args:
        name (str): Argument name to test.
        expected (str): Expected result of the test.
    """
    # Generate Argument Name
    result = utils.arguments.name(name)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    (
        "description",
        "default",
        "expected",
    ),
    [
        ("A",  "A",                     "A (default: A)"),
        ("A",  5,                       "A (default: 5)"),
        ("A",  None,                    "A (default: None)"),
        ("A",  utils.arguments.MISSING, "A"),
        (None, "A",                     "(default: A)"),
        (None, 5,                       "(default: 5)"),
        (None, None,                    "(default: None)"),
        (None, utils.arguments.MISSING, ""),
    ],
)
def test_argument_description(
    description: Optional[str],
    default: Optional[Any],
    expected: str,
) -> None:
    """Tests `utils.arguments.description` Function.

    Args:
        description (Optional[str]): Optional argument description to test.
        default (Optional[Any]): Optional argument default to test.
        expected (str): Expected result of the test.
    """
    # Generate Argument Description
    result = utils.arguments.description(description, default)

    # Assert
    assert result == expected
