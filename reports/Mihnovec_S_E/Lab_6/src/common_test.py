"""
Тесты для функции common.
"""

import pytest
from string_utils import common


def test_common_spec():
    """
    Проверка случаев из спецификации с исправлением логических опечаток.
    """
    with pytest.raises(TypeError):
        common(None, None)

    assert common("", "") == ""
    assert common("", " abc ") == ""
    assert common(" abc ", "") == ""

    assert common(" abc ", "abc") == "abc"

    assert common("ab", " abxyz ") == "ab"

    assert common(" abcde ", " abxyz ") == " ab"

    assert common(" abcde ", " xyz ") == " "

    assert common(" deabc ", " abcdeabcd ") == "deabc"
    assert common(" dfabcegt ", " rtoefabceiq ") == "fabce"


if __name__ == "__main__":
    pytest.main([__file__])
