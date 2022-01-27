"""Declarative Typed Argument Parsing with Pydantic Models

This is the `pydantic-argparse` package, which contains the classes, methods
and functions required for declarative and typed argument parsing with
`pydantic` models.

The public interface exposed by this package is the declarative and typed
`ArgumentParser` class, as well as the package "dunder" metadata.
"""

# Local
from .__version__ import __title__, __description__, __version__, __author__, __license__
from .argparse import ArgumentParser
