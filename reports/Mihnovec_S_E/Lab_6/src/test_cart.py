"""Тесты для модуля shopping."""
from unittest.mock import patch
import pytest
import shopping
from shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def empty_cart():
    """Фикстура пустой корзины."""
    return Cart()


def test_add_item(empty_cart):  # pylint: disable=redefined-outer-name
    """Тест добавления товара."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


@pytest.mark.parametrize(
    "discount, expected", [(0, 100), (50, 50), (100, 0)]
)
def test_discount(empty_cart, discount, expected):  # pylint: disable=redefined-outer-name
    """Тест скидок."""
    empty_cart.add_item("Item", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected


@patch("requests.post")
def test_log_purchase(mock_post):
    """Тест мока запроса."""
    log_purchase({"item": "test"})
    mock_post.assert_called_once()


def test_apply_coupon_with_monkeypatch(empty_cart, monkeypatch):  # pylint: disable=redefined-outer-name
    """Тест купонов с использованием monkeypatch."""
    empty_cart.add_item("Item", 100.0)
    monkeypatch.setitem(shopping.COUPONS, "TEST", 25)
    apply_coupon(empty_cart, "TEST")
    assert empty_cart.total() == 75.0


def test_apply_coupon_invalid(empty_cart):  # pylint: disable=redefined-outer-name
    """Тест невалидного купона."""
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "NON_EXISTENT")
