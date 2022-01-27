"""Utility Functions for Declarative Typed Argument Parsing.

This package contains helper functions for the typed argument parsing process,
including formatting argument names and descriptions, recursively parsing
`argparse.Namespace` objects to `dict`s and constructing named partial type
casting functions.

The public interface exposed by this package is various utility helper methods.
"""

# Local
from .utils import argument_name, argument_description, namespace_to_dict, type_caster
