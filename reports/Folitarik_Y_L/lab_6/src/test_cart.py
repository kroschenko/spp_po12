"""
Tests for the shopping module.
"""

from unittest.mock import patch
import pytest
import shopping
from shopping import Cart, log_purchase, apply_coupon

# pylint: disable=redefined-outer-name, import-error


@pytest.fixture
def empty_cart():
    """Create a fresh Cart instance."""
    return Cart()


def test_add_item(empty_cart):
    """Test item addition logic."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


def test_negative_price(empty_cart):
    """Test error for negative prices."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        empty_cart.add_item("Banana", -5.0)


def test_total(empty_cart):
    """Test calculation of total price."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Orange", 20.0)
    assert empty_cart.total() == 30.0


@pytest.mark.parametrize(
    "discount, expected_total",
    [
        (0, 100.0),
        (50, 50.0),
        (100, 0.0),
    ],
)
def test_apply_discount_valid(empty_cart, discount, expected_total):
    """Test valid discount applications."""
    empty_cart.add_item("Gadget", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total


@pytest.mark.parametrize("invalid_discount", [-10, 110])
def test_apply_discount_invalid(empty_cart, invalid_discount):
    """Test invalid discount values."""
    empty_cart.add_item("Gadget", 100.0)
    with pytest.raises(ValueError, match="Invalid discount percentage"):
        empty_cart.apply_discount(invalid_discount)


@patch("shopping.requests.post")
def test_log_purchase_mock(mock_post):
    """Test remote logging using mock."""
    test_item = {"name": "Apple", "price": 10.0}
    log_purchase(test_item)
    mock_post.assert_called_once_with(
        "https://example.com/log", json=test_item, timeout=5
    )


def test_apply_coupon_success(empty_cart, monkeypatch):
    """Test coupon application with monkeypatch."""
    monkeypatch.setitem(shopping.COUPONS, "TEST_COUPON", 20)
    empty_cart.add_item("Item", 100.0)
    apply_coupon(empty_cart, "TEST_COUPON")
    assert empty_cart.total() == 80.0


def test_apply_coupon_invalid(empty_cart):
    """Test error for non-existent coupons."""
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "NON_EXISTENT")
