"""Tests for cart module."""

from unittest.mock import patch
import pytest
from shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def empty_cart():
    return Cart()


def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10)
    assert len(empty_cart.items) == 1


def test_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Bad", -5)


def test_total(empty_cart):
    empty_cart.add_item("A", 100)
    empty_cart.add_item("B", 200)
    assert empty_cart.total() == 300


@pytest.mark.parametrize("d,exp", [(0, 100), (50, 50), (100, 0)])
def test_discount(empty_cart, d, exp):
    empty_cart.add_item("X", 100)
    empty_cart.apply_discount(d)
    assert empty_cart.total() == exp


@patch("shopping.requests.post")
def test_log(mock_post):
    log_purchase({"name": "Apple"})
    mock_post.assert_called_once()


def test_coupon(empty_cart):
    empty_cart.add_item("X", 100)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 90