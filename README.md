e<div align="center">
    <a href="https://pydantic-args.supimdos.com">
        <img src="https://raw.githubusercontent.com/SupImDos/pydantic-args/master/docs/assets/images/logo.svg" width="50%">
    </a>
    <h1>
        Pydantic Argparse
    </h1>
    <p>
        <em>Typed Argument Parsing with Pydantic</em>
    </p>
    <a href="https://pypi.python.org/pypi/pydantic-args">
        <img src="https://img.shields.io/pypi/v/pydantic-args.svg">
    </a>
    <a href="https://pepy.tech/project/pydantic-args">
        <img src="https://pepy.tech/badge/pydantic-args">
    </a>
    <a href="https://github.com/SupImDos/pydantic-args">
        <img src="https://img.shields.io/pypi/pyversions/pydantic-args.svg">
    </a>
    <a href="https://github.com/SupImDos/pydantic-args/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/SupImDos/pydantic-args.svg">
    </a>
    <br>
    <a href="https://github.com/SupImDos/pydantic-args/actions/workflows/tests.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-args/tests.yml?label=tests">
    </a>
    <a href="https://github.com/SupImDos/pydantic-args/actions/workflows/tests.yml">
        <img src="https://img.shields.io/coveralls/github/SupImDos/pydantic-args">
    </a>
    <a href="https://github.com/SupImDos/pydantic-args/actions/workflows/linting.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-args/linting.yml?label=linting">
    </a>
    <a href="https://github.com/SupImDos/pydantic-args/actions/workflows/typing.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-args/typing.yml?label=typing">
    </a>
</div>

## Help
See [documentation](https://pydantic-args.supimdos.com) for help.

## Installation
Installation with `pip` is simple:
```console
$ pip install pydantic-args
```

## Example
```py
import pydantic
import pydantic_args


class Arguments(pydantic.BaseModel):
    # Required Args
    string: str = pydantic.Field(description="a required string")
    integer: int = pydantic.Field(description="a required integer")
    flag: bool = pydantic.Field(description="a required flag")

    # Optional Args
    second_flag: bool = pydantic.Field(False, description="an optional flag")
    third_flag: bool = pydantic.Field(True, description="an optional flag")


def main() -> None:
    # Create Parser and Parse Args
    parser = pydantic_args.ArgumentParser(
        model=Arguments,
        prog="Example Program",
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
usage: Example Program [-h] [-v] --string STRING --integer INTEGER --flag |
                       --no-flag [--second-flag] [--no-third-flag]

Example Description

required arguments:
  --string STRING    a required string
  --integer INTEGER  a required integer
  --flag, --no-flag  a required flag

optional arguments:
  --second-flag      an optional flag (default: False)
  --no-third-flag    an optional flag (default: True)

help:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit

Example Epilog
```

```console
$ python3 example.py --string hello --integer 42 --flag
string='hello' integer=42 flag=True second_flag=False third_flag=True
```

## License
This project is licensed under the terms of the MIT license.
