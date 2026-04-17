"""Tests for shopping module."""
# pylint: disable=redefined-outer-name

import pytest
from unittest.mock import patch
from shopping import Cart, log_purchase, apply_coupon, COUPONS


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


@pytest.mark.parametrize("discount,expected", [(0, 100), (50, 50), (100, 0)])
def test_discount(cart, discount, expected):
    """Test discount application."""
    cart.add_item("X", 100)
    cart.apply_discount(discount)
    assert cart.total() == expected


@patch("shopping.requests.post")
def test_log_purchase(mock_post):
    """Test log purchase mocks HTTP call."""
    log_purchase({"name": "Apple"})
    mock_post.assert_called_once()


def test_apply_coupon(monkeypatch):
    """Test coupon application."""
    cart = Cart()
    monkeypatch.setitem(COUPONS, "TEST", 20)
    cart.add_item("X", 100)
    apply_coupon(cart, "TEST")
    assert cart.total() == 80
