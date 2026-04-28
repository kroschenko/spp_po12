"""
Модуль для работы со строками.
"""

from typing import Optional


def common(str1: Optional[str], str2: Optional[str]) -> str:
    """
    Находит наибольшую общую подстроку двух строк.
    Спецификация требует обработки None и пустых строк.
    """
    if str1 is None or str2 is None:
        raise TypeError("Аргументы не могут быть None")

    if not str1 or not str2:
        return ""

    longest = ""
    for i in range(len(str1)):
        for j in range(i + 1, len(str1) + 1):
            substring = str1[i:j]
            if substring in str2 and len(substring) > len(longest):
                longest = substring

    return longest
