"""Модуль с тестами для корзины покупок."""
# pylint: disable=redefined-outer-name
from unittest.mock import patch
import pytest
from shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def cart_fixture():
    """Создает пустую корзину для тестов."""
    return Cart()


def test_add_item(cart_fixture):
    """Тестирует добавление товара в корзину."""
    cart_fixture.add_item("Apple", 10.0)
    assert len(cart_fixture.items) == 1


def test_negative_price(cart_fixture):
    """Тестирует ошибку при отрицательной цене."""
    with pytest.raises(ValueError):
        cart_fixture.add_item("Apple", -5.0)


def test_total(cart_fixture):
    """Тестирует подсчет общей стоимости."""
    cart_fixture.add_item("Apple", 10.0)
    cart_fixture.add_item("Orange", 20.0)
    assert cart_fixture.total() == 30.0


@pytest.mark.parametrize(
    "discount, expected_total", [(0, 100.0), (50, 50.0), (100, 0.0)]
)
def test_apply_discount(cart_fixture, discount, expected_total):
    """Тестирует применение скидки."""
    cart_fixture.add_item("PC", 100.0)
    cart_fixture.apply_discount(discount)
    assert cart_fixture.total() == expected_total


def test_invalid_discount(cart_fixture):
    """Тестирует ошибку при невалидной скидке."""
    with pytest.raises(ValueError):
        cart_fixture.apply_discount(-1)
    with pytest.raises(ValueError):
        cart_fixture.apply_discount(101)


def test_log_purchase():
    """Тестирует логирование покупки."""
    with patch("requests.post") as mocked_post:
        item = {"name": "Apple", "price": 10.0}
        log_purchase(item)
        mocked_post.assert_called_once_with(
            "https://example.com/log", json=item, timeout=30
        )


def test_apply_coupon(cart_fixture):
    """Тестирует применение купона к корзине."""
    cart_fixture.add_item("PC", 100.0)
    apply_coupon(cart_fixture, "SAVE10")
    assert cart_fixture.total() == 90.0

    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart_fixture, "FAKE")
