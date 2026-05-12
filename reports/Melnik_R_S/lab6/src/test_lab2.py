"""
lab2_tests
"""

import pytest
from lab2 import BoundedIntSet


def test_create_bounded_set():
    """Тривиальный случай: создание множества и проверка базовых атрибутов."""
    s = BoundedIntSet(capacity=5, initial_elements=[1, 2, 3])
    assert s.capacity == 5
    assert s.elements == [1, 2, 3]


def test_negative_capacity():
    """Исключительная ситуация: отрицательная мощность."""
    with pytest.raises(ValueError):
        BoundedIntSet(capacity=-1)


def test_add_duplicate_element():
    """Граничный случай: добавление дубликата игнорируется."""
    s = BoundedIntSet(capacity=3, initial_elements=[1])
    s.add(1)
    assert len(s.elements) == 1


def test_add_overflow():
    """Исключительная ситуация: превышение мощности (OverflowError)."""
    s = BoundedIntSet(capacity=2, initial_elements=[1, 2])
    with pytest.raises(OverflowError):
        s.add(3)


def test_remove_missing_element():
    """Исключительная ситуация: удаление несуществующего элемента."""
    s = BoundedIntSet(capacity=5, initial_elements=[1, 2])
    with pytest.raises(ValueError):
        s.remove(99)


def test_set_union():
    """Тривиальный случай: объединение множеств."""
    set1 = BoundedIntSet(capacity=2, initial_elements=[1, 2])
    set2 = BoundedIntSet(capacity=2, initial_elements=[2, 3])

    union_set = set1.union(set2)
    assert union_set.capacity == 4
    assert sorted(union_set.elements) == [1, 2, 3]
