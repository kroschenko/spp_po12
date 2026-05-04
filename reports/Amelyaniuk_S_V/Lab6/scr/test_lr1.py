import pytest
from logic_lr1 import check_age


def test_adult():
    assert check_age(20) is True


def test_child():
    assert check_age(10) is False


def test_age_zero():
    assert check_age(0) is False


def test_age_type_error():
    with pytest.raises(TypeError):
        check_age("20")


def test_age_value_error():
    with pytest.raises(ValueError):
        check_age(-1)
