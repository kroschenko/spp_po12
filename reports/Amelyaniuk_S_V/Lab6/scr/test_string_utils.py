"""Модуль с тестами для функции index_of_difference."""
import pytest
from string_utils import index_of_difference


def test_index_of_difference():
    """Тестирует функцию index_of_difference."""
    # Согласно спецификации варианта 5:
    with pytest.raises(TypeError):
        index_of_difference(None, None)

    assert index_of_difference("", "") == -1
    assert index_of_difference("", "abc") == 0
    assert index_of_difference("abc", "") == 0
    assert index_of_difference("abc", "abc") == -1
    assert index_of_difference("ab", "abxyz") == 2
    assert index_of_difference("abcde", "abxyz") == 2
    assert index_of_difference("abcde", "xyz") == 0
