import pytest
import requests
from unittest.mock import patch

# ========== КЛАСС CART ==========
class Cart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item: str, price: float):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append((item, price))
    
    def total(self) -> float:
        return sum(price for _, price in self.items)
    
    def apply_discount(self, discount_percent: float):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Скидка должна быть от 0 до 100 процентов")
        multiplier = 1 - (discount_percent / 100)
        self.items = [(item, price * multiplier) for item, price in self.items]
    
    def apply_coupon(self, coupon_code: str):
        coupons = {"SAVE10": 10, "HALF": 50}
        if coupon_code in coupons:
            self.apply_discount(coupons[coupon_code])
        else:
            raise ValueError("Invalid coupon")


def log_purchase(item):
    requests.post("https://example.com/log", json=item)


# ========== ФУНКЦИЯ STRING REPEAT ==========
def string_repeat(pattern: str, repeat: int) -> str:
    if pattern is None:
        raise TypeError("pattern не может быть None")
    if repeat < 0:
        raise ValueError("repeat не может быть отрицательным")
    return pattern * repeat


# ========== ТЕСТЫ ==========
@pytest.fixture
def empty_cart():
    return Cart()


def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0] == ("Apple", 10.0)


def test_add_item_negative_price(empty_cart):
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        empty_cart.add_item("Orange", -5.0)


def test_total(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    assert empty_cart.total() == 30.0


@pytest.mark.parametrize("discount, expected_total", [
    (0, 30.0),
    (50, 15.0),
    (100, 0.0),
])
def test_apply_discount_valid(empty_cart, discount, expected_total):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected_total


@pytest.mark.parametrize("discount", [-10, 150, 200])
def test_apply_discount_invalid(empty_cart, discount):
    empty_cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError, match="Скидка должна быть от 0 до 100 процентов"):
        empty_cart.apply_discount(discount)


def test_apply_coupon_valid(empty_cart):
    empty_cart.add_item("Apple", 100.0)
    empty_cart.apply_coupon("SAVE10")
    assert empty_cart.total() == 90.0


def test_apply_coupon_invalid(empty_cart):
    empty_cart.add_item("Apple", 100.0)
    with pytest.raises(ValueError, match="Invalid coupon"):
        empty_cart.apply_coupon("INVALID")


def test_log_purchase_mock():
    with patch("requests.post") as mock_post:
        log_purchase({"item": "Apple", "price": 10.0})
        mock_post.assert_called_once_with(
            "https://example.com/log",
            json={"item": "Apple", "price": 10.0}
        )


def test_string_repeat_zero():
    assert string_repeat("e", 0) == ""


def test_string_repeat_positive():
    assert string_repeat("e", 3) == "eee"


def test_string_repeat_with_spaces():
    assert string_repeat(" ABC ", 2) == " ABC  ABC "


def test_string_repeat_negative():
    with pytest.raises(ValueError, match="repeat не может быть отрицательным"):
        string_repeat("e", -2)


def test_string_repeat_none():
    with pytest.raises(TypeError, match="pattern не может быть None"):
        string_repeat(None, 1)


@pytest.mark.parametrize("pattern, repeat, expected", [
    ("a", 5, "aaaaa"),
    ("abc", 3, "abcabcabc"),
    ("", 10, ""),
    ("x", 1, "x"),
])
def test_string_repeat_parametrized(pattern, repeat, expected):
    assert string_repeat(pattern, repeat) == expected


if __name__ == "__main__":
    pytest.main(["-v"])
    