<div align="center">
<!-- Logo -->
<a href="https://pydantic-argparse.supimdos.com"><img src="assets/images/logo.svg" width="50%"></a>
<!-- Headings -->
<h1 style="margin-bottom:0;font-size:3em;">Pydantic Argparse</h1>
<p style="margin-top:0;"><em>Typed Argument Parsing with Pydantic</em></p>
<!-- Badges (Row 1) -->
<a href="https://pypi.python.org/pypi/pydantic-argparse"><img src="https://img.shields.io/pypi/v/pydantic-argparse"></a>
<a href="https://pepy.tech/project/pydantic-argparse"><img src="https://img.shields.io/pepy/dt/pydantic-argparse?color=blue"></a>
<a href="https://github.com/SupImDos/pydantic-argparse"><img src="https://img.shields.io/pypi/pyversions/pydantic-argparse"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/blob/master/LICENSE"><img src="https://img.shields.io/github/license/SupImDos/pydantic-argparse"></a>
<br>
<!-- Badges (Row 2) -->
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/test.yml?label=tests"></a>
<a href="https://app.codecov.io/github/SupImDos/pydantic-argparse"><img src="https://img.shields.io/codecov/c/github/SupImDos/pydantic-argparse"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/lint.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/lint.yml?label=linting"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/format.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/format.yml?label=formatting"></a>
<a href="https://github.com/SupImDos/pydantic-argparse/actions/workflows/type.yml"><img src="https://img.shields.io/github/actions/workflow/status/supimdos/pydantic-argparse/type.yml?label=typing"></a>
</div>
---

## Overview
`pydantic-argparse` is a Python package built on top of [`pydantic`][1] which
provides declarative *typed* argument parsing using `pydantic` models.

## Requirements
`pydantic-argparse` requires Python 3.8+, and is compatible with the Pydantic
v1 API.

## Installation
Installation with `pip` is simple:
```console
$ pip install pydantic-argparse
```

## Quick Start
--8<-- "docs/examples/simple.md"

## Credits
This project is made possible by [`pydantic`][1].

## License
This project is licensed under the terms of the MIT license.

<!--- Reference -->
[1]: https://docs.pydantic.dev/
