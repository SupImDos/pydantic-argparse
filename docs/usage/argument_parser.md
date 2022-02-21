## Overview
The interface for `pydantic-argparse` is the custom typed
[`ArgumentParser`][pydantic_argparse.argparse.parser.ArgumentParser] class,
which provides declarative, typed argument parsing.

This `ArgumentParser` class presents a very *similar* interface to the `python`
standard library `argparse.ArgumentParser`, in an attempt to provide as close
to a drop-in-replacement as possible.

## Instantiation
Instantiation of the `ArgumentParser` is as follows:
```python
parser = pydantic_argparse.ArgumentParser(
    model=Arguments,
    prog="Program Name",
    description="Program Description",
    version="1.2.3",
    epilog="Program Epilog",
    add_help=True,
    exit_on_error=True,
)
```

### Required Parameters
The *required* parameters for the `ArgumentParser` are outlined below:

* `model` (`pydantic.BaseModel`):
    `pydantic` model that defines the command-line arguments

!!! note
    The supplied `pydantic` model is at the very core of `pydantic-argparse`,
    and its declaration and functionality are explained in further detail in
    the next section.

### Optional Parameters
The *optional* parameters for the `ArgumentParser` are outlined below:

* `prog` (`Optional[str]`):
    The program name that appears in the help message
* `description` (`Optional[str]`):
    The program description that appears in the help message
* `version` (`Optional[str]`):
    The program version that appears in the help message
* `epilog` (`Optional[str]`):
    The program epilog that appears in the help message
* `add_help` (`bool`):
    Whether to add the `-h / --help` help message
* `exit_on_error` (`bool`):
    Whether to exit on error, or just raise an `ArgumentError`

## Parsing
To parse command-line arguments into the `model` using the `ArgumentParser`:
```python
args = parser.parse_typed_args()
```

!!! info
    The `ArgumentParser` is *generic* over its `pydantic` `model`. This means
    that the parsed `args` object is type-hinted as an instance of its `model`.

### Optional Parameters
The *optional* parameters for the `parse_typed_args` method are outlined below:

* `args` (`Optional[list[str]]`):
    Optional list of arguments to parse *instead* of `sys.argv`
