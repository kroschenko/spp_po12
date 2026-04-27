"""Tests for factorial module."""

import pytest
from factorial import factorial


def test_factorial_zero():
    """Test factorial of 0."""
    assert factorial(0) == 1


def test_factorial_one():
    """Test factorial of 1."""
    assert factorial(1) == 1


def test_factorial_five():
    """Test factorial of 5."""
    assert factorial(5) == 120


def test_factorial_negative():
    """Test negative input raises error."""
    with pytest.raises(ValueError):
        factorial(-1)


def test_factorial_type():
    """Test wrong type raises error."""
    with pytest.raises(TypeError):
        factorial("a")
