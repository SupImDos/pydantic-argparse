"""Tests the `actions` Module.

This module provides full unit test coverage for the `actions` module, testing
all branches of all methods. These unit tests target the `SubParsersAction`
class by testing the expected nested namespace functionality.
"""


# Standard
import argparse

# Third-Party
import pytest

# Local
from pydantic_argparse.argparse import actions


def test_invalid_command(sub_parsers_action: actions.SubParsersAction) -> None:
    """Tests SubParsersAction with invalid command.

    Args:
        sub_parsers_action (SubParsersAction): PyTest SubParsersAction fixture.
    """
    # Assert Raises
    with pytest.raises(argparse.ArgumentError):
        # Test Invalid Command
        sub_parsers_action(
            parser=argparse.ArgumentParser(),
            namespace=argparse.Namespace(),
            values=["fake", "--not-real"],
        )


def test_valid_command(sub_parsers_action: actions.SubParsersAction) -> None:
    """Tests SubParsersAction with valid command.

    Args:
        sub_parsers_action (SubParsersAction): PyTest SubParsersAction fixture.
    """
    # Add Test Argument
    sub_parsers_action.add_parser("test")

    # Create Namespace
    namespace = argparse.Namespace()

    # Test Valid Command
    sub_parsers_action(
        parser=argparse.ArgumentParser(),
        namespace=namespace,
        values=["test"],
    )

    # Assert
    assert getattr(namespace, "test") == argparse.Namespace()  # noqa: B009


def test_unrecognised_args(sub_parsers_action: actions.SubParsersAction) -> None:
    """Tests SubParsersAction with unrecognised args.

    Args:
        sub_parsers_action (SubParsersAction): PyTest SubParsersAction fixture.
    """
    # Add Test Argument
    sub_parsers_action.add_parser("test")

    # Create Namespace
    namespace = argparse.Namespace()

    # Test Unrecognised Args
    sub_parsers_action(
        parser=argparse.ArgumentParser(),
        namespace=namespace,
        values=["test", "--flag"],
    )

    # Assert
    assert getattr(namespace, "test") == argparse.Namespace()  # noqa: B009
    assert getattr(namespace, argparse._UNRECOGNIZED_ARGS_ATTR) == ["--flag"]


def test_deep_unrecognised_args(sub_parsers_action: actions.SubParsersAction) -> None:
    """Tests SubParsersAction with deeply nested unrecognised args.

    Args:
        sub_parsers_action (SubParsersAction): PyTest SubParsersAction fixture.
    """
    # Add Test Argument
    deep: argparse.ArgumentParser = sub_parsers_action.add_parser("test")
    deep.add_subparsers(action=actions.SubParsersAction).add_parser("deep")

    # Create Namespace
    namespace = argparse.Namespace()

    # Test Deeply Nested Unrecognised Args
    sub_parsers_action(
        parser=argparse.ArgumentParser(),
        namespace=namespace,
        values=["test", "--a", "deep", "--b"],
    )

    # Assert
    assert getattr(namespace, "test") == argparse.Namespace(deep=argparse.Namespace())  # noqa: B009
    assert getattr(namespace, argparse._UNRECOGNIZED_ARGS_ATTR) == ["--a", "--b"]
