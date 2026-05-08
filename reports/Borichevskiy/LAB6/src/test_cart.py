"""
Тесты для shopping.py
"""

from __future__ import annotations
import pytest
from unittest.mock import patch

from shopping import Cart, apply_coupon, log_purchase


@pytest.fixture
def empty_cart() -> Cart:
    return Cart()


def test_add_item(empty_cart: Cart) -> None:
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items["Apple"] == 10.0


def test_add_item_negative_price(empty_cart: Cart) -> None:
    with pytest.raises(ValueError):
        empty_cart.add_item("Bad", -5)


def test_total(empty_cart: Cart) -> None:
    empty_cart.add_item("A", 10)
    empty_cart.add_item("B", 5)
    assert empty_cart.total() == 15


@pytest.mark.parametrize(
    "discount, price, expected",
    [
        (0, 100, 100),
        (50, 100, 50),
        (100, 100, 0),
    ],
)
def test_apply_discount_valid(discount: float, price: float, expected: float) -> None:
    cart = Cart()
    cart.add_item("X", price)
    cart.apply_discount(discount)
    assert cart.items["X"] == expected


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(discount: float) -> None:
    cart = Cart()
    cart.add_item("X", 100)
    with pytest.raises(ValueError):
        cart.apply_discount(discount)


def test_log_purchase_mocked() -> None:
    with patch("shopping.requests.post") as mock_post:
        log_purchase({"item": "Apple"})
        mock_post.assert_called_once_with(
            "https://example.com/log",
            json={"item": "Apple"},
        )


def test_apply_coupon_valid(empty_cart: Cart) -> None:
    empty_cart.add_item("X", 100)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.items["X"] == 90


def test_apply_coupon_invalid(empty_cart: Cart) -> None:
    empty_cart.add_item("X", 100)
    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "UNKNOWN")
