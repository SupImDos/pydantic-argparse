## Overview
`pydantic-argparse` provides functionality for boolean flag arguments through
the use of `pydantic` fields with a type of "`:::python bool`".

This provides the standard `argparse` functionality of:

* `:::python action=argparse.BooleanOptionalAction`
* `:::python action="store_true"`
* `:::python action="store_false"`

## Usage
The indented usage of boolean flags is to enable or disable features. For
example:

```console
$ python3 example.py --debug
```

```python
if args.debug:
    log.setLevel(logging.DEBUG)
```

## Boolean Flags
There are 3 different kinds of boolean flag arguments, which are outlined
below.

### Required
A *required* boolean flag is defined as follows:

```python
class Arguments(BaseModel):
    # Required Flag
    flag: bool = Field(description="this argument is a required flag")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] --flag | --no-flag

required arguments:
  --flag, --no-flag  this argument is a required flag

help:
  -h, --help         show this help message and exit
```

Outcomes:

* Providing an argument of `--flag` will set `args.flag` to `True`.
* Providing an argument of `--no-flag` will set `args.flag` to `False`.
* This argument cannot be omitted.

### Optional (Default `False`)
An *optional* boolean flag with a default of `False` is defined as follows:

```python
class Arguments(BaseModel):
    # Optional Flag (Default True)
    flag: bool = Field(False, description="this argument is an optional flag")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] [--flag]

optional arguments:
  --flag      this argument is an optional flag (default: False)

help:
  -h, --help  show this help message and exit
```

Outcomes:

* Providing an argument of `--flag` will set `args.flag` to `True`.
* Omitting this argument will set `args.flag` to `False` (the default).

### Optional (Default `True`)
An *optional* boolean flag with a default of `True` is defined as follows:

```python
class Arguments(BaseModel):
    # Optional Flag (Default True)
    flag: bool = Field(True, description="this argument is an optional flag")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] [--no-flag]

optional arguments:
  --no-flag   this argument is an optional flag (default: True)

help:
  -h, --help  show this help message and exit
```

Outcomes:

* Providing an argument of `--no-flag` will set `args.flag` to `False`.
* Omitting this argument will set `args.flag` to `True` (the default).
