#!/usr/bin/env python3
"""test_parser.py

Tests parser Module.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Standard
import argparse
from collections import deque
from datetime import date, datetime, time, timedelta
import re
import textwrap

# Third-Party
import pydantic
import pytest

# Local
from pydantic_argparse import ArgumentParser
from tests.conftest import ExampleModel, ExampleEnum, ExampleEnumSingle

# Typing
from typing import Any, Literal, Optional, Tuple, TypeVar  # pylint: disable=wrong-import-order


# Constants
ArgumentT = TypeVar("ArgumentT")


@pytest.mark.parametrize(["prog"],          [("AA",), (None,)])
@pytest.mark.parametrize(["description"],   [("BB",), (None,)])
@pytest.mark.parametrize(["version"],       [("CC",), (None,)])
@pytest.mark.parametrize(["epilog"],        [("DD",), (None,)])
@pytest.mark.parametrize(["add_help"],      [(True,), (False,)])
@pytest.mark.parametrize(["exit_on_error"], [(True,), (False,)])
def test_create_argparser(
    prog: Optional[str],
    description: Optional[str],
    version: Optional[str],
    epilog: Optional[str],
    add_help: bool,
    exit_on_error: bool,
    ) -> None:
    """Tests Constructing the ArgumentParser.

    Args:
        prog (Optional[str]): Program name for testing.
        description (Optional[str]): Program description for testing.
        version (Optional[str]): Program version for testing.
        epilog (Optional[str]): Program epilog for testing.
        add_help (bool): Whether to add help flag for testing.
        exit_on_error (bool): Whether to exit on error for testing.
    """
    # Create ArgumentParser
    parser = ArgumentParser(
        model=ExampleModel,
        prog=prog,
        description=description,
        version=version,
        epilog=epilog,
        add_help=add_help,
        exit_on_error=exit_on_error,
    )

    # Asserts
    assert isinstance(parser, ArgumentParser)


@pytest.mark.parametrize(
    [
        "argument_type",
        "argument_default",
        "arguments",
        "result",
    ],
    [
        # Required Arguments
        (int,                  ..., "--test 123",              123),
        (float,                ..., "--test 4.56",             4.56),
        (str,                  ..., "--test hello",            "hello"),
        (bytes,                ..., "--test bytes",            b"bytes"),
        (list[str],            ..., "--test a b c",            list(("a", "b", "c"))),
        (Tuple[str, str, str], ..., "--test a b c",            tuple(("a", "b", "c"))),
        (set[str],             ..., "--test a b c",            set(("a", "b", "c"))),
        (frozenset[str],       ..., "--test a b c",            frozenset(("a", "b", "c"))),
        (deque[str],           ..., "--test a b c",            deque(("a", "b", "c"))),
        (dict[str, int],       ..., "--test {\"a\":2}",        dict(a=2)),
        (date,                 ..., "--test 2021-12-25",       date(2021, 12, 25)),
        (datetime,             ..., "--test 2021-12-25T12:34", datetime(2021, 12, 25, 12, 34)),
        (time,                 ..., "--test 12:34",            time(12, 34)),
        (timedelta,            ..., "--test PT12H",            timedelta(hours=12)),
        (bool,                 ..., "--test",                  True),
        (bool,                 ..., "--no-test",               False),
        (Literal["A"],         ..., "--test A",                "A"),
        (Literal["A", "B"],    ..., "--test B",                "B"),
        (ExampleEnumSingle,    ..., "--test D",                ExampleEnumSingle.D),
        (ExampleEnum,          ..., "--test C",                ExampleEnum.C),

        # Optional Arguments (With Default)
        (int,                  456,                            "--test 123",              123),
        (float,                1.23,                           "--test 4.56",             4.56),
        (str,                  "world",                        "--test hello",            "hello"),
        (bytes,                b"bits",                        "--test bytes",            b"bytes"),
        (list[str],            list(("d", "e", "f")),          "--test a b c",            list(("a", "b", "c"))),
        (Tuple[str, str, str], tuple(("d", "e", "f")),         "--test a b c",            tuple(("a", "b", "c"))),
        (set[str],             set(("d", "e", "f")),           "--test a b c",            set(("a", "b", "c"))),
        (frozenset[str],       frozenset(("d", "e", "f")),     "--test a b c",            frozenset(("a", "b", "c"))),
        (deque[str],           deque(("d", "e", "f")),         "--test a b c",            deque(("a", "b", "c"))),
        (dict[str, int],       dict(b=3),                      "--test {\"a\":2}",        dict(a=2)),
        (date,                 date(2021, 7, 21),              "--test 2021-12-25",       date(2021, 12, 25)),
        (datetime,             datetime(2021, 7, 21, 3, 21),   "--test 2021-04-03T02:01", datetime(2021, 4, 3, 2, 1)),
        (time,                 time(3, 21),                    "--test 12:34",            time(12, 34)),
        (timedelta,            timedelta(hours=6),             "--test PT12H",            timedelta(hours=12)),
        (bool,                 False,                          "--test",                  True),
        (bool,                 True,                           "--no-test",               False),
        (Literal["A"],         "A",                            "--test",                  "A"),
        (Literal["A", "B"],    "A",                            "--test B",                "B"),
        (ExampleEnumSingle,    ExampleEnumSingle.D,            "--test",                  ExampleEnumSingle.D),
        (ExampleEnum,          ExampleEnum.B,                  "--test C",                ExampleEnum.C),

        # Optional Arguments (With Default) (No Value Given)
        (int,                  456,                            "", 456),
        (float,                1.23,                           "", 1.23),
        (str,                  "world",                        "", "world"),
        (bytes,                b"bits",                        "", b"bits"),
        (list[str],            list(("d", "e", "f")),          "", list(("d", "e", "f"))),
        (Tuple[str, str, str], tuple(("d", "e", "f")),         "", tuple(("d", "e", "f"))),
        (set[str],             set(("d", "e", "f")),           "", set(("d", "e", "f"))),
        (frozenset[str],       frozenset(("d", "e", "f")),     "", frozenset(("d", "e", "f"))),
        (deque[str],           deque(("d", "e", "f")),         "", deque(("d", "e", "f"))),
        (dict[str, int],       dict(b=3),                      "", dict(b=3)),
        (date,                 date(2021, 7, 21),              "", date(2021, 7, 21)),
        (datetime,             datetime(2021, 7, 21, 3, 21),   "", datetime(2021, 7, 21, 3, 21)),
        (time,                 time(3, 21),                    "", time(3, 21)),
        (timedelta,            timedelta(hours=6),             "", timedelta(hours=6)),
        (bool,                 False,                          "", False),
        (bool,                 True,                           "", True),
        (Literal["A"],         "A",                            "", "A"),
        (Literal["A", "B"],    "A",                            "", "A"),
        (ExampleEnumSingle,    ExampleEnumSingle.D,            "", ExampleEnumSingle.D),
        (ExampleEnum,          ExampleEnum.B,                  "", ExampleEnum.B),

        # Optional Arguments (No Default)
        (Optional[int],                  None, "--test 123",              123),
        (Optional[float],                None, "--test 4.56",             4.56),
        (Optional[str],                  None, "--test hello",            "hello"),
        (Optional[bytes],                None, "--test bytes",            b"bytes"),
        (Optional[list[str]],            None, "--test a b c",            list(("a", "b", "c"))),
        (Optional[Tuple[str, str, str]], None, "--test a b c",            tuple(("a", "b", "c"))),
        (Optional[set[str]],             None, "--test a b c",            set(("a", "b", "c"))),
        (Optional[frozenset[str]],       None, "--test a b c",            frozenset(("a", "b", "c"))),
        (Optional[deque[str]],           None, "--test a b c",            deque(("a", "b", "c"))),
        (Optional[dict[str, int]],       None, "--test {\"a\":2}",        dict(a=2)),
        (Optional[date],                 None, "--test 2021-12-25",       date(2021, 12, 25)),
        (Optional[datetime],             None, "--test 2021-12-25T12:34", datetime(2021, 12, 25, 12, 34)),
        (Optional[time],                 None, "--test 12:34",            time(12, 34)),
        (Optional[timedelta],            None, "--test PT12H",            timedelta(hours=12)),
        (Optional[bool],                 None, "--test",                  True),
        (Optional[Literal["A"]],         None, "--test",                  "A"),
        (Optional[Literal["A", "B"]],    None, "--test B",                "B"),
        (Optional[ExampleEnumSingle],    None, "--test",                  ExampleEnumSingle.D),
        (Optional[ExampleEnum],          None, "--test C",                ExampleEnum.C),

        # Optional Arguments (No Default) (No Value Given)
        (Optional[int],                  None, "", None),
        (Optional[float],                None, "", None),
        (Optional[str],                  None, "", None),
        (Optional[bytes],                None, "", None),
        (Optional[list[str]],            None, "", None),
        (Optional[Tuple[str, str, str]], None, "", None),
        (Optional[set[str]],             None, "", None),
        (Optional[frozenset[str]],       None, "", None),
        (Optional[deque[str]],           None, "", None),
        (Optional[dict[str, int]],       None, "", None),
        (Optional[date],                 None, "", None),
        (Optional[datetime],             None, "", None),
        (Optional[time],                 None, "", None),
        (Optional[timedelta],            None, "", None),
        (Optional[bool],                 None, "", None),
        (Optional[Literal["A"]],         None, "", None),
        (Optional[Literal["A", "B"]],    None, "", None),
        (Optional[ExampleEnumSingle],    None, "", None),
        (Optional[ExampleEnum],          None, "", None),
    ]
)
def test_arguments(
    argument_type: type[ArgumentT],
    argument_default: ArgumentT,
    arguments: str,
    result: ArgumentT,
    ) -> None:
    """Tests ArgumentParser Valid Arguments.

    Args:
        argument_type (type[ArgumentT]): Type of the argument.
        argument_default (ArgumentT): Default for the argument.
        arguments (str): An example string of arguments for testing.
        result (ArgumentT): Result from parsing the argument.
    """
    # Dynamically Create Pydantic Model
    model: Any = pydantic.create_model(
        "model",
        test=(argument_type, argument_default),
    )

    # Create ArgumentParser
    parser = ArgumentParser(model)

    # Parse
    args = parser.parse_typed_args(arguments.split())

    # Asserts
    assert isinstance(args.test, type(result))
    assert args.test == result


@pytest.mark.parametrize(
    [
        "argument_type",
        "argument_default",
        "arguments",
    ],
    [
        # Invalid Arguments
        (int,                  ..., "--test invalid"),
        (float,                ..., "--test invalid"),
        (list[int],            ..., "--test invalid"),
        (Tuple[int, int, int], ..., "--test invalid"),
        (set[int],             ..., "--test invalid"),
        (frozenset[int],       ..., "--test invalid"),
        (deque[int],           ..., "--test invalid"),
        (dict[str, int],       ..., "--test invalid"),
        (date,                 ..., "--test invalid"),
        (datetime,             ..., "--test invalid"),
        (time,                 ..., "--test invalid"),
        (timedelta,            ..., "--test invalid"),
        (bool,                 ..., "--test invalid"),
        (Literal["A"],         ..., "--test invalid"),
        (Literal["A", "B"],    ..., "--test invalid"),
        (ExampleEnumSingle,    ..., "--test invalid"),
        (ExampleEnum,          ..., "--test invalid"),

        # Missing Argument Values
        (int,                  ..., "--test"),
        (float,                ..., "--test"),
        (str,                  ..., "--test"),
        (bytes,                ..., "--test"),
        (list[int],            ..., "--test"),
        (Tuple[int, int, int], ..., "--test"),
        (set[int],             ..., "--test"),
        (frozenset[int],       ..., "--test"),
        (deque[int],           ..., "--test"),
        (dict[str, int],       ..., "--test"),
        (date,                 ..., "--test"),
        (datetime,             ..., "--test"),
        (time,                 ..., "--test"),
        (timedelta,            ..., "--test"),
        (Literal["A"],         ..., "--test"),
        (Literal["A", "B"],    ..., "--test"),
        (ExampleEnumSingle,    ..., "--test"),
        (ExampleEnum,          ..., "--test"),

        # Missing Arguments
        (int,                  ..., ""),
        (float,                ..., ""),
        (str,                  ..., ""),
        (bytes,                ..., ""),
        (list[int],            ..., ""),
        (Tuple[int, int, int], ..., ""),
        (set[int],             ..., ""),
        (frozenset[int],       ..., ""),
        (deque[int],           ..., ""),
        (dict[str, int],       ..., ""),
        (date,                 ..., ""),
        (datetime,             ..., ""),
        (time,                 ..., ""),
        (timedelta,            ..., ""),
        (bool,                 ..., ""),
        (Literal["A"],         ..., ""),
        (Literal["A", "B"],    ..., ""),
        (ExampleEnumSingle,    ..., ""),
        (ExampleEnum,          ..., ""),

        # Invalid Optional Arguments
        (Optional[int],                  None, "--test invalid"),
        (Optional[float],                None, "--test invalid"),
        (Optional[list[int]],            None, "--test invalid"),
        (Optional[Tuple[int, int, int]], None, "--test invalid"),
        (Optional[set[int]],             None, "--test invalid"),
        (Optional[frozenset[int]],       None, "--test invalid"),
        (Optional[deque[int]],           None, "--test invalid"),
        (Optional[dict[str, int]],       None, "--test invalid"),
        (Optional[date],                 None, "--test invalid"),
        (Optional[datetime],             None, "--test invalid"),
        (Optional[time],                 None, "--test invalid"),
        (Optional[timedelta],            None, "--test invalid"),
        (Optional[bool],                 None, "--test invalid"),
        (Optional[Literal["A"]],         None, "--test invalid"),
        (Optional[Literal["A", "B"]],    None, "--test invalid"),
        (Optional[ExampleEnumSingle],    None, "--test invalid"),
        (Optional[ExampleEnum],          None, "--test invalid"),

        # Missing Optional Argument Values
        (Optional[int],                  None, "--test"),
        (Optional[float],                None, "--test"),
        (Optional[str],                  None, "--test"),
        (Optional[bytes],                None, "--test"),
        (Optional[list[int]],            None, "--test"),
        (Optional[Tuple[int, int, int]], None, "--test"),
        (Optional[set[int]],             None, "--test"),
        (Optional[frozenset[int]],       None, "--test"),
        (Optional[deque[int]],           None, "--test"),
        (Optional[dict[str, int]],       None, "--test"),
        (Optional[date],                 None, "--test"),
        (Optional[datetime],             None, "--test"),
        (Optional[time],                 None, "--test"),
        (Optional[timedelta],            None, "--test"),
        (Optional[Literal["A", "B"]],    None, "--test"),
        (Optional[ExampleEnum],          None, "--test"),
    ]
)
@pytest.mark.parametrize(
    [
        "exit_on_error",
        "error"
    ],
    [
        (True,  SystemExit),
        (False, argparse.ArgumentError),
    ]
)
def test_invalid_arguments(
    argument_type: type[ArgumentT],
    argument_default: ArgumentT,
    arguments: str,
    exit_on_error: bool,
    error: type[Exception],
    ) -> None:
    """Tests ArgumentParser Invalid Arguments.

    Args:
        argument_type (type[ArgumentT]): Type of the argument.
        argument_default (ArgumentT): Default for the argument.
        arguments (str): An example string of arguments for testing.
        exit_on_error (bool): Whether to raise or exit on error.
        error (type[Exception]): Exception that should be raised for testing.
    """
    # Dynamically Create Pydantic Model
    model: Any = pydantic.create_model(
        "model",
        test=(argument_type, argument_default),
    )

    # Create ArgumentParser
    parser = ArgumentParser(model, exit_on_error=exit_on_error)

    # Assert Parser Raises Error
    with pytest.raises(error):
        # Parse
        parser.parse_typed_args(arguments.split())


def test_help_message(capsys: pytest.CaptureFixture[str]) -> None:
    """Tests ArgumentParser Help Message.

    Args:
        capsys (pytest.CaptureFixture[str]): Fixture to capture STDOUT/STDERR.
    """
    # Dynamically Create Pydantic Model
    model: Any = pydantic.create_model("model")

    # Create ArgumentParser
    parser = ArgumentParser(
        model=model,
        prog="AA",
        description="BB",
        version="CC",
        epilog="DD",
    )

    # Assert Parser Exits
    with pytest.raises(SystemExit):
        # Ask for Help
        parser.parse_typed_args(["--help"])

    # Check STDOUT
    captured = capsys.readouterr()
    assert captured.out == textwrap.dedent(
        """
        usage: AA [-h] [-v]

        BB

        help:
          -h, --help     show this help message and exit
          -v, --version  show program's version number and exit

        DD
        """
    ).lstrip()


def test_version_message(capsys: pytest.CaptureFixture[str]) -> None:
    """Tests ArgumentParser Version Message.

    Args:
        capsys (pytest.CaptureFixture[str]): Fixture to capture STDOUT/STDERR.
    """
    # Dynamically Create Pydantic Model
    model: Any = pydantic.create_model("model")

    # Create ArgumentParser
    parser = ArgumentParser(
        model=model,
        prog="AA",
        description="BB",
        version="CC",
        epilog="DD",
    )

    # Assert Parser Exits
    with pytest.raises(SystemExit):
        # Ask for Version
        parser.parse_typed_args(["--version"])

    # Check STDOUT
    captured = capsys.readouterr()
    assert captured.out == textwrap.dedent(
        """
        CC
        """
    ).lstrip()


@pytest.mark.parametrize(
    [
        "argument_name",
        "argument_field",
    ],
    ExampleModel.__fields__.items()
)
def test_argument_descriptions(
    argument_name: str,
    argument_field: pydantic.fields.ModelField,
    capsys: pytest.CaptureFixture[str],
    ) -> None:
    """Tests Argument Descriptions.

    Args:
        argument_name (str): Argument name.
        argument_field (pydantic.fields.ModelField): Argument pydantic field.
        capsys (pytest.CaptureFixture[str]): Fixture to capture STDOUT/STDERR.
    """
    # Create ArgumentParser
    parser = ArgumentParser(ExampleModel)

    # Assert Parser Exits
    with pytest.raises(SystemExit):
        # Ask for Help
        parser.parse_typed_args(["--help"])

    # Capture STDOUT
    captured = capsys.readouterr()

    # Process STDOUT
    # Capture all arguments below 'required arguments:'
    # Capture all arguments below 'optional arguments:'
    _, required, optional, _ = re.split(r".+:\n", captured.out)

    # Format Argument Name
    argument_name = argument_name.replace("_", "-")

    # Check if Required or Optional
    if argument_field.required:
        # Assert Argument in Required Args Section
        assert argument_name in required
        assert argument_name not in optional
        assert argument_field.field_info.description in required
        assert argument_field.field_info.description not in optional

    else:
        # Assert Argument in Optional Args Section
        assert argument_name in optional
        assert argument_name not in required
        assert argument_field.field_info.description in optional
        assert argument_field.field_info.description not in required
        assert f"(default: {argument_field.default})" in optional
        assert f"(default: {argument_field.default})" not in required
