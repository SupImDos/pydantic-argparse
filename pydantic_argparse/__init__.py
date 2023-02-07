"""Declarative Typed Argument Parsing with Pydantic Models.

This is the `pydantic-argparse` package, which contains the classes, methods
and functions required for declarative and typed argument parsing with
`pydantic` models.

The public interface exposed by this package is the declarative and typed
`ArgumentParser` class, as well as the package "dunder" metadata.
"""

# Local
from pydantic_argparse.argparse import ArgumentParser
from pydantic_argparse.__metadata__ import __title__
from pydantic_argparse.__metadata__ import __description__
from pydantic_argparse.__metadata__ import __version__
from pydantic_argparse.__metadata__ import __author__
from pydantic_argparse.__metadata__ import __license__


# Public Re-Exports
__all__ = (
    "ArgumentParser",
    "__title__",
    "__description__",
    "__version__",
    "__author__",
    "__license__",
)
