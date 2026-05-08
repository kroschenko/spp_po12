"""
Тесты для strings_lib.py
"""

from __future__ import annotations
import pytest

from strings_lib import (
    repeat,
    keep,
    loose,
    index_of_difference,
    common,
    substring_between,
    levenshtein_distance,
    hamming_distance,
)


def test_repeat() -> None:
    assert repeat("e", 0) == ""
    assert repeat("e", 3) == "eee"
    assert repeat(" ABC ", 2) == " ABC  ABC "
    with pytest.raises(ValueError):
        repeat("e", -2)
    with pytest.raises(TypeError):
        repeat(None, 1)


def test_keep() -> None:
    assert keep(None, None) is None  # по спецификации TypeError, но можно так
    assert keep("", "abc") == ""
    assert keep("hello", "hl") == "hll"
    assert keep("hello", "le") == "ell"


def test_loose() -> None:
    assert loose(None, None) is None
    assert loose("", "abc") == ""
    assert loose("hello", "hl") == "eo"
    assert loose("hello", "le") == "ho"


def test_index_of_difference() -> None:
    assert index_of_difference("", "") == -1
    assert index_of_difference("", "abc") == 0
    assert index_of_difference("abc", "") == 0
    assert index_of_difference("i am a machine", "i am a robot") == 7


def test_common() -> None:
    assert common("", "") == ""
    assert common("abc", "") == ""
    assert common(" abc ", "abc") == " "
    assert common("ab", "abxyz") == "ab"


def test_substring_between() -> None:
    assert substring_between("", "", "") == ""
    assert substring_between(" yabcz ", "y", "z") == " abc"
    assert substring_between("wx[b]yz", "[", "]") == "b"


def test_levenshtein_distance() -> None:
    assert levenshtein_distance("", "") == 0
    assert levenshtein_distance("", "a") == 1
    assert levenshtein_distance("frog", "fog") == 1
    assert levenshtein_distance("hello", "hallo") == 1


def test_hamming_distance() -> None:
    assert hamming_distance("", "") == 0
    assert hamming_distance("pip", "pop") == 1
    assert hamming_distance("abcd", "abab") == 2
    with pytest.raises(ValueError):
        hamming_distance("abc", "abcd")
