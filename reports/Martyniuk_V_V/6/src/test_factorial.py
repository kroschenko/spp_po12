"""Tests for factorial module."""
# pylint: disable=redefined-outer-name

import pytest
from factorial import factorial


@pytest.mark.parametrize("n,expected", [(0, 1), (1, 1), (2, 2), (3, 6), (5, 120)])
def test_factorial(n, expected):
    """Test factorial calculation."""
    assert factorial(n) == expected


def test_factorial_negative():
    """Test negative input raises error."""
    with pytest.raises(ValueError):
        factorial(-1)


def test_factorial_type():
    """Test wrong type raises error."""
    with pytest.raises(TypeError):
        factorial("a")
