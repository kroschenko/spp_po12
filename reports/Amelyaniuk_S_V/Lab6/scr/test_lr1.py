"""Модуль с тестами для функции check_age."""
import pytest
from logic_lr1 import check_age


def test_adult():
    """Тестирует проверку совершеннолетнего возраста."""
    assert check_age(20) is True


def test_child():
    """Тестирует проверку детского возраста."""
    assert check_age(10) is False


def test_age_zero():
    """Тестирует проверку возраста 0."""
    assert check_age(0) is False


def test_age_type_error():
    """Тестирует TypeError при неверном типе."""
    with pytest.raises(TypeError):
        check_age("20")


def test_age_value_error():
    """Тестирует ValueError при отрицательном возрасте."""
    with pytest.raises(ValueError):
        check_age(-1)
