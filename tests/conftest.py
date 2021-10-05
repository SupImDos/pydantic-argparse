#!/usr/bin/env python3
"""conftest.py

Configure Testing and Define Pytest Fixtures

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Standard
from collections import deque
from datetime import date, datetime, time, timedelta
from enum import Enum
import pathlib

# Third-Party
import pydantic
import pytest
import toml

# Typing
from typing import Any, Literal, Optional, Tuple  # pylint: disable=wrong-import-order


# Constants
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_TOML = PROJECT_ROOT.joinpath("pyproject.toml")


@pytest.fixture
def pyproject() -> dict[str, Any]:
    """Loads the project pyproject.toml.

    Returns:
        dict[str, Any]: pyproject.toml parsed as a dictionary.
    """
    # Load Project TOML
    return dict(toml.load(PROJECT_TOML))


class ExampleEnum(Enum):
    """Example Enum for Testing"""
    A = 1
    B = 2
    C = 3


class ExampleEnumSingle(Enum):
    """Example Enum with Single Member for Testing"""
    D = 4


class ExampleModel(pydantic.BaseModel):
    """Example Model for Testing"""
    # Required Arguments
    arg_01: int                            = pydantic.Field(description="arg_01")
    arg_02: float                          = pydantic.Field(description="arg_02")
    arg_03: str                            = pydantic.Field(description="arg_03")
    arg_04: bytes                          = pydantic.Field(description="arg_04")
    arg_05: list[str]                      = pydantic.Field(description="arg_05")
    arg_06: Tuple[str, str, str]           = pydantic.Field(description="arg_06")
    arg_07: set[str]                       = pydantic.Field(description="arg_07")
    arg_08: frozenset[str]                 = pydantic.Field(description="arg_08")
    arg_09: deque[str]                     = pydantic.Field(description="arg_09")
    arg_10: dict[str, int]                 = pydantic.Field(description="arg_10")
    arg_11: date                           = pydantic.Field(description="arg_11")
    arg_12: datetime                       = pydantic.Field(description="arg_12")
    arg_13: time                           = pydantic.Field(description="arg_13")
    arg_14: timedelta                      = pydantic.Field(description="arg_14")
    arg_15: bool                           = pydantic.Field(description="arg_15")
    arg_16: Literal["A"]                   = pydantic.Field(description="arg_16")
    arg_17: Literal["A", "B"]              = pydantic.Field(description="arg_17")
    arg_aa: ExampleEnumSingle              = pydantic.Field(description="arg_aa")
    arg_18: ExampleEnum                    = pydantic.Field(description="arg_18")

    # Optional Arguments (With Default)
    arg_19: int                            = pydantic.Field(12345,                         description="arg_19")
    arg_20: float                          = pydantic.Field(6.789,                         description="arg_20")
    arg_21: str                            = pydantic.Field("ABC",                         description="arg_21")
    arg_22: bytes                          = pydantic.Field(b"ABC",                        description="arg_22")
    arg_23: list[str]                      = pydantic.Field(list(("A", "B", "C")),         description="arg_23")
    arg_24: Tuple[str, str, str]           = pydantic.Field(tuple(("A", "B", "C")),        description="arg_24")
    arg_25: set[str]                       = pydantic.Field(set(("A", "B", "C")),          description="arg_25")
    arg_26: frozenset[str]                 = pydantic.Field(frozenset(("A", "B", "C")),    description="arg_26")
    arg_27: deque[str]                     = pydantic.Field(deque(("A", "B", "C")),        description="arg_27")
    arg_28: dict[str, int]                 = pydantic.Field(dict(A=123),                   description="arg_28")
    arg_29: date                           = pydantic.Field(date(2021, 12, 25),            description="arg_29")
    arg_30: datetime                       = pydantic.Field(datetime(2021, 12, 25, 7, 30), description="arg_30")
    arg_31: time                           = pydantic.Field(time(7, 30),                   description="arg_31")
    arg_32: timedelta                      = pydantic.Field(timedelta(hours=5),            description="arg_32")
    arg_33: bool                           = pydantic.Field(False,                         description="arg_33")
    arg_34: bool                           = pydantic.Field(True,                          description="arg_34")
    arg_bb: Literal["A"]                   = pydantic.Field("A",                           description="arg_bb")
    arg_35: Literal["A", "B"]              = pydantic.Field("A",                           description="arg_35")
    arg_cc: ExampleEnumSingle              = pydantic.Field(ExampleEnumSingle.D,           description="arg_cc")
    arg_36: ExampleEnum                    = pydantic.Field(ExampleEnum.A,                 description="arg_36")

    # Optional Arguments (No Default)
    arg_37: Optional[int]                  = pydantic.Field(description="arg_37")
    arg_38: Optional[float]                = pydantic.Field(description="arg_38")
    arg_39: Optional[str]                  = pydantic.Field(description="arg_39")
    arg_40: Optional[bytes]                = pydantic.Field(description="arg_40")
    arg_41: Optional[list[str]]            = pydantic.Field(description="arg_41")
    arg_42: Optional[Tuple[str, str, str]] = pydantic.Field(description="arg_42")
    arg_43: Optional[set[str]]             = pydantic.Field(description="arg_43")
    arg_44: Optional[frozenset[str]]       = pydantic.Field(description="arg_44")
    arg_45: Optional[deque[str]]           = pydantic.Field(description="arg_45")
    arg_46: Optional[dict[str, int]]       = pydantic.Field(description="arg_46")
    arg_47: Optional[date]                 = pydantic.Field(description="arg_47")
    arg_48: Optional[datetime]             = pydantic.Field(description="arg_48")
    arg_49: Optional[time]                 = pydantic.Field(description="arg_49")
    arg_50: Optional[timedelta]            = pydantic.Field(description="arg_50")
    arg_51: Optional[bool]                 = pydantic.Field(description="arg_51")
    arg_52: Optional[Literal["A"]]         = pydantic.Field(description="arg_52")
    arg_53: Optional[Literal["A", "B"]]    = pydantic.Field(description="arg_53")
    arg_dd: Optional[ExampleEnumSingle]    = pydantic.Field(description="arg_dd")
    arg_54: Optional[ExampleEnum]          = pydantic.Field(description="arg_54")
