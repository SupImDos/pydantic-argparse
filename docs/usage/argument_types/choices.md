## Overview
`pydantic-argparse` provides functionality for choice arguments. A choice is a
command-line argument that allows a restricted set of values. For example:
`--choice X` or `--choice Y`.

This covers the standard `argparse` functionality of:

* `:::python choices=["A", "B", "C"]`

## Usage
The intended usage of choice arguments is to restrict the set of valid options
for the user. For example:

```console
$ python3 example.py --choice A
```

```python
if args.choice == "A":
    # Choice A
    ...
elif args.choice == "B":
    # Choice B
    ...
elif args.choice == "C":
    # Choice C
    ...
else:
    # This cannot occur!
    # Something must have gone wrong...
    ...
```

## Enums
Enum choices can be created by defining a `pydantic` `Field` with a type of an
`:::python enum.Enum` class, which contains more than one enumeration. There
are different kinds of enum choice arguments, which are outlined below.

### Required
A *required* enum choice argument is defined as follows:

```python
class Choices(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()

class Arguments(BaseModel):
    # Required Choice
    choice: Choices = Field(description="this is a required choice")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] --choice {A, B, C}

required arguments:
  --choice {A, B, C}  this is a required choice

help:
  -h, --help          show this help message and exit
```

Outcomes:

* Providing an argument of `--choice A` will set `args.choice` to `Choices.A`.
* Providing an argument of `--choice B` will set `args.choice` to `Choices.B`.
* Providing an argument of `--choice C` will set `args.choice` to `Choices.C`.
* This argument cannot be omitted.

### Optional (Default `None`)
An *optional* enum choice argument with a default of `None` is defined as
follows:

```python
class Choices(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()

class Arguments(BaseModel):
    # Optional Choice (Default None)
    choice: Optional[Choices] = Field(description="this is an optional choice")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] [--choice {A, B, C}]

optional arguments:
  --choice {A, B, C}  this is an optional choice (default: None)

help:
  -h, --help          show this help message and exit
```

Outcomes:

* Providing an argument of `--choice A` will set `args.choice` to `Choices.A`.
* Providing an argument of `--choice B` will set `args.choice` to `Choices.B`.
* Providing an argument of `--choice C` will set `args.choice` to `Choices.C`.
* Omitting this argument will set `args.choice` to `None` (the default).

### Optional (Default `Value`)
An *optional* enum choice argument with a default choice is defined as follows:

```python
class Choices(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()

class Arguments(BaseModel):
    # Optional Choice (Default Choices.A)
    choice: Choices = Field(Choices.A, description="this is an optional choice")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] [--choice {A, B, C}]

optional arguments:
  --choice {A, B, C}  this is an optional choice (default: Choices.A)

help:
  -h, --help          show this help message and exit
```

Outcomes:

* Providing an argument of `--choice A` will set `args.choice` to `Choices.A`.
* Providing an argument of `--choice B` will set `args.choice` to `Choices.B`.
* Providing an argument of `--choice C` will set `args.choice` to `Choices.C`.
* Omitting this argument will set `args.choice` to `Choices.A` (the default).

## Literals
Literal choices can be created by defining a `pydantic` `Field` with a type of
`:::python typing.Literal`, which contains more than one literal value. There
are different kinds of literal flag arguments, which are outlined below.

### Required
A *required* literal choice argument is defined as follows:

```python
class Arguments(BaseModel):
    # Required Choice
    choice: Literal["A", "B", "C"] = Field(description="this is a required choice")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] --choice {A, B, C}

required arguments:
  --choice {A, B, C}  this is a required choice

help:
  -h, --help          show this help message and exit
```

Outcomes:

* Providing an argument of `--choice A` will set `args.choice` to `"A"`.
* Providing an argument of `--choice B` will set `args.choice` to `"B"`.
* Providing an argument of `--choice C` will set `args.choice` to `"C"`.
* This argument cannot be omitted.

### Optional (Default `None`)
An *optional* literal choice argument with a default of `None` is defined as
follows:

```python
class Arguments(BaseModel):
    # Optional Choice (Default None)
    choice: Optional[Literal["A", "B", "C"]] = Field(description="this is an optional choice")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] [--choice {A, B, C}]

optional arguments:
  --choice {A, B, C}  this is an optional choice (default: None)

help:
  -h, --help          show this help message and exit
```

Outcomes:

* Providing an argument of `--choice A` will set `args.choice` to `"A"`.
* Providing an argument of `--choice B` will set `args.choice` to `"B"`.
* Providing an argument of `--choice C` will set `args.choice` to `"C"`.
* Omitting this argument will set `args.choice` to `None` (the default).

### Optional (Default `Value`)
An *optional* literal choice argument with a default choice is defined as
follows:

```python
class Arguments(BaseModel):
    # Optional Choice (Default "A")
    choice: Literal["A", "B", "C"] = Field("A", description="this is an optional choice")
```

This `Arguments` model generates the following command-line interface:

```console
$ python3 example.py --help
usage: example.py [-h] [--choice {A, B, C}]

optional arguments:
  --choice {A, B, C}  this is an optional choice (default: A)

help:
  -h, --help          show this help message and exit
```

Outcomes:

* Providing an argument of `--choice A` will set `args.choice` to `"A"`.
* Providing an argument of `--choice B` will set `args.choice` to `"B"`.
* Providing an argument of `--choice C` will set `args.choice` to `"C"`.
* Omitting this argument will set `args.choice` to `"A"` (the default).
