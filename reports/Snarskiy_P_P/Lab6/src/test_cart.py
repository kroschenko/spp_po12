"""
Тесты для мини-библиотеки покупок (shopping.py).
Запуск: pytest test_cart.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
from shopping import Cart, log_purchase, apply_coupon

# ──────────────────────────────────────────────
# Задание 1.1 — добавление товара
# ──────────────────────────────────────────────


def test_add_item_increases_count(empty_cart):
    """После add_item в корзине должен быть ровно один элемент."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


def test_add_item_stores_correct_data(empty_cart):
    """Убеждаемся, что имя и цена сохранены правильно."""
    empty_cart.add_item("Apple", 10.0)
    assert empty_cart.items[0]["name"] == "Apple"
    assert empty_cart.items[0]["price"] == 10.0


# ──────────────────────────────────────────────
# Задание 1.2 — отрицательная цена
# ──────────────────────────────────────────────


def test_add_item_negative_price_raises(empty_cart):
    """Отрицательная цена должна вызывать ValueError."""
    with pytest.raises(ValueError):
        empty_cart.add_item("Bad Item", -5.0)


# ──────────────────────────────────────────────
# Задание 1.3 — общая стоимость
# ──────────────────────────────────────────────


def test_total_empty_cart(empty_cart):
    """Сумма пустой корзины равна нулю."""
    assert empty_cart.total() == 0.0


def test_total_single_item(empty_cart):
    """Сумма корзины с одним товаром равна его цене."""
    empty_cart.add_item("Apple", 10.0)
    assert empty_cart.total() == 10.0


def test_total_multiple_items(empty_cart):
    """Сумма нескольких товаров считается верно."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.5)
    empty_cart.add_item("Cherry", 3.0)
    assert empty_cart.total() == pytest.approx(18.5)


# ──────────────────────────────────────────────
# Задание 2 — apply_discount с @parametrize
# ──────────────────────────────────────────────


@pytest.mark.parametrize(
    "discount, expected_price",
    [
        (0, 10.0),  # 0 % — цена не меняется
        (50, 5.0),  # 50 % — цена вдвое меньше
        (100, 0.0),  # 100 % — цена обнуляется
    ],
)
def test_apply_discount_valid(empty_cart, discount, expected_price):
    """Корректные скидки изменяют цену ожидаемым образом."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.items[0]["price"] == pytest.approx(expected_price)


@pytest.mark.parametrize("bad_discount", [-1, -0.01, 101, 200])
def test_apply_discount_invalid_raises(empty_cart, bad_discount):
    """Скидка < 0 % или > 100 % должна вызывать ValueError."""
    empty_cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(bad_discount)


# ──────────────────────────────────────────────
# Задание 3: фикстура пустой корзины
# ──────────────────────────────────────────────


@pytest.fixture
def empty_cart():
    """Возвращает свежий экземпляр Cart перед каждым тестом."""
    return Cart()


# ──────────────────────────────────────────────
# Задание 4 — мок requests.post в log_purchase
# ──────────────────────────────────────────────


def test_log_purchase_calls_post():
    """log_purchase должен вызывать requests.post с корректными данными."""
    item = {"name": "Apple", "price": 10.0}

    with patch("shopping.requests.post") as mock_post:
        log_purchase(item)

        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        assert args[0] == "https://example.com/log"
        assert kwargs["json"] == item


def test_log_purchase_no_real_http():
    """Реальный HTTP-запрос НЕ должен уходить (мок перехватывает его)."""
    with patch("shopping.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        log_purchase({"name": "Test", "price": 1.0})

        assert mock_post.called


def test_apply_coupon_save10(empty_cart):
    """Купон SAVE10 даёт 10 % скидки."""
    empty_cart.add_item("Apple", 10.0)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.items[0]["price"] == pytest.approx(9.0)


def test_apply_coupon_half(empty_cart):
    """Купон HALF даёт 50 % скидки."""
    empty_cart.add_item("Apple", 10.0)
    apply_coupon(empty_cart, "HALF")
    assert empty_cart.items[0]["price"] == pytest.approx(5.0)


def test_apply_coupon_invalid_raises(empty_cart):
    """Несуществующий купон должен вызывать ValueError."""
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "UNKNOWN")


def test_apply_coupon_with_patch_dict(empty_cart):
    """
    Мокаем модульный словарь COUPONS через patch.dict.
    Добавляем новый купон TESTCODE (20 %) и убеждаемся, что он работает,
    а оригинальный словарь не изменился после выхода из контекста.
    """
    import shopping

    empty_cart.add_item("Apple", 10.0)

    with patch.dict(shopping.COUPONS, {"TESTCODE": 20}, clear=False):

        apply_coupon(empty_cart, "TESTCODE")  # 20 % от 10.0 → 8.0
        assert empty_cart.items[0]["price"] == pytest.approx(8.0)

        assert "SAVE10" in shopping.COUPONS
        assert "HALF" in shopping.COUPONS

    assert "TESTCODE" not in shopping.COUPONS


def test_apply_coupon_monkeypatch(empty_cart, monkeypatch):
    """
    Используем monkeypatch для подмены всей функции apply_coupon —
    убеждаемся, что тест изолирован от реального словаря купонов.
    """
    empty_cart.add_item("Apple", 10.0)
    custom_coupons = {"VIP": 30}  # только наш купон

    def fake_apply_coupon(cart, coupon_code):
        if coupon_code in custom_coupons:
            cart.apply_discount(custom_coupons[coupon_code])
        else:
            raise ValueError("Invalid coupon")

    import shopping

    monkeypatch.setattr(shopping, "apply_coupon", fake_apply_coupon)

    shopping.apply_coupon(empty_cart, "VIP")
    assert empty_cart.items[0]["price"] == pytest.approx(7.0)

    with pytest.raises(ValueError):
        shopping.apply_coupon(empty_cart, "SAVE10")
