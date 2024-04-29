"""Declarative Typed Argument Parsing with Pydantic Models.

This is the `pydantic-argparse` package, which contains the classes, methods
and functions required for declarative and typed argument parsing with
`pydantic` models.

The public interface exposed by this package is the declarative and typed
`ArgumentParser` class, as well as the package "dunder" metadata.
"""

from pydantic_argparse.__metadata__ import __version__ as __version__
from pydantic_argparse.__metadata__ import __version_tuple__ as __version_tuple__
from pydantic_argparse.__metadata__ import version as version
from pydantic_argparse.__metadata__ import version_tuple as version_tuple
from pydantic_argparse.argparse import ArgumentParser as ArgumentParser
