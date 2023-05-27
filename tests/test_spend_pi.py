#!/usr/bin/env python
"""Tests for `api` package."""
# pylint: disable=redefined-outer-name
from api import __version__


def test_version() -> None:
    """Sample pytest test function."""
    assert __version__ == "0.1.0"
