"""Тесты для функций, выделенных из ЛР1."""

import pytest

from task_2_lab1_functions import increment_digits, median


def test_median_for_odd_count() -> None:
    """Нечётное количество элементов."""
    assert median([3, 1, 2]) == 2.0


def test_median_for_even_count() -> None:
    """Чётное количество элементов."""
    assert median([1, 2, 3, 4]) == 2.5


def test_median_for_single_element() -> None:
    """Тривиальный случай для одного элемента."""
    assert median([7]) == 7.0


def test_median_for_empty_list_raises_error() -> None:
    """Пустой список должен вызывать исключение."""
    with pytest.raises(ValueError):
        median([])


def test_increment_digits_regular_case() -> None:
    """Обычное увеличение без переноса на весь массив."""
    assert increment_digits([1, 2, 3]) == [1, 2, 4]


def test_increment_digits_with_carry() -> None:
    """Увеличение с переносом разряда."""
    assert increment_digits([1, 2, 9]) == [1, 3, 0]


def test_increment_digits_all_nines() -> None:
    """Граничный случай, когда все цифры равны девяти."""
    assert increment_digits([9, 9, 9]) == [1, 0, 0, 0]


def test_increment_digits_empty_list_raises_error() -> None:
    """Пустой список не является корректным числом."""
    with pytest.raises(ValueError):
        increment_digits([])


def test_increment_digits_invalid_digit_raises_error() -> None:
    """Значения вне диапазона 0..9 запрещены."""
    with pytest.raises(ValueError):
        increment_digits([1, 10, 2])
