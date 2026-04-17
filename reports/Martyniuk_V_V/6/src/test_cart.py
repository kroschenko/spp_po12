# pylint: disable=redefined-outer-name
"""Tests for shopping module."""

import pytest
from shopping import Cart, apply_coupon


@pytest.fixture
def empty_cart():
    """Return empty cart."""
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


def test_discount(empty_cart):
    empty_cart.add_item("X", 100)
    empty_cart.apply_discount(50)
    assert empty_cart.total() == 50


def test_coupon(empty_cart):
    empty_cart.add_item("X", 100)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 90
