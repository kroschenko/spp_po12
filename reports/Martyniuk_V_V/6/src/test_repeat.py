"""Tests for string repeat module."""

import pytest
from string_repeat import repeat


def test_repeat_zero():
    """Test repeat 0 times."""
    assert repeat("e", 0) == ""


def test_repeat_three():
    """Test repeat 3 times."""
    assert repeat("e", 3) == "eee"


def test_repeat_pattern():
    """Test repeat pattern."""
    assert repeat("ABC", 2) == "ABCABC"


def test_repeat_negative():
    """Test negative count raises error."""
    with pytest.raises(ValueError):
        repeat("e", -2)


def test_repeat_none():
    """Test None pattern raises error."""
    with pytest.raises(TypeError):
        repeat(None, 1)
