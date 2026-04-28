"""
Тесты для модуля lab1 (работа со списками).
"""

from unittest.mock import patch
import pytest
from reports.Mihnovec_S_E.Lab_1.src.Lab1 import isequal, add_item, remove_item


def test_isequal_less_than_two():
    """Проверка случая, когда в списке меньше двух элементов."""
    assert isequal([1]) == "меньше двух."
    assert isequal([]) == "меньше двух."


def test_isequal_equal():
    """Проверка случая, когда все элементы равны."""
    assert isequal([5, 5, 5]) == "равны"


def test_isequal_not_equal():
    """Проверка случая, когда элементы разные."""
    assert isequal([1, 2, 1]) == "неравны"


def test_add_item_success():
    """Проверка успешного добавления элемента через mock ввода."""
    items = [1, 2]
    with patch("builtins.input", return_value="10"):
        add_item(items)
    assert items == [1, 2, 10]


def test_add_item_value_error():
    """Проверка ввода некорректных данных (строка вместо числа) в add_item."""
    items = [1, 2]
    with patch("builtins.input", return_value="abc"):
        add_item(items)
    assert items == [1, 2]


def test_remove_item_success():
    """Проверка успешного удаления по индексу (пользователь вводит 1-based индекс)."""
    items = [10, 20, 30]
    with patch("builtins.input", return_value="2"):
        remove_item(items)
    assert items == [10, 30]


def test_remove_item_out_of_range():
    """Проверка удаления по несуществующему индексу."""
    items = [10, 20]
    with patch("builtins.input", return_value="99"):
        remove_item(items)
    assert items == [10, 20]


if __name__ == "__main__":
    pytest.main([__file__])
