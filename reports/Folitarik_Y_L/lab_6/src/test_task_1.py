"""
Module for testing the check_mass function.
"""

# pylint: disable=import-error

import pytest
from task_1 import check_mass


def test_all_elements_equal():
    """Test if all elements are identical."""
    assert check_mass([1, 1, 1]) == "равны"
    assert check_mass(["a", "a"]) == "равны"


def test_elements_not_equal():
    """Test if elements are different."""
    assert check_mass([1, 2, 1]) == "Не равны"
    assert check_mass([1, 1, "1"]) == "Не равны"


def test_empty_list():
    """Test behavior with an empty list."""
    assert check_mass([]) == "один элемент"


def test_single_element_list():
    """Test behavior with a single element."""
    assert check_mass([42]) == "равны"


def test_invalid_input_type():
    """Test if non-list input raises TypeError."""
    with pytest.raises(TypeError):
        check_mass(123)
    with pytest.raises(TypeError):
        check_mass(None)


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ([7, 7, 7], "равны"),
        ([1, 2, 3], "Не равны"),
        ([], "один элемент"),
        ([0], "равны"),
    ],
)
def test_check_mass_parametrized(input_data, expected):
    """Run multiple test cases using parameterization."""
    assert check_mass(input_data) == expected
