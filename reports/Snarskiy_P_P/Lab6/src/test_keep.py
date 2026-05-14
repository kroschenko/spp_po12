"""
Тесты для метода keep(str, pattern) — написаны ДО реализации (TDD).
Запуск: pytest test_keep.py -v
"""

import pytest
from keep import keep


def test_both_none_raises_type_error():
    """keep(None, None) → TypeError."""
    with pytest.raises(TypeError):
        keep(None, None)


@pytest.mark.parametrize("pattern", ["hl", "", "abc", " "])
def test_str_none_returns_none(pattern):
    """keep(None, *) → None  (str=None, pattern — любой не-None)."""
    assert keep(None, pattern) is None


@pytest.mark.parametrize("pattern", ["hl", "", "abc", " ", None])
def test_empty_str_returns_empty(pattern):
    """keep('', *) → ''  (пустая строка — любой pattern, включая None)."""
    # Исключение: keep(None, None) уже покрыто отдельным тестом,
    # здесь str всегда '', поэтому None-pattern допустим.
    assert keep("", pattern) == ""


@pytest.mark.parametrize("s", ["hello", "world", "test", " hello "])
def test_pattern_none_returns_empty(s):
    """keep(*, None) → ''  (str не None, pattern=None)."""
    assert keep(s, None) == ""


@pytest.mark.parametrize("s", ["hello", "world", "test", " hello "])
def test_pattern_empty_returns_empty(s):
    """keep(*, '') → ''  (pattern — пустая строка)."""
    assert keep(s, "") == ""


def test_spec_example_hl():
    """keep(' hello ', 'hl') = ' hll '  — из спецификации."""
    assert keep(" hello ", "hl") == " hll "


def test_spec_example_le():
    """keep(' hello ', 'le') = ' ell '  — из спецификации."""
    assert keep(" hello ", "le") == " ell "
