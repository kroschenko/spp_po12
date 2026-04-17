"""Tests for repeat module."""
# pylint: disable=redefined-outer-name

import pytest
from string_repeat import repeat


@pytest.mark.parametrize("pattern,n,expected", [
    ("e", 0, ""),
    ("e", 3, "eee"),
    ("ABC", 2, "ABCABC"),
])
def test_repeat(pattern, n, expected):
    """Test string repeat."""
    assert repeat(pattern, n) == expected


def test_repeat_negative():
    """Test negative count raises error."""
    with pytest.raises(ValueError):
        repeat("e", -2)


def test_repeat_none():
    """Test None pattern raises error."""
    with pytest.raises(TypeError):
        repeat(None, 1)
