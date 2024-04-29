"""Compatibiltity Shims for Declarative Typed Argument Parsing.

This package contains compatibility shims for the `pydantic` and `argparse`
modules, so that we can properly maintain version compatibility in one place.

The public interface exposed by this package is the module shims themselves.
"""

from pydantic_argparse.compatibility.argparse import argparse as argparse
from pydantic_argparse.compatibility.pydantic import pydantic as pydantic
