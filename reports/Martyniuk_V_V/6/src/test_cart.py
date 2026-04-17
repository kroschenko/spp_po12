"""Tests for shopping cart module."""

import pytest
from shopping import Cart, apply_coupon


@pytest.fixture
def cart():
    """Return empty cart."""
    return Cart()


def test_add_item(cart):
    """Test adding item."""
    cart.add_item("Apple", 10)
    assert len(cart.items) == 1


def test_negative_price(cart):
    """Test negative price raises error."""
    with pytest.raises(ValueError):
        cart.add_item("Bad", -5)


def test_total(cart):
    """Test total calculation."""
    cart.add_item("A", 100)
    cart.add_item("B", 200)
    assert cart.total() == 300


def test_apply_discount(cart):
    """Test discount application."""
    cart.add_item("X", 100)
    cart.apply_discount(50)
    assert cart.total() == 50


def test_discount_invalid(cart):
    """Test invalid discount raises error."""
    cart.add_item("X", 100)
    with pytest.raises(ValueError):
        cart.apply_discount(150)


def test_apply_coupon(cart):
    """Test coupon application."""
    cart.add_item("X", 100)
    apply_coupon(cart, "SAVE10")
    assert cart.total() == 90
