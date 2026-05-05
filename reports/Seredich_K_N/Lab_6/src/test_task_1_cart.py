"""Тесты для мини-библиотеки покупок."""

# pylint: disable=redefined-outer-name

from unittest.mock import patch

import pytest

from task_1_shopping import Cart, apply_coupon, log_purchase


@pytest.fixture
def empty_cart() -> Cart:
    """Возвращает пустую корзину для тестов."""
    return Cart()


def test_add_item_adds_single_item(empty_cart: Cart) -> None:
    """После добавления товара в корзине один элемент."""
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


def test_add_item_negative_price_raises_error(empty_cart: Cart) -> None:
    """Отрицательная цена должна вызывать исключение."""
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -1.0)


def test_total_calculates_sum(empty_cart: Cart) -> None:
    """Метод total возвращает корректную сумму товаров."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.5)
    assert empty_cart.total() == pytest.approx(15.5)


@pytest.mark.parametrize(
    ("discount", "expected_total"),
    [(0, 100.0), (50, 50.0), (100, 0.0)],
)
def test_apply_discount_valid_values(
    empty_cart: Cart, discount: float, expected_total: float
) -> None:
    """Скидка в допустимом диапазоне применяется корректно."""
    empty_cart.add_item("Apple", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == pytest.approx(expected_total)


@pytest.mark.parametrize("discount", [-1, 101])
def test_apply_discount_invalid_values_raise_error(
    empty_cart: Cart, discount: float
) -> None:
    """Скидка вне диапазона [0, 100] должна вызывать исключение."""
    empty_cart.add_item("Apple", 100.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)


def test_log_purchase_calls_requests_post() -> None:
    """Логирование покупки вызывает requests.post с корректными данными."""
    item = {"name": "Apple", "price": 10.0}

    with patch("task_1_shopping.requests.post") as mocked_post:
        log_purchase(item)

    mocked_post.assert_called_once_with("https://example.com/log", json=item, timeout=5)


def test_apply_coupon_save10_uses_mocked_coupon_dict(empty_cart: Cart) -> None:
    """Купон SAVE10 применяет скидку из подменённого словаря."""
    empty_cart.add_item("Apple", 100.0)
    with patch.dict("task_1_shopping.COUPONS", {"SAVE10": 30, "HALF": 50}, clear=True):
        apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == pytest.approx(70.0)


def test_apply_coupon_invalid_code_raises_error(empty_cart: Cart) -> None:
    """Неизвестный купон должен вызывать исключение."""
    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "NOPE")
