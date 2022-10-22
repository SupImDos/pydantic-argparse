"""Single-Source of Truth Package Versioning and Metadata

The `pydantic-argparse` package uses the `pyproject.toml` file as a
single-source of truth for the package metadata. As such, rather than
duplicating the metadata in code here, it is retrieved from the installed
package metadata at runtime.

The metadata exported are the `title`, `description`, `version`, `author` and
`license` of the package
"""


# Standard
from importlib import metadata


# Retrieve Metadata from Package
__title__: str = metadata.metadata(__package__)["name"]
__description__: str = metadata.metadata(__package__)["summary"]
__version__: str = metadata.metadata(__package__)["version"]
__author__: str = metadata.metadata(__package__)["author"]
__license__: str = metadata.metadata(__package__)["license"]
