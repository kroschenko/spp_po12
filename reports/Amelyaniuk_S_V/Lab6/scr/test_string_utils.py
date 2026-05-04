import pytest
from string_utils import indexOfDifference


def test_index_of_difference():
    # Согласно спецификации варианта 5:
    with pytest.raises(TypeError):
        indexOfDifference(None, None)

    assert indexOfDifference("", "") == -1
    assert indexOfDifference("", "abc") == 0
    assert indexOfDifference("abc", "") == 0
    assert indexOfDifference("abc", "abc") == -1
    assert indexOfDifference("ab", "abxyz") == 2
    assert indexOfDifference("abcde", "abxyz") == 2
    assert indexOfDifference("abcde", "xyz") == 0
