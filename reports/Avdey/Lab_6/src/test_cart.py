from unittest.mock import patch

import pytest

import shopping
from task_3 import repeat
from shopping import Cart, apply_coupon, log_purchase
from lab_1 import all_elements_equal, find_two_sum

# Задание 1


# 3. Фикстура для пустой корзины
@pytest.fixture(name="empty_cart")
def fixture_empty_cart():
    return Cart()


# 1. Добавление товара
def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"
    assert empty_cart.items[0]["price"] == 10.0


#  Тест отрицательной цены
def test_add_item_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Banana", -5)


#  Тест подсчета общей стоимости
def test_total(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 5.0)
    assert empty_cart.total() == 15.0


# 2. Тест apply_discount с параметризацией
@pytest.mark.parametrize(
    "discount, expected",
    [
        (0, 20.0),
        (50, 10.0),
        (100, 0.0),
    ],
)
def test_apply_discount(empty_cart, discount, expected):
    empty_cart.add_item("Apple", 20.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == expected


@pytest.mark.parametrize("discount", [-10, 150])
def test_apply_discount_invalid(empty_cart, discount):
    empty_cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)


def test_log_purchase():
    with patch("shopping.requests.post") as mock_post:
        item = {"name": "Apple", "price": 10.0}
        log_purchase(item)
        mock_post.assert_called_once_with("https://example.com/log", json=item)


# 5. Тест apply_coupon


def test_apply_coupon_save10(empty_cart):
    empty_cart.add_item("Apple", 100.0)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 90.0


def test_apply_coupon_half(empty_cart):
    empty_cart.add_item("Apple", 100.0)
    apply_coupon(empty_cart, "HALF")
    assert empty_cart.total() == 50.0


def test_apply_coupon_invalid(empty_cart):
    empty_cart.add_item("Apple", 100.0)
    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "INVALID")


def test_apply_coupon_monkeypatch(empty_cart, monkeypatch):
    empty_cart.add_item("Apple", 100.0)
    fake_coupons = {"FAKE50": 50}

    monkeypatch.setattr(shopping, "coupons", fake_coupons)

    apply_coupon(empty_cart, "FAKE50")
    assert empty_cart.total() == 50.0


# Задание 2


@pytest.mark.parametrize(
    "data, expected",
    [
        ([], False),  # пустой список
        ([1], True),  # один элемент
        ([1, 1, 1], True),  # все одинаковые
        ([1, 2, 1], False),  # разные элементы
        (["a", "a", "a"], True),  # строки одинаковые
        (["a", "b"], False),  # строки разные
    ],
)
def test_all_elements_equal(data, expected):
    assert all_elements_equal(data) == expected


def test_find_two_sum_simple():
    arr = [2, 7, 11, 15]
    target = 9
    assert find_two_sum(arr, target) == [0, 1]


def test_find_two_sum_multiple_pairs():
    arr = [1, 2, 3, 4, 5]
    target = 6
    assert find_two_sum(arr, target) == [0, 4]


def test_find_two_sum_no_solution():
    arr = [1, 2, 3]
    target = 10
    assert find_two_sum(arr, target) is None


def test_find_two_sum_negative_numbers():
    arr = [-1, -2, 3, 4]
    target = 2
    assert find_two_sum(arr, target) == [0, 2]


def test_find_two_sum_empty():
    assert find_two_sum([], 5) is None


def test_find_two_sum_single_element():
    assert find_two_sum([5], 5) is None


# Задание 3


def test_repeat_zero():
    assert repeat("e", 0) == ""


def test_repeat_positive():
    assert repeat("e", 3) == "eee"
    assert repeat("ABC", 2) == "ABCABC"


def test_repeat_negative():
    with pytest.raises(ValueError):
        repeat("e", -2)


def test_repeat_none_pattern():
    with pytest.raises(TypeError):
        repeat(None, 1)


def test_repeat_empty_pattern():
    assert repeat("", 5) == ""
