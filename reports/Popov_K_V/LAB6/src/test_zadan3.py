"""
Тесты для функции repeat (Задание 3, Вариант 1).
"""
import pytest
from zadanie3 import repeat

def test_repeat_zero():
    """Спецификация: repeat("e", 0) = ''"""
    assert repeat("e", 0) == ""

def test_repeat_positive():
    """Спецификация: repeat("e", 3) = 'eee'"""
    assert repeat("e", 3) == "eee"

def test_repeat_multiple_chars():
    """Спецификация: repeat("ABC", 2) = 'ABCABC'"""
    assert repeat("ABC", 2) == "ABCABC"

def test_repeat_negative_times():
    """Спецификация: repeat("e", -2) = ValueError"""
    with pytest.raises(ValueError):
        repeat("e", -2)

def test_repeat_none_pattern():
    """Спецификация: repeat(None, 1) = TypeError"""
    with pytest.raises(TypeError):
        repeat(None, 1)
