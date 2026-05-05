"""Тесты для лабораторной работы №1."""

import pytest
from lab1 import task_1_shuffle_numbers, task_2_majority_element


def test_shuffle_trivial():
    """Тест на обычные значения n."""
    n = 5
    result = task_1_shuffle_numbers(n)
    assert len(result) == n
    assert sorted(result) == [1, 2, 3, 4, 5]


def test_shuffle_boundary():
    """Тест на граничные значения n."""
    assert task_1_shuffle_numbers(1) == [1]
    # Используем логическую проверку вместо == [] для соответствия Pylint
    assert not task_1_shuffle_numbers(0)


def test_shuffle_exceptions():
    """Тест на обработку исключений при неверном вводе."""
    with pytest.raises(ValueError):
        task_1_shuffle_numbers(-10)
    with pytest.raises(TypeError):
        task_1_shuffle_numbers("5")


@pytest.mark.parametrize(
    "nums, expected",
    [([3, 2, 3], 3), ([1, 2, 1, 1, 1, 2, 2], 1), ([2, 2, 1, 1, 1, 2, 2], 2)],
)
def test_majority_trivial(nums, expected):
    """Тест поиска мажоритарного элемента на обычных списках."""
    assert task_2_majority_element(nums) == expected


def test_majority_boundary():
    """Тест на граничные значения списков."""
    assert task_2_majority_element([5]) == 5
    assert task_2_majority_element([7, 7, 7, 7]) == 7


def test_majority_exceptions():
    """Тест на исключение при пустом списке."""
    with pytest.raises(ValueError, match="Список не может быть пустым"):
        task_2_majority_element([])
