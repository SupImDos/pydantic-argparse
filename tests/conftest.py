"""conftest.py

Configure Testing and Define Pytest Fixtures

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import annotations


# Standard
from collections import deque
from datetime import date, datetime, time, timedelta
from enum import Enum

# Third-Party
import pydantic

# Typing
from typing import Literal, Optional, Tuple  # pylint: disable=wrong-import-order


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
    arg_17: Literal["A", 1]                = pydantic.Field(description="arg_17")
    arg_18: ExampleEnumSingle              = pydantic.Field(description="arg_18")
    arg_19: ExampleEnum                    = pydantic.Field(description="arg_19")

    # Optional Arguments (With Default)
    arg_20: int                            = pydantic.Field(12345,                         description="arg_20")
    arg_21: float                          = pydantic.Field(6.789,                         description="arg_21")
    arg_22: str                            = pydantic.Field("ABC",                         description="arg_22")
    arg_23: bytes                          = pydantic.Field(b"ABC",                        description="arg_23")
    arg_24: list[str]                      = pydantic.Field(list(("A", "B", "C")),         description="arg_24")
    arg_25: Tuple[str, str, str]           = pydantic.Field(tuple(("A", "B", "C")),        description="arg_25")
    arg_26: set[str]                       = pydantic.Field(set(("A", "B", "C")),          description="arg_26")
    arg_27: frozenset[str]                 = pydantic.Field(frozenset(("A", "B", "C")),    description="arg_27")
    arg_28: deque[str]                     = pydantic.Field(deque(("A", "B", "C")),        description="arg_28")
    arg_29: dict[str, int]                 = pydantic.Field(dict(A=123),                   description="arg_29")
    arg_30: date                           = pydantic.Field(date(2021, 12, 25),            description="arg_30")
    arg_31: datetime                       = pydantic.Field(datetime(2021, 12, 25, 7, 30), description="arg_31")
    arg_32: time                           = pydantic.Field(time(7, 30),                   description="arg_32")
    arg_33: timedelta                      = pydantic.Field(timedelta(hours=5),            description="arg_33")
    arg_34: bool                           = pydantic.Field(False,                         description="arg_34")
    arg_35: bool                           = pydantic.Field(True,                          description="arg_35")
    arg_36: Literal["A"]                   = pydantic.Field("A",                           description="arg_36")
    arg_37: Literal["A", 1]                = pydantic.Field("A",                           description="arg_37")
    arg_38: ExampleEnumSingle              = pydantic.Field(ExampleEnumSingle.D,           description="arg_38")
    arg_39: ExampleEnum                    = pydantic.Field(ExampleEnum.A,                 description="arg_39")

    # Optional Arguments (No Default)
    arg_40: Optional[int]                  = pydantic.Field(description="arg_40")
    arg_41: Optional[float]                = pydantic.Field(description="arg_41")
    arg_42: Optional[str]                  = pydantic.Field(description="arg_42")
    arg_43: Optional[bytes]                = pydantic.Field(description="arg_43")
    arg_44: Optional[list[str]]            = pydantic.Field(description="arg_44")
    arg_45: Optional[Tuple[str, str, str]] = pydantic.Field(description="arg_45")
    arg_46: Optional[set[str]]             = pydantic.Field(description="arg_46")
    arg_47: Optional[frozenset[str]]       = pydantic.Field(description="arg_47")
    arg_48: Optional[deque[str]]           = pydantic.Field(description="arg_48")
    arg_49: Optional[dict[str, int]]       = pydantic.Field(description="arg_49")
    arg_50: Optional[date]                 = pydantic.Field(description="arg_50")
    arg_51: Optional[datetime]             = pydantic.Field(description="arg_51")
    arg_52: Optional[time]                 = pydantic.Field(description="arg_52")
    arg_53: Optional[timedelta]            = pydantic.Field(description="arg_53")
    arg_54: Optional[bool]                 = pydantic.Field(description="arg_54")
    arg_55: Optional[Literal["A"]]         = pydantic.Field(description="arg_55")
    arg_56: Optional[Literal["A", 1]]      = pydantic.Field(description="arg_56")
    arg_57: Optional[ExampleEnumSingle]    = pydantic.Field(description="arg_57")
    arg_58: Optional[ExampleEnum]          = pydantic.Field(description="arg_58")

    # Special Enums and Literals Optional Flag Behaviour
    arg_59: Optional[Literal["A"]]         = pydantic.Field(description="arg_59")
    arg_60: Optional[Literal["A"]]         = pydantic.Field("A", description="arg_60")
    arg_61: Optional[ExampleEnumSingle]    = pydantic.Field(description="arg_61")
    arg_62: Optional[ExampleEnumSingle]    = pydantic.Field(ExampleEnumSingle.D, description="arg_62")
