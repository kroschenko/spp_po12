"""Тесты для функции repeat."""

import pytest

from task_3_string_utils import repeat


def test_repeat_zero_times() -> None:
    """Повторение 0 раз возвращает пустую строку."""
    assert repeat("e", "|", 0) == ""


def test_repeat_three_times_with_separator() -> None:
    """Повторение с разделителем."""
    assert repeat("e", "|", 3) == "e|e|e"


def test_repeat_with_spaces_and_comma() -> None:
    """Повторение строки с пробелами и запятой."""
    assert repeat(" ABC ", ",", 2) == "ABC , ABC "


def test_repeat_with_empty_separator() -> None:
    """Пустой разделитель склеивает элементы."""
    assert repeat(" DBE ", "", 2) == " DBEDBE "


def test_repeat_one_time_returns_trimmed() -> None:
    """Одно повторение возвращает строку без внешних пробелов."""
    assert repeat(" DBE ", ":", 1) == "DBE"


def test_repeat_negative_count_raises_error() -> None:
    """Отрицательное количество повторов запрещено."""
    with pytest.raises(ValueError):
        repeat("e", "|", -2)


def test_repeat_empty_text() -> None:
    """Пустой текст формирует только разделители."""
    assert repeat("", ":", 3) == "::"


def test_repeat_none_text_raises_type_error() -> None:
    """None вместо текста должен вызывать TypeError."""
    with pytest.raises(TypeError):
        repeat(None, "a", 1)  # type: ignore[arg-type]


def test_repeat_none_separator_raises_type_error() -> None:
    """None вместо разделителя должен вызывать TypeError."""
    with pytest.raises(TypeError):
        repeat("a", None, 2)  # type: ignore[arg-type]
