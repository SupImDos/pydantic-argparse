"""Pydantic Utility Functions for Declarative Typed Argument Parsing.

The `pydantic` module contains utility functions used for interacting with the
internals of `pydantic`, such as updating `pydantic` validator dictionaries and
constructing new `pydantic` model types with dynamically generated validators.
"""


# Third-Party
import pydantic

# Typing
from typing import Any, Dict, Callable, Optional, Type, TypeVar


# Constants
PydanticModelT = TypeVar("PydanticModelT", bound=pydantic.BaseModel)
PydanticValidator = classmethod


def update_validators(
    validators: Dict[str, PydanticValidator],
    field: str,
    validator: Optional[Callable[..., Any]],
) -> None:
    """Updates a validators dictionary with a possible new validator.

    Note that this function mutates the validators dictionary *in-place*, and
    does not return the dictionary.

    Args:
        validators (Dict[str, PydanticValidator]): Validators to update.
        field (str): Name of the field that the validator function targets.
        validator (Optional[Callable[..., Any]]): Possible validator function.
    """
    # Check for Validator
    if validator:
        # Construct Pydantic Validator Decorator
        decorator = pydantic.validator(field, pre=True, allow_reuse=True)

        # Decorate and Add Validator
        validators[validator.__name__] = decorator(validator)


def model_with_validators(
    model: Type[PydanticModelT],
    validators: Dict[str, PydanticValidator],
) -> Type[PydanticModelT]:
    """Constructs a new `pydantic` model type with the supplied validators.

    Args:
        model (Type[PydanticModelT]): Model type to use as base class.
        validators (Dict[str, PydanticValidator]): Validators to add.

    Returns:
        Type[PydanticModelT]: New `pydantic` model type with validators.
    """
    # Construct New Type and Return
    return type(model.__name__, (model, ), validators)
