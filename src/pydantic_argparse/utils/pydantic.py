"""Pydantic Utility Functions for Declarative Typed Argument Parsing.

The `pydantic` module contains utility functions used for interacting with the
internals of `pydantic`, such as constructing field validators, updating
field validator dictionaries and constructing new model classes with
dynamically generated validators and environment variable parsers.
"""


# Standard
import contextlib

# Third-Party
import pydantic

# Typing
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union


# Constants
T = TypeVar("T")
PydanticModelT = TypeVar("PydanticModelT", bound=pydantic.BaseModel)
PydanticValidator = classmethod


def as_validator(
    field: pydantic.fields.ModelField,
    caster: Callable[[str], Any],
) -> PydanticValidator:
    """Shortcut to wrap a caster and construct a validator for a given field.

    The provided caster function must cast from a string to the type required
    by the field. Once wrapped, the constructed validator will pass through any
    non-string values, or any values that cause the caster function to raise an
    exception to let the built-in `pydantic` field validation handle them. The
    validator will also cast empty strings to `None`.

    Args:
        field (pydantic.fields.ModelField): Field to construct validator for.
        caster (Callable[[str], Any]): String to field type caster function.

    Returns:
        PydanticValidator: Constructed field validator function.
    """
    # Dynamically construct a `pydantic` validator function for the supplied
    # field. The constructed validator must be `pre=True` so that the validator
    # is called before the built-in `pydantic` field validation occurs and is
    # provided with the raw input data. The constructed validator must also be
    # `allow_reuse=True` so the `__validator` function name can be reused
    # multiple times when being decorated as a `pydantic` validator. Note that
    # despite the `__validator` function *name* being reused, each instance of
    # the validator function is uniquely constructed for the supplied field.
    @pydantic.validator(field.name, pre=True, allow_reuse=True)
    def __validator(cls: Type[Any], value: T) -> Union[T, None, Any]:
        if not isinstance(value, str):
            return value
        if not value:
            return None
        try:
            return caster(value)
        except Exception:
            return value

    # Rename the validator uniquely for this field to avoid any collisions. The
    # leading `__` and prefix of `pydantic_argparse` should guard against any
    # potential collisions with user defined validators.
    __validator.__name__ = f"__pydantic_argparse_{field.name}"

    # Return the constructed validator
    return __validator


def update_validators(
    validators: Dict[str, PydanticValidator],
    validator: Optional[PydanticValidator],
) -> None:
    """Updates a validators dictionary with a possible new field validator.

    Note that this function mutates the validators dictionary *in-place*, and
    does not return the dictionary.

    Args:
        validators (Dict[str, PydanticValidator]): Validators to update.
        validator (Optional[PydanticValidator]): Possible field validator.
    """
    # Check for Validator
    if validator:
        # Add Validator
        validators[validator.__name__] = validator


def model_with_validators(
    model: Type[PydanticModelT],
    validators: Dict[str, PydanticValidator],
) -> Type[PydanticModelT]:
    """Generates a new `pydantic` model class with the supplied validators.

    If the supplied base model is a subclass of `pydantic.BaseSettings`, then 
    the newly generated model will also have a new `parse_env_var` classmethod
    monkeypatched onto it that suppresses any exceptions raised when initially
    parsing the environment variables. This allows the raw values to still be
    passed through to the `pydantic` field validators if initial parsing fails.

    Args:
        model (Type[PydanticModelT]): Model type to use as base class.
        validators (Dict[str, PydanticValidator]): Field validators to add.

    Returns:
        Type[PydanticModelT]: New `pydantic` model type with field validators.
    """
    # Construct New Model with Validators
    model = pydantic.create_model(
        model.__name__,
        __base__=model,
        __validators__=validators,
    )

    # Check if the model is a `BaseSettings`
    if issubclass(model, pydantic.BaseSettings):
        # Hold a reference to the current `parse_env_var` classmethod
        parse_env_var = model.__config__.parse_env_var

        # Construct a new `parse_env_var` function which suppresses exceptions
        # raised by the current `parse_env_var` classmethod. This allows the
        # raw values to be passed through to the `pydantic` field validator
        # methods if they cannot be parsed initially.
        def __parse_env_var(field_name: str, raw_val: str) -> Any:
            with contextlib.suppress(Exception):
                return parse_env_var(field_name, raw_val)
            return raw_val

        # Monkeypatch `parse_env_var`
        model.__config__.parse_env_var = __parse_env_var  # type: ignore[assignment]

    # Return Constructed Model
    return model
