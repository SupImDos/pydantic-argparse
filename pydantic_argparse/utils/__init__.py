"""Utility Functions for Declarative Typed Argument Parsing.

This package contains helper functions for the typed argument parsing process,
including formatting argument names and descriptions, recursively parsing
`argparse.Namespace` objects to `dict`s, constructing named partial type
casting functions and checking the types of `pydantic` fields.

The public interface exposed by this package is various utility helper methods.
"""

# Local
from .utils import (
    argument_name,
    argument_description,
    namespace_to_dict,
    type_caster,
    is_field_a,
)
