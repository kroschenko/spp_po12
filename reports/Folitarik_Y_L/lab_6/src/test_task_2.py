"""
Тесты для функции common.
"""

import pytest
from task_2 import common


def test_common_type_error():
    """Проверка выброса TypeError при передаче None."""
    with pytest.raises(TypeError):
        common(None, None)


@pytest.mark.parametrize(
    "s1, s2, expected",
    [
        ("", "", ""),
        ("", "abc", ""),
        ("abc", "", ""),
        ("abc", "abc", "abc"),
        ("ab", "abxyz", "ab"),
        ("abcde", "abxyz", "ab"),
        ("abcde", "xyz", ""),
        ("deabc", "abcdeabcd", "deabc"),
        ("dfabcegt", "rtoefabceiq", "fabce"),
    ],
)
def test_common_logic(s1, s2, expected):
    """Тестирование логики поиска подстроки на примерах из спецификации."""
    assert common(s1, s2) == expected


def test_common_case_sensitivity():
    """Проверка чувствительности к регистру."""
    assert common("ABC", "abc") == ""


def test_common_multiple_options():
    """Если есть несколько подстрок одинаковой длины, возвращается одна из них."""
    # В "abac" и "abdc" общие "ab" (длина 2) и "c" (длина 1)
    assert common("abac", "abdc") == "ab"
