#!/usr/bin/env python3
"""cli.py

Provides command line functionality to the application.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Local
from .parser import ArgumentParser, PydanticModel


def cli(
    app: str,
    description: str,
    version: str,
    model: type[PydanticModel],
    ) -> ArgumentParser[PydanticModel]:
    """Generates command line argument parser for application.

    Args:
        app (str): Application name for CLI.
        description (str): Application description for CLI.
        version (str): Application version for CLI.
        model (type[PydanticModel]): Pydantic model for arguments.

    Returns:
        ArgumentParser: Generated custom typed argument parser.
    """
    # Create Argparser
    parser = ArgumentParser(
        prog=app,
        description=description,
        version=version,
        model=model,
    )

    # Return Argparser
    return parser
