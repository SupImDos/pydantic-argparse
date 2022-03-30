## Overview
`pydantic-argparse` provides functionality for commands. A command is a
positional command-line argument that is followed by its own subset of
command-line arguments. For example: `serve --address 0.0.0.0 --port 8080` or
`build --path abc --mode xyz`.

This section covers the following standard `argparse` argument functionality:

```python
# Subparser Commands
subparsers = parser.add_subparsers()
serve = subparsers.add_parser("serve")
serve.add_argument(...)
```

## Usage
The intended usage of commands is to provide the user with different
application behaviours, each with their own subset of arguments. For example:

```console
$ python3 example.py serve --address 0.0.0.0 --port 8080
```

```python
if args.serve:
    # Serve Command
    # We have typed access to any of the serve model arguments we defined
    # For example: `args.serve.address`, `args.serve.port`, etc.
    ...
```

## Pydantic Models
Commands can be created by first defining a `pydantic` model for the command,
containing its own subset of arguments. The command can then be added by
defining a `pydantic` field with a type of `:::python Optional[Command]`.
Despite each command itself being *optional*, overall a command is *always*
required, as outlined below.

### Required
*Required* commands are defined as follows:

```python
class Build(BaseModel):
    path: str = Field(description="build path")
    mode: str = Field(descroption="build mode")

class Serve(BaseModel):
    address: str = Field(description="serve address")
    port: int = Field(description="serve port")

class Arguments(BaseModel):
    # Commands
    build: Optional[Build] = Field(description="build command")
    serve: Optional[Serve] = Field(description="serve command")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] {build,serve} ...

commands:
  {build,serve}
    build        build command
    serve        serve command

help:
  -h, --help     show this help message and exit
```

This `Arguments` model also generates command-line interfaces for each of its
commands:

```console
$ python3 example.py build --help
usage: example.py build [-h] --path PATH --mode MODE

required arguments:
  --path PATH  build path
  --mode MODE  build mode

help:
  -h, --help   show this help message and exit
```

```console
$ python3 example.py serve --help
usage: example.py serve [-h] --address ADDRESS --port PORT

required arguments:
  --address ADDRESS  serve address
  --port PORT        serve port

help:
  -h, --help         show this help message and exit
```

Outcomes:

* Providing arguments of `build --path abc --mode xyz` will set `args.build`
  to `:::python Build(path="abc", mode="xyz")`, and `args.serve` to `None`.
* Providing arguments of `serve --address 127.0.0.1 --port 8080` will set
  `args.serve` to `:::python Serve(address="127.0.0.1", port=8080)`, and
  `args.build` to `None`.
* Commands cannot be omitted.
