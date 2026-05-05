"""
Тесты для модуля lab1_2 (алгоритм Two Sum).
"""

from unittest.mock import patch
from reports.Mihnovec_S_E.Lab_1.src.Lab1_2 import twosum, settarget


def test_twosum_basic():
    """Проверка стандартного случая Two Sum."""
    assert twosum(9, [2, 7, 11, 15]) == [0, 1]


def test_twosum_no_result():
    """Проверка случая, когда пара чисел не найдена."""
    assert twosum(10, [1, 2, 3]) == []


def test_twosum_negative():
    """Проверка работы с отрицательными числами."""
    assert twosum(-5, [-1, -4, 2, 3]) == [0, 1]


def test_settarget_valid():
    """Проверка корректного ввода целевого числа."""
    with patch("builtins.input", return_value="50"):
        assert settarget() == 50


def test_settarget_invalid():
    """Проверка ввода текста вместо числа в settarget."""
    with patch("builtins.input", return_value="ошибка"):
        assert settarget() == 0
