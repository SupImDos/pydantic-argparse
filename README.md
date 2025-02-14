<div align="center">
<!-- Logo -->
<a href="https://pydantic-argparse.supimdos.com"><img src="https://raw.githubusercontent.com/SupImDos/pydantic-argparse/master/docs/assets/images/logo.svg" width="50%"></a>
<!-- Headings -->
<h1>Pydantic Argparse</h1>
<p><em>Typed Argument Parsing with Pydantic</em></p>
<!-- Badges (Row 1) -->
<a href="https://pypi.python.org/pypi/pydantic-argparse"><img src="https://img.shields.io/pypi/v/pydantic-argparse"></a>
<a href="https://pepy.tech/project/pydantic-argparse"><img src="https://img.shields.io/pepy/dt/pydantic-argparse?color=blue"></a>
<a href="https://github.com/SupImDos/pydantic-argparse"><img src="https://img.shields.io/pypi/pyversions/pydantic-argparse"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/blob/master/LICENSE"><img src="https://img.shields.io/github/license/SupImDos/pydantic-argparse"></a>
<br>
<!-- Badges (Row 2) -->
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/test.yml?label=tests"></a>
<a href="https://app.codecov.io/github/SupImDos/pydantic-argparse"><img src="https://img.shields.io/codecov/c/github/SupImDos/pydantic-argparse"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/lint.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/lint.yml?label=linting"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/format.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/format.yml?label=formatting"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/type.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/type.yml?label=typing"></a>
</div>

## Help
See [documentation](https://pydantic-argparse.supimdos.com) for help.

## Requirements
Requires Python 3.8+, and is compatible with the Pydantic v1 API.

## Installation
Installation with `pip` is simple:
```console
$ pip install pydantic-argparse
```

## Example
```py
import pydantic.v1 as pydantic

import pydantic_argparse


class Arguments(pydantic.BaseModel):
    # Required Args
    string: str = pydantic.Field(description="a required string", aliases=["-s"])
    integer: int = pydantic.Field(description="a required integer", aliases=["-i"])
    flag: bool = pydantic.Field(description="a required flag", aliases=["-f"])

    # Optional Args
    second_flag: bool = pydantic.Field(False, description="an optional flag")
    third_flag: bool = pydantic.Field(True, description="an optional flag")


def main() -> None:
    # Create Parser and Parse Args
    parser = pydantic_argparse.ArgumentParser(
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
usage: Example Program [-h] [-v] [-s STRING] [-i INTEGER] [-f | --flag | --no-flag]
                       [--second-flag] [--no-third-flag]

Example Description

required arguments:
  -s STRING, --string STRING
                        a required string
  -i INTEGER, --integer INTEGER
                        a required integer
  -f, --flag, --no-flag
                        a required flag

optional arguments:
  --second-flag         an optional flag (default: False)
  --no-third-flag       an optional flag (default: True)

help:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Example Epilog
```

```console
$ python3 example.py --string hello -i 42 -f
string='hello' integer=42 flag=True second_flag=False third_flag=True
```

## License
This project is licensed under the terms of the MIT license.
