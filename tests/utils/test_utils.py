"""Tests the `utils` Module.

This module provides full unit test coverage for the `utils` module, testing
all branches of all functions.
"""


# Standard
import argparse

# Third-Party
import pytest

# Local
from pydantic_argparse.utils import utils

# Typing
from typing import Any, Optional  # pylint: disable=wrong-import-order


@pytest.mark.parametrize(
    [
        "name",
        "expected",
    ],
    [
        ("test", "--test"),
        ("test_two", "--test-two"),
    ]
)
def test_argument_name(
    name: str,
    expected: str,
    ) -> None:
    """Tests utils.argument_name Function.

    Args:
        name (str): Argument name to test.
        expected (str): Expected result of the test.
    """
    # Generate Argument Name
    result = utils.argument_name(name)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    [
        "description",
        "default",
        "expected",
    ],
    [
        ("A",  "A",           "A (default: A)"),
        ("A",  5,             "A (default: 5)"),
        ("A",  None,          "A (default: None)"),
        ("A",  utils.MISSING, "A"),
        (None, "A",           "(default: A)"),
        (None, 5,             "(default: 5)"),
        (None, None,          "(default: None)"),
        (None, utils.MISSING, ""),
    ]
)
def test_argument_description(
    description: Optional[str],
    default: Optional[Any],
    expected: str,
    ) -> None:
    """Tests utils.argument_description Function.

    Args:
        description (Optional[str]): Optional argument description to test.
        default (Optional[Any]): Optional argument default to test.
        expected (str): Expected result of the test.
    """
    # Generate Argument Description
    result = utils.argument_description(description, default)

    # Assert
    assert result == expected


def test_namespace_to_dict() -> None:
    """Tests utils.namespace_to_dict Function."""
    # Generate Dictionary
    result = utils.namespace_to_dict(
        argparse.Namespace(
            a="1",
            b=2,
            c=argparse.Namespace(
                d="3",
                e=4,
                f=argparse.Namespace(
                    g=5,
                    h="6",
                    i=7,
                )
            )
        )
    )

    # Assert
    assert result == {
        "a": "1",
        "b": 2,
        "c": {
            "d": "3",
            "e": 4,
            "f": {
                "g": 5,
                "h": "6",
                "i": 7,
            }
        }
    }


def test_type_caster() -> None:
    """Tests utils.type_caster Function."""
    # Create Lambda to Test
    test = lambda x, y, z: x + y + z

    # Generate Type Caster
    result = utils.type_caster("abc", test, y="y", z="z")

    # Assert
    assert result.__name__ == "abc"
    assert result("x") == "xyz"
