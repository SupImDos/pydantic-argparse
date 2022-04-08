## Overview
At the core of `pydantic-argparse` is the `pydantic` *model*, in which
arguments are declared with `pydantic` *fields*. This combination of the
*model* and its *fields* defines the *schema* for your command-line arguments.

## Pydantic
### Models
A `pydantic` model is simply a *dataclass-like* class that inherits from the
`pydantic.BaseModel` base class. In `pydantic-argparse`, this model is used to
declaratively define your command-line arguments.

```python
class Arguments(BaseModel):
    # Required
    string: str
    integer: int
    number: float

    # Optional
    boolean: bool = False
```

Arbitrary data, such as raw command-line arguments, can be passed to a model.
After parsing and validation `pydantic` guarantees that the fields of the
resultant model instance will conform to the field types defined on the model.

!!! info
    For more information about `pydantic` models, see the `pydantic` [docs][1].

### Fields
A `pydantic` model contains *fields*, which are the model class attributes.
These fields define each `pydantic-argparse` command-line argument, and they
can be declared either *implicitly* (as above), or *explicitly* (as below).

```python
class Arguments(BaseModel):
    # Required
    string: str = Field(description="this argument is a string")
    integer: int = Field(description="this argument is an integer")
    number: float = Field(description="this argument is a number")

    # Optional
    boolean: bool = Field(False, description="this argument is a boolean")
```

Explicitly defining fields can provide extra information about an argument,
either for the command-line interface, the model schema or features such as
complex validation.

!!! info
    For more information about `pydantic` fields, see the `pydantic` [docs][2].

## Arguments
### Required
A field defines a required argument if it has no default value, or a default
value of the `Ellipses` (`...`) singleton object.

```python
class Arguments(BaseModel):
    a: int
    b: int = ...
    c: int = Field()
    d: int = Field(...)
```

### Optional
A field defines an optional argument if it has a default value.

```python
class Arguments(BaseModel):
    a: int = 42
    b: int = Field(42)
```

A field can also define an optional argument if it is type-hinted as
`Optional`. This type-hinting also allows the value of `None` for the field.

```python
class Arguments(BaseModel):
    a: Optional[int]
    b: Optional[int] = None
    c: Optional[int] = Field()
    d: Optional[int] = Field(None)
```

### Descriptions
A field can be provided with a `description`, which will appear in the
command-line interface help message.

```python
class Arguments(BaseModel):
    a: int = Field(description="this is the command-line description!")
```

### Aliases
A field can be provided with an `alias`, which will change the argument name in
the command-line interface.

```python
class Arguments(BaseModel):
    # We want our argument to be named `class` (i.e., `--class`), but `class`
    # is a reserved keyword in Python. To accomplish this, we can use the Field
    # `alias` to override the argument name.
    class_argument: int = Field(alias="class")
```

!!! tip
    This feature allows you to define arguments that use a reserved python
    keyword as the name. For example: `class`, `continue`, `async`.

    You can see the list of reserved keywords in Python at any time by typing
    `:::python help("keywords")` into the Python interpreter.

## Validation
When parsing command-line arguments with `parser.parse_typed_args()`, the raw
values are parsed and validated using `pydantic`. The parser has different
behaviours depending on whether the supplied command-line arguments are valid.

Consider the following example model:

```python
class Arguments(BaseModel):
    integer: int
```

### Success
When the provided command-line arguments satisfy the `pydantic` model, a
populated instance of the model is returned

```console
$ python3 example.py --integer 42
Arguments(integer=42)
```

### Failure
When the provided command-line arguments do not satisfy the `pydantic` model,
the `ArgumentParser` will provide an error to the user. For example:

```console
$ python3 example.py --integer hello
usage: example.py [-h] --integer INTEGER
example.py: error: 1 validation error for Arguments
integer
  value is not a valid integer (type=type_error.integer)
```

!!! note
    The validation error shown to the user is the same as the error that
    `pydantic` returns to the user with a `ValidationError`

<!--- Reference -->
[1]: https://pydantic-docs.helpmanual.io/usage/models/
[2]: https://pydantic-docs.helpmanual.io/usage/schema/#field-customization
