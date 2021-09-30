#!/usr/bin/env python3
"""conftest.py

Configure Testing and Define Pytest Fixtures

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Standard
import pathlib

# Third-Party
import pytest
import toml

# Typing
from typing import Any  # pylint: disable=wrong-import-order


# Constants
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_TOML = PROJECT_ROOT.joinpath("pyproject.toml")


@pytest.fixture
def pyproject() -> dict[str, Any]:
    """Loads the project pyproject.toml.

    Returns:
        dict[str, Any]: pyproject.toml parsed as a dictionary.
    """
    # Load Project TOML
    return dict(toml.load(PROJECT_TOML))
