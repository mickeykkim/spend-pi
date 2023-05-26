#!/usr/bin/env python
"""Tests for `spend_pi` package."""
# pylint: disable=redefined-outer-name
from spend_pi import __version__


def test_version() -> None:
    """Sample pytest test function."""
    assert __version__ == "0.1.0"
