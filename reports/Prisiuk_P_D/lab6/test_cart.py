"""Тесты для модуля корзины покупок."""

from unittest.mock import patch
import pytest
import shopping
from shopping import Cart, log_purchase, apply_coupon

# pylint: disable=redefined-outer-name


@pytest.fixture
def empty_cart():
    """Фикстура для создания пустой корзины."""
    return Cart()


def test_add_item(empty_cart):
    """Тест добавления товара."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"


def test_add_item_negative_price(empty_cart):
    """Тест добавления товара с отрицательной ценой."""
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -5.0)


def test_total(empty_cart):
    """Тест расчета общей стоимости."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
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
    """Тест применения корректных скидок."""
    empty_cart.add_item("Item", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total


@pytest.mark.parametrize("invalid_discount", [-10, 150])
def test_apply_discount_invalid(empty_cart, invalid_discount):
    """Тест применения некорректных скидок."""
    empty_cart.add_item("Item", 100.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(invalid_discount)


@patch("shopping.requests.post")
def test_log_purchase(mock_post):
    """Тест логирования покупки с использованием мока."""
    item = {"name": "Apple", "price": 10.0}
    log_purchase(item)
    mock_post.assert_called_once_with("https://example.com/log", json=item, timeout=5)


def test_apply_coupon_valid(empty_cart, monkeypatch):
    """Тест применения существующего купона."""
    monkeypatch.setitem(shopping.COUPONS, "TEST20", 20)
    empty_cart.add_item("Item", 100.0)
    apply_coupon(empty_cart, "TEST20")
    assert empty_cart.total() == 80.0


def test_apply_coupon_invalid(empty_cart):
    """Тест применения несуществующего купона."""
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "FAKE_COUPON")
