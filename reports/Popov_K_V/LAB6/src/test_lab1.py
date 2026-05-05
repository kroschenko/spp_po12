"""
Тесты для модуля корзины покупок (shopping.py).
Лабораторная работа №6.
"""
import pytest
import requests
from shopping import Cart, log_purchase, apply_coupon

# pylint: disable=redefined-outer-name
# Это отключит предупреждение о том, что аргумент функции совпадает с именем фикстуры.

@pytest.fixture
def empty_cart():
    """Фикстура для создания пустого экземпляра корзины."""
    return Cart()

def test_add_item(empty_cart):
    """Проверка добавления товара в корзину."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0] == {"name": "Apple", "price": 10.0}

def test_negative_price(empty_cart):
    """Проверка выброса исключения при отрицательной цене товара."""
    with pytest.raises(ValueError):
        empty_cart.add_item("Banana", -5.0)

def test_total(empty_cart):
    """Проверка расчета общей суммы товаров в корзине."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    assert empty_cart.total() == 30.0

@pytest.mark.parametrize("discount, expected_price", [
    (0, 10.0),    # 0% - цена остаётся прежней
    (50, 5.0),    # 50% - цена уменьшается вдвое
    (100, 0.0)    # 100% - цена становится ноль
])
def test_apply_discount_valid(empty_cart, discount, expected_price):
    """Тестирование корректных значений скидки через параметризацию."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.items[0]["price"] == expected_price

@pytest.mark.parametrize("invalid_discount", [
    -10,  # < 0%
    110   # > 100%
])
def test_apply_discount_exceptions(empty_cart, invalid_discount):
    """Проверка выброса исключения при недопустимом проценте скидки."""
    empty_cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(invalid_discount)

def test_log_purchase(monkeypatch):
    """Тестирование логирования покупки с использованием моков."""

    # pylint: disable=too-few-public-methods
    class MockResponse:
        """Вспомогательный класс для имитации ответа сервера."""
        def __init__(self):
            self.called_url = None
            self.called_json = None

        def mock_post(self, url, json=None, timeout=None):
            """Имитация метода requests.post."""
            _ = timeout  # Используем переменную, чтобы не было ошибки unused argument
            self.called_url = url
            self.called_json = json

    mock_resp = MockResponse()
    monkeypatch.setattr(requests, "post", mock_resp.mock_post)

    test_item = {"name": "Apple", "price": 10.0}
    log_purchase(test_item)

    assert mock_resp.called_url == "https://example.com/log"
    assert mock_resp.called_json == test_item

def test_apply_coupon_valid(empty_cart, monkeypatch):
    """Проверка применения валидного купона с мокингом словаря купонов."""
    empty_cart.add_item("Apple", 100.0)
    monkeypatch.setattr("shopping.coupons", {"MOCK20": 20})
    apply_coupon(empty_cart, "MOCK20")
    assert empty_cart.items[0]["price"] == 80.0

def test_apply_coupon_invalid(empty_cart):
    """Проверка поведения системы при вводе несуществующего купона."""
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "WRONG_COUPON")
