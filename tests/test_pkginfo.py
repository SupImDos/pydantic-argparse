#!/usr/bin/env python3
"""test_pkginfo.py

Tests __pkginfo__ Module.

@author Hayden Richards <SupImDos@gmail.com>
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Local
from pydantic_argparse import __app__, __description__, __version__, __authors__

# Typing
from typing import Any  # pylint: disable=wrong-import-order


def test_correct_app_name(pyproject: dict[str, Any]) -> None:
    """Tests __app__ in __pkginfo__ matches pyproject.toml.

    Args:
        pyproject (dict[str, Any]): pyproject.toml loaded as dictionary as per
            pytest fixture.
    """
    # Assert App Name is Correct
    assert (
        __app__ == pyproject["tool"]["poetry"]["name"]
    ), "Project app name should match in package and package config"


def test_correct_description(pyproject: dict[str, Any]) -> None:
    """Tests __description__ in __pkginfo__ matches pyproject.toml.

    Args:
        pyproject (dict[str, Any]): pyproject.toml loaded as dictionary as per
            pytest fixture.
    """
    # Assert Description is Correct
    assert (
        __description__ == pyproject["tool"]["poetry"]["description"]
    ), "Project description should match in package and package config"


def test_correct_version(pyproject: dict[str, Any]) -> None:
    """Tests __version__ in __pkginfo__ matches pyproject.toml.

    Args:
        pyproject (dict[str, Any]): pyproject.toml loaded as dictionary as per
            pytest fixture.
    """
    # Assert Version is Correct
    assert (
        __version__ == pyproject["tool"]["poetry"]["version"]
    ), "Project version should match in package and package config"


def test_correct_authors(pyproject: dict[str, Any]) -> None:
    """Tests __authors__ in __pkginfo__ matches pyproject.toml.

    Args:
        pyproject (dict[str, Any]): pyproject.toml loaded as dictionary as per
            pytest fixture.
    """
    # Assert Authors is Correct
    assert (
        __authors__ == pyproject["tool"]["poetry"]["authors"]
    ), "Project authors should match in package and package config"
