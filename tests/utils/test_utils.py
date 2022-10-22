"""Tests the `utils` Module.

This module provides full unit test coverage for the `utils` module, testing
all branches of all functions.
"""


# Standard
import argparse
import collections
import collections.abc
import enum

# Third-Party
import pydantic
import pytest

# Local
from pydantic_argparse.utils import utils
import tests.conftest as conf

# Typing
from typing import Any, Literal, Optional


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
    (
        "description",
        "default",
        "expected",
    ),
    [
        ("A",  "A",           "A (default: A)"),
        ("A",  5,             "A (default: 5)"),
        ("A",  None,          "A (default: None)"),
        ("A",  utils.MISSING, "A"),
        (None, "A",           "(default: A)"),
        (None, 5,             "(default: 5)"),
        (None, None,          "(default: None)"),
        (None, utils.MISSING, ""),
    ],
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
    test = lambda x, y, z: x + y + z  # noqa: E731

    # Generate Type Caster
    result = utils.type_caster("abc", test, y="y", z="z")

    # Assert
    assert result.__name__ == "abc"
    assert result("x") == "xyz"


@pytest.mark.parametrize(
    (
        "field_type",
        "expected_type",
    ),
    [
        (bool,                   bool),
        (int,                    int),
        (float,                  float),
        (str,                    str),
        (bytes,                  bytes),
        (list,                   list),
        (list,                   collections.abc.Container),
        (list[str],              list),
        (list[str],              collections.abc.Container),
        (tuple,                  tuple),
        (tuple,                  collections.abc.Container),
        (tuple[str, ...],        tuple),
        (tuple[str, ...],        collections.abc.Container),
        (set,                    set),
        (set,                    collections.abc.Container),
        (set[str],               set),
        (set[str],               collections.abc.Container),
        (frozenset,              frozenset),
        (frozenset,              collections.abc.Container),
        (frozenset[str],         frozenset),
        (frozenset[str],         collections.abc.Container),
        (collections.deque,      collections.deque),
        (collections.deque,      collections.abc.Container),
        (collections.deque[str], collections.deque),
        (collections.deque[str], collections.abc.Container),
        (dict,                   dict),
        (dict,                   collections.abc.Mapping),
        (dict[str, int],         dict),
        (dict[str, int],         collections.abc.Mapping),
        (Literal["A"],           Literal),
        (Literal[1, 2, 3],       Literal),
        (conf.TestCommand,       pydantic.BaseModel),
        (conf.TestCommands,      pydantic.BaseModel),
        (conf.TestEnum,          enum.Enum),
        (conf.TestEnumSingle,    enum.Enum),
    ],
)
def test_is_field_a(field_type: Any, expected_type: Any) -> None:
    """Tests utils.is_field_a Function.

    Args:
        field_type (Any): Field type to test.
        expected_type (Any): Expected type to check for the field.
    """
    # Dynamically Create Field
    field = pydantic.fields.ModelField(
        name="test",
        type_=field_type,
        class_validators=None,
        model_config=pydantic.BaseConfig,
    )

    # Check and Assert Field Type
    assert utils.is_field_a(field, expected_type)
