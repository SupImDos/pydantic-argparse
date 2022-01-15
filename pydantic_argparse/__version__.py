"""__version__.py

Exports the title, description, version, author and license of the package

@author Hayden Richards <SupImDos@gmail.com>
"""


# Standard
from importlib import metadata


# Retrieve Metadata from Package
__title__ = metadata.metadata(__package__)["name"]
__description__ = metadata.metadata(__package__)["summary"]
__version__ = metadata.metadata(__package__)["version"]
__author__ = metadata.metadata(__package__)["author"]
__license__ = metadata.metadata(__package__)["license"]
