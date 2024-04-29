"""Compatibility Shim for Pydantic.

In order to support both Pydantic v1 and Pydantic v2, we need to make sure we
import the module correctly:

* For `pydantic~=2.0` there is a working `v1` module.
* For `pydantic==1.10.15` there is a broken `v1` module (with no `fields`).
* For `pydantic<1.10.14` there is no `v1` module.
"""


# Pydantic Shim
# There is a bit of fiddling around here to accomodate for the cases outlined
# above, as well as to keep the type-checker and language-server happy.
try:  # pragma: no cover
    from pydantic import v1 as pydantic
    pydantic.fields  # noqa: B018
    # Test
    import pydantic  # type: ignore[no-redef]
    assert pydantic.__version__.startswith("2")
    from pydantic import v1 as pydantic
except (ImportError, AttributeError):  # pragma: no cover
    import pydantic  # type: ignore[no-redef]
    # Test
    assert pydantic.__version__.startswith("1")
