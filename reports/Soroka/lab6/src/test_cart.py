# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods
"""
Модуль для тестирования мини-библиотеки покупок (shopping.py).
Включает тесты добавления товаров, применения скидок, купонов и логгирования.
"""

import pytest
import requests
import shopping
from shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def empty_cart():
    """Фикстура для создания пустой корзины перед каждым тестом."""
    return Cart()


def test_add_item(empty_cart):
    """Проверка успешного добавления товара в корзину."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"
    assert empty_cart.items[0]["price"] == 10.0


def test_negative_price(empty_cart):
    """Проверка выброса исключения при добавлении товара с отрицательной ценой."""
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        empty_cart.add_item("Banana", -5.0)


def test_total(empty_cart):
    """Проверка корректного вычисления общей стоимости товаров в корзине."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Milk", 15.0)
    assert empty_cart.total() == 25.0


@pytest.mark.parametrize("discount, expected_total",[
    (0, 100.0),
    (50, 50.0),
    (100, 0.0)
])
def test_apply_discount_valid(empty_cart, discount, expected_total):
    """Проверка корректного применения валидных скидок (0, 50, 100 процентов)."""
    empty_cart.add_item("Jacket", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total


@pytest.mark.parametrize("invalid_discount", [-10, 150])
def test_apply_discount_invalid(empty_cart, invalid_discount):
    """Проверка выброса исключения при недопустимых значениях скидки."""
    empty_cart.add_item("Jacket", 100.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(invalid_discount)


def test_log_purchase(monkeypatch):
    """Тестирование функции логгирования покупок с использованием мокирования."""
    mock_data = {}

    def mock_post(url, json, timeout=10):
        """Заглушка для имитации POST-запроса."""
        mock_data["url"] = url
        mock_data["json"] = json
        mock_data["timeout"] = timeout

        class MockResponse:
            """Фейковый ответ сервера."""
            status_code = 200

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)

    item = {"name": "Laptop", "price": 1000.0}
    log_purchase(item)

    assert mock_data["url"] == "https://example.com/log"
    assert mock_data["json"] == item
    assert mock_data["timeout"] == 10


def test_apply_coupon_valid(empty_cart, monkeypatch):
    """Проверка применения валидного купона с подменой словаря купонов."""
    monkeypatch.setattr(shopping, "coupons", {"TEST20": 20})

    empty_cart.add_item("Shoes", 100.0)
    apply_coupon(empty_cart, "TEST20")

    assert empty_cart.total() == 80.0


def test_apply_coupon_invalid(empty_cart):
    """Проверка выброса исключения при использовании несуществующего купона."""
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "WRONG_CODE")
