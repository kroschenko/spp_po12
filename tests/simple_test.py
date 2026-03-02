import pytest

from reports.Mihnovec_S_E.Lab_1.src.Lab1 import isequal
from reports.Mihnovec_S_E.Lab_1.src.Lab1_2 import twosum

# --- Тесты для Lab1.py (Функция isequal) ---

def test_isequal_all_same():
    """Тест: все элементы одинаковые"""
    assert isequal([1, 1, 1]) == "равны"

def test_isequal_different():
    """Тест: элементы разные"""
    assert isequal([1, 2, 1]) == "неравны"

def test_isequal_too_short():
    """Тест: меньше двух элементов"""
    assert isequal([1]) == "меньше двух."

def test_isequal_empty():
    """Тест: пустой список"""
    assert isequal([]) == "меньше двух."


# --- Тесты для Lab1_2.py (Функция twosum) ---

def test_twosum_success():
    """Тест: стандартный случай (сумма найдена)"""
    assert twosum(9, [2, 7, 11, 15]) == [0, 1]

def test_twosum_another_success():
    """Тест: другая комбинация"""
    assert twosum(6, [3, 2, 4]) == [1, 2]

def test_twosum_no_result():
    """Тест: когда подходящих чисел нет"""
    assert twosum(10, [1, 2, 3]) == []

def test_twosum_same_numbers():
    """Тест: два одинаковых числа дают цель"""
    assert twosum(6, [3, 3]) == [0, 1]