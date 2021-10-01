# pydantic-argparse

[![pypi](https://img.shields.io/pypi/v/pydantic-argparse.svg)](https://pypi.python.org/pypi/pydantic-argparse)
[![downloads](https://pepy.tech/badge/pydantic-argparse)](https://pepy.tech/project/pydantic-argparse)
[![versions](https://img.shields.io/pypi/pyversions/pydantic-argparse.svg)](https://github.com/SupImDos/pydantic-argparse)
[![license](https://img.shields.io/github/license/SupImDos/pydantic-argparse.svg)](https://github.com/SupImDos/pydantic-argparse/blob/master/LICENSE)


Typed Argument Parsing with Pydantic

## Help

Documentation coming soon.

## Installation

Install using:
* `pip3 install pydantic-argparse`

## Example

```py
import pydantic
import pydantic_argparse


class Arguments(pydantic.BaseModel):
    """Arguments for CLI"""
    # Required Args
    aaa: str = pydantic.Field(description="I'm a required string")
    bbb: int = pydantic.Field(description="I'm a required integer")
    ccc: bool = pydantic.Field(description="I'm a required bool")

    # Optional Args
    ddd: bool = pydantic.Field(False, description="I'm an optional bool (default False)")
    eee: bool = pydantic.Field(True, description="I'm an optional bool (default True)")


def main() -> None:
    """Main example function."""
    # Create Parser and Parse Args
    parser = pydantic_argparse.ArgumentParser(
        model=Arguments,
        prog="Example",
        description="Example Description",
        version="0.0.1",
        epilog="Example Epilog",
    )
    args = parser.parse_typed_args()

    # Print Args
    print(args)


if __name__ == "__main__":
    main()
```

```console
$ python3 example.py --help

usage: Example [-h] [-v] --aaa AAA --bbb BBB --ccc | --no-ccc [--ddd] [--no-eee]

Example Description

required arguments:
  --aaa AAA          I'm a required string
  --bbb BBB          I'm a required integer
  --ccc, --no-ccc    I'm a required bool

optional arguments:
  --ddd              I'm an optional bool (default False)
  --no-eee           I'm an optional bool (default True)

help:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit

Example Epilog
```

```console
$ python3 example.py --aaa hello --bbb 123 --no-ccc

aaa='hello' bbb=123 ccc=False ddd=False eee=True
```
