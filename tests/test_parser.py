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
from enum import Enum
import textwrap

# Third-Party
import pydantic
import pytest

# Local
from pydantic_argparse import ArgumentParser

# Typing
from typing import Any, Literal, Optional, Tuple, TypeVar  # pylint: disable=wrong-import-order


# Constants
ArgumentT = TypeVar("ArgumentT")
ExampleEnum = Enum("ExampleEnum", ("A", "B", "C"))


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
        (Literal["A"],         ..., "--test",                  "A"),
        (Literal["A", "B"],    ..., "--test B",                "B"),
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
        (Optional[bool],                 None, "", False),
        (Optional[Literal["A"]],         None, "", None),
        (Optional[Literal["A", "B"]],    None, "", None),
        (Optional[ExampleEnum],          None, "", None),
    ]
)
def test_arguments(
    argument_type: type[ArgumentT],
    argument_default: ArgumentT,
    arguments: str,
    result: ArgumentT,
    ) -> None:
    """Tests ArgumentParser.

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
        "exit_on_error",
        "error"
    ],
    [
        # Invalid Arguments (Exit on Error)
        (int,                  ..., "--test invalid",       True,  SystemExit),
        (float,                ..., "--test invalid",       True,  SystemExit),
        (list[int],            ..., "--test a b c",         True,  SystemExit),
        (Tuple[int, int, int], ..., "--test a b c",         True,  SystemExit),
        (set[int],             ..., "--test a b c",         True,  SystemExit),
        (frozenset[int],       ..., "--test a b c",         True,  SystemExit),
        (deque[int],           ..., "--test a b c",         True,  SystemExit),
        (dict[str, int],       ..., "--test {\"a\":\"b\"}", True,  SystemExit),
        (date,                 ..., "--test invalid",       True,  SystemExit),
        (datetime,             ..., "--test invalid",       True,  SystemExit),
        (time,                 ..., "--test invalid",       True,  SystemExit),
        (timedelta,            ..., "--test invalid",       True,  SystemExit),
        (Literal["A", "B"],    ..., "--test C",             True,  SystemExit),
        (ExampleEnum,          ..., "--test D",             True,  SystemExit),

        # Invalid Arguments (Raise on Error)
        (int,                  ..., "--test invalid",       False, argparse.ArgumentError),
        (float,                ..., "--test invalid",       False, argparse.ArgumentError),
        (list[int],            ..., "--test a b c",         False, argparse.ArgumentError),
        (Tuple[int, int, int], ..., "--test a b c",         False, argparse.ArgumentError),
        (set[int],             ..., "--test a b c",         False, argparse.ArgumentError),
        (frozenset[int],       ..., "--test a b c",         False, argparse.ArgumentError),
        (deque[int],           ..., "--test a b c",         False, argparse.ArgumentError),
        (dict[str, int],       ..., "--test {\"a\":\"b\"}", False, argparse.ArgumentError),
        (date,                 ..., "--test invalid",       False, argparse.ArgumentError),
        (datetime,             ..., "--test invalid",       False, argparse.ArgumentError),
        (time,                 ..., "--test invalid",       False, argparse.ArgumentError),
        (timedelta,            ..., "--test invalid",       False, argparse.ArgumentError),
        (Literal["A", "B"],    ..., "--test C",             False, argparse.ArgumentError),
        (ExampleEnum,          ..., "--test D",             False, argparse.ArgumentError),
    ]
)
def test_invalid_arguments(
    argument_type: type[ArgumentT],
    argument_default: ArgumentT,
    arguments: str,
    exit_on_error: bool,
    error: type[Exception],
    ) -> None:
    """Tests ArgumentParser.

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
    assert captured.out.strip() == textwrap.dedent(
        """
        usage: AA [-h] [-v]

        BB

        help:
          -h, --help     show this help message and exit
          -v, --version  show program's version number and exit

        DD
        """
    ).strip()
