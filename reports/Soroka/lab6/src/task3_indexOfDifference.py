# pylint: disable=invalid-name
"""
Модуль содержит реализацию функции indexOfDifference и тесты к ней.
Задание 3, вариант 5.
"""

import pytest


def indexOfDifference(str1: str, str2: str) -> int:
    """
    Возвращает индекс первой позиции, в которой строки различаются.
    Если строки идентичны, возвращает -1.
    Если передан None, выбрасывает TypeError.
    """
    if str1 is None or str2 is None:
        raise TypeError("Строки не могут быть None")

    if str1 == str2:
        return -1

    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return i

    return min_len


@pytest.mark.parametrize("str1, str2, expected_index",[
    ("", "", -1),
    ("", "abc", 0),
    ("abc", "", 0),
    ("abc", "abc", -1),
    ("ab", "abxyz", 2),
    ("abcde", "abxyz", 2),
    ("abcde", "xyz", 0),
    ("i am a machine", "i am a robot", 7)
])
def test_index_of_difference_logic(str1, str2, expected_index):
    """Проверка функции indexOfDifference на корректных и граничных значениях."""
    assert indexOfDifference(str1, str2) == expected_index


def test_index_of_difference_type_error():
    """Проверка выброса TypeError при передаче None в качестве аргумента."""
    with pytest.raises(TypeError):
        indexOfDifference(None, None)

    with pytest.raises(TypeError):
        indexOfDifference("abc", None)
