"""
Тесты для модуля string_repeat.

Содержит тесты для функций повторения строк.
"""

import pytest
from string_repeat import repeat_string


# ========== Параметризованные тесты ==========

@pytest.mark.parametrize("pattern,repeat_count,expected", [
    # Тривиальные случаи
    ("", 5, ""),
    ("e", 0, ""),
    ("e", 1, "e"),
    # Обычные случаи
    ("e", 3, "eee"),
    ("ABC", 2, "ABCABC"),
    ("123", 3, "123123123"),
    # С пробелами и спецсимволами
    (" ABC ", 2, " ABC  ABC "),
    ("\n", 3, "\n\n\n"),
    # Unicode
    ("Привет", 2, "ПриветПривет"),
    ("😀", 3, "😀😀😀"),
])
def test_repeat_valid_cases(pattern, repeat_count, expected):
    """Проверка корректных случаев повторения."""
    assert repeat_string(pattern, repeat_count) == expected


@pytest.mark.parametrize("pattern,repeat_count", [
    ("e", -1),
    ("test", -5),
    ("abc", -100),
])
def test_repeat_negative_count(pattern, repeat_count):
    """Отрицательное количество повторений -> ValueError."""
    with pytest.raises(ValueError, match="repeat count cannot be negative"):
        repeat_string(pattern, repeat_count)


@pytest.mark.parametrize("pattern", [None, 123, 3.14, [], {}, set()])
def test_repeat_invalid_pattern(pattern):
    """Неверный тип pattern -> TypeError."""
    with pytest.raises(TypeError):
        repeat_string(pattern, 1)  # type: ignore


def test_repeat_large_number():
    """Повторение большое количество раз."""
    result = repeat_string("a", 10000)
    assert len(result) == 10000
    assert result == "a" * 10000


def test_repeat_long_pattern():
    """Повторение длинного паттерна."""
    long_pattern = "abcdefghij" * 100  # 1000 символов
    result = repeat_string(long_pattern, 10)
    assert len(result) == 10000
    assert result[:1000] == long_pattern


def test_repeat_identity_property():
    """Свойство: repeat(x, 1) == x."""
    test_strings = ["a", "abc", "Hello", " ", "\n", "123"]
    for s in test_strings:
        assert repeat_string(s, 1) == s


def test_repeat_concatenation_property():
    """Свойство: repeat(x, a+b) == repeat(x, a) + repeat(x, b)."""
    pattern = "abc"
    a, b = 3, 4
    assert repeat_string(pattern, a + b) == \
           repeat_string(pattern, a) + repeat_string(pattern, b)


def test_repeat_length_property():
    """Свойство: len(repeat(s, n)) == len(s) * n."""
    test_cases = [
        ("a", 5),
        ("ab", 10),
        ("Hello", 7),
        ("", 100),
    ]
    for pattern, n in test_cases:
        assert len(repeat_string(pattern, n)) == len(pattern) * n
