"""
Тесты для модуля shopping.

Содержит тесты для класса Cart и функций log_purchase, apply_coupon.
"""

from unittest.mock import patch
import pytest
from shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def cart_fixture():
    """Фикстура: создаёт пустую корзину."""
    return Cart()


# ========== Задание 1.1: Базовые тесты ==========

def test_add_item(cart):
    """Проверка добавления товара."""
    cart.add_item("Apple", 10.0)
    assert len(cart) == 1
    assert cart.items[0] == ("Apple", 10.0)


def test_add_multiple_items(cart):
    """Проверка добавления нескольких товаров."""
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 15.5)
    assert len(cart) == 2
    assert cart.total() == 25.5


def test_negative_price(cart):
    """Проверка выброса ошибки при отрицательной цене."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        cart.add_item("Orange", -5.0)


def test_total(cart):
    """Проверка вычисления общей стоимости."""
    cart.add_item("A", 100)
    cart.add_item("B", 200)
    cart.add_item("C", 50.5)
    assert cart.total() == 350.5


def test_total_empty_cart(cart):
    """Проверка общей стоимости пустой корзины."""
    assert cart.total() == 0.0


# ========== Задание 1.2: Параметризованные тесты для скидок ==========

@pytest.mark.parametrize("discount, expected_total", [
    (0, 100),    # 0% - цена остаётся прежней
    (50, 50),    # 50% - цена уменьшается вдвое
    (100, 0),    # 100% - цена становится ноль
])
def test_apply_discount(cart, discount, expected_total):
    """Проверка применения скидки с разными значениями."""
    cart.add_item("Item", 100)
    cart.apply_discount(discount)
    assert cart.total() == expected_total


@pytest.mark.parametrize("bad_discount", [-10, -50, 110, 150, 200])
def test_discount_out_of_range(cart, bad_discount):
    """Проверка выброса исключения при невалидной скидке."""
    cart.add_item("Item", 100)
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        cart.apply_discount(bad_discount)


def test_discount_on_multiple_items(cart):
    """Проверка скидки на нескольких товарах."""
    cart.add_item("Item1", 100)
    cart.add_item("Item2", 200)
    cart.add_item("Item3", 300)
    cart.apply_discount(25)  # 25% скидка
    assert cart.total() == (100 + 200 + 300) * 0.75


# ========== Задание 1.4: Мокирование requests.post ==========

@patch("shopping.requests.post")
def test_log_purchase_called_once(mock_post):
    """Проверка, что requests.post вызывается ровно один раз."""
    item = {"name": "Apple", "price": 10.0}
    log_purchase(item)
    mock_post.assert_called_once()


@patch("shopping.requests.post")
def test_log_purchase_with_correct_data(mock_post):
    """Проверка, что requests.post вызывается с корректными данными."""
    item = {"name": "Laptop", "price": 999.99}
    log_purchase(item)
    mock_post.assert_called_once_with(
        "https://example.com/log",
        json=item,
        timeout=30
    )


@patch("shopping.requests.post")
def test_log_purchase_multiple_calls(mock_post):
    """Проверка множественных вызовов логирования."""
    items = [
        {"name": "Apple", "price": 10},
        {"name": "Banana", "price": 15},
        {"name": "Orange", "price": 12}
    ]
    for item in items:
        log_purchase(item)

    assert mock_post.call_count == 3
    for single_item in items:
        mock_post.assert_any_call(
            "https://example.com/log",
            json=single_item,
            timeout=30
        )


# ========== Задание 1.5: Тесты для apply_coupon ==========

def test_apply_coupon_save10(cart):
    """Проверка применения купона SAVE10 (10% скидка)."""
    cart.add_item("Test", 200)
    apply_coupon(cart, "SAVE10")
    assert cart.total() == 180  # 200 - 10% = 180


def test_apply_coupon_half(cart):
    """Проверка применения купона HALF (50% скидка)."""
    cart.add_item("Test", 200)
    apply_coupon(cart, "HALF")
    assert cart.total() == 100  # 200 - 50% = 100


def test_apply_coupon_invalid(cart):
    """Проверка выброса исключения при недействительном купоне."""
    cart.add_item("Test", 100)
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart, "INVALID")


def test_apply_coupon_case_sensitive(cart):
    """Проверка чувствительности к регистру."""
    cart.add_item("Test", 100)
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart, "save10")  # нижний регистр


# ========== Мокирование словаря coupons ==========

def test_apply_coupon_with_monkeypatch(cart, monkeypatch):
    """Подмена словаря coupons с помощью monkeypatch."""
    # Создаём фейковый словарь купонов
    fake_coupons = {"TEST15": 15, "SUPER20": 20}

    # Подменяем словарь в функции apply_coupon
    monkeypatch.setattr("shopping.apply_coupon.coupons", fake_coupons)

    cart.add_item("Item", 100)
    apply_coupon(cart, "TEST15")
    assert cart.total() == 85  # 100 - 15% = 85


def test_apply_coupon_with_patch_dict(cart):
    """Подмена словаря coupons с помощью patch.dict."""
    fake_coupons = {"MOCK50": 50}

    with patch.dict("shopping.apply_coupon.coupons", fake_coupons, clear=True):
        cart.add_item("Item", 200)
        apply_coupon(cart, "MOCK50")
        assert cart.total() == 100


# ========== Дополнительные тесты ==========

def test_add_item_zero_price(cart):
    """Добавление товара с нулевой ценой."""
    cart.add_item("Free Item", 0.0)
    assert len(cart) == 1
    assert cart.total() == 0.0


def test_apply_discount_zero_items(cart):
    """Применение скидки к пустой корзине."""
    cart.apply_discount(50)
    assert cart.total() == 0.0
    assert len(cart) == 0
