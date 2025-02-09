"""Tests the `arguments` Module.

This module provides full unit test coverage for the `arguments` module,
testing all branches of all functions.
"""

import pytest

from pydantic_argparse import utils
from tests import conftest as conf

from typing import Any, List, Optional


@pytest.mark.parametrize(
    (
        "name",
        "aliases",
        "invert",
        "expected",
    ),
    [
        ("test", ["-t", "-te"], False, ["-t", "-te", "--test"]),
        ("test", ["-nt"], True, ["-nt", "--no-test"]),
        ("test_two", [], False, ["--test-two"]),
        ("test_two", [], True, ["--no-test-two"]),
    ],
)
def test_argument_names(
    name: str,
    aliases: List[str],
    invert: bool,
    expected: str,
) -> None:
    """Tests `utils.arguments.names` Function.

    Args:
        name (str): Argument name to test.
        aliases (List[str]): List of aliases.
        invert (bool): Whether to invert the name.
        expected (str): Expected result of the test.
    """
    # Construct Pydantic Field
    field = conf.create_test_field(name, aliases=aliases)

    # Generate Argument Name
    result = utils.arguments.names(field, invert)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    (
        "description",
        "default",
        "expected",
    ),
    [
        ("A", "B", "A (default: B)"),
        ("A", 5, "A (default: 5)"),
        ("A", None, "A (default: None)"),
        ("A", ..., "A"),
        (None, "B", "(default: B)"),
        (None, 5, "(default: 5)"),
        (None, None, "(default: None)"),
        (None, ..., ""),
    ],
)
def test_argument_description(
    description: Optional[str],
    default: Any,
    expected: str,
) -> None:
    """Tests `utils.arguments.description` Function.

    Args:
        description (Optional[str]): Optional argument description to test.
        default (Any): Optional argument default value to test.
        expected (str): Expected result of the test.
    """
    # Construct Pydantic Field
    field = conf.create_test_field(default=default, description=description)

    # Generate Argument Description
    result = utils.arguments.description(field)

    # Assert
    assert result == expected
