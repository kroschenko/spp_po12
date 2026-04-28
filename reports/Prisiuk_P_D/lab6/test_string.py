"""Тесты для утилит обработки строк."""

import pytest
from string_utils import keep


def test_keep_none_none():
    """Проверка случая, когда оба аргумента None."""
    with pytest.raises(TypeError):
        keep(None, None)


def test_keep_none_string():
    """Проверка, если исходная строка None."""
    assert keep(None, "abc") is None


@pytest.mark.parametrize("pattern", ["abc", "", None])
def test_keep_empty_string(pattern):
    """Проверка, если исходная строка пустая."""
    assert keep("", pattern) == ""


def test_keep_string_none():
    """Проверка, если паттерн равен None."""
    assert keep("hello", None) == ""


def test_keep_string_empty():
    """Проверка, если паттерн пустой."""
    assert keep("hello", "") == ""


@pytest.mark.parametrize(
    "text, pattern, expected",
    [
        (" hello ", "hl", " hll "),
        (" hello ", "le", " ell "),
    ],
)
def test_keep_normal(text, pattern, expected):
    """Проверка стандартной логики с сохранением пробелов."""
    assert keep(text, pattern) == expected
