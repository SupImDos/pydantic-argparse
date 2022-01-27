"""Parses Pydantic Fields to Command-Line Arguments.

This package contains the methods required for parsing `pydantic` model fields
to `ArgumentParser` command-line arguments.

The public interface exposed by this package is the `parsing` functions, which
take an `argparse.ArgumentParser` and a `pydantic.fields.ModelField`, parse the
field and add a new argument to the `ArgumentParser`.
"""

# Local
from .boolean import parse_boolean_field
from .command import parse_command_field
from .container import parse_container_field
from .enum import parse_enum_field
from .json import parse_json_field
from .literal import parse_literal_field
from .standard import parse_standard_field
