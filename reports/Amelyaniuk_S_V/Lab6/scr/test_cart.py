import pytest
from unittest.mock import patch
from shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def empty_cart():
    return Cart()


def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1


def test_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -5.0)


def test_total(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Orange", 20.0)
    assert empty_cart.total() == 30.0


@pytest.mark.parametrize(
    "discount, expected_total", [(0, 100.0), (50, 50.0), (100, 0.0)]
)
def test_apply_discount(empty_cart, discount, expected_total):
    empty_cart.add_item("PC", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total


def test_invalid_discount(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.apply_discount(-1)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(101)


def test_log_purchase():
    with patch("requests.post") as mocked_post:
        item = {"name": "Apple", "price": 10.0}
        log_purchase(item)
        mocked_post.assert_called_once_with("https://example.com/log", json=item)


def test_apply_coupon(empty_cart, monkeypatch):
    empty_cart.add_item("PC", 100.0)
    # Тестируем валидный купон
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 90.0

    # Тестируем ошибку при невалидном купоне
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "FAKE")
