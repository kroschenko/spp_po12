"""Tests for string metrics functions."""

import pytest
from string_metrics import levenshtein_distance


class TestLevenshteinDistance:  # pylint: disable=too-many-public-methods
    """Test cases for levenshtein_distance function."""

    # ========== TRIVIAL CASES ==========

    def test_both_empty_strings(self):
        """Test with both strings empty."""
        assert levenshtein_distance("", "") == 0

    def test_first_empty_second_nonempty(self):
        """Test with first string empty, second non-empty."""
        assert levenshtein_distance("", "a") == 1
        assert levenshtein_distance("", "abc") == 3

    def test_first_nonempty_second_empty(self):
        """Test with first non-empty, second string empty."""
        assert levenshtein_distance("a", "") == 1
        assert levenshtein_distance("aaapppp", "") == 7

    def test_identical_strings(self):
        """Test with identical strings."""
        assert levenshtein_distance("hello", "hello") == 0
        assert levenshtein_distance("", "") == 0
        assert levenshtein_distance("a", "a") == 0

    # ========== BOUNDARY CASES ==========

    def test_single_character_difference(self):
        """Test strings differing by one character."""
        assert levenshtein_distance("frog", "fog") == 1

    def test_complete_difference(self):
        """Test completely different strings."""
        assert levenshtein_distance("fly", "ant") == 3

    def test_one_character_strings(self):
        """Test single character strings."""
        assert levenshtein_distance("a", "b") == 1
        assert levenshtein_distance("a", "a") == 0

    # ========== SPECIFICATION TESTS ==========

    def test_spec_example_frog_fog(self):
        """Test from spec: frog vs fog."""
        assert levenshtein_distance("frog", "fog") == 1

    def test_spec_example_elephant_hippo(self):
        """Test from spec: elephant vs hippo."""
        assert levenshtein_distance("elephant", "hippo") == 7

    def test_spec_example_hippo_elephant(self):
        """Test from spec: hippo vs elephant (symmetric)."""
        assert levenshtein_distance("hippo", "elephant") == 7

    def test_spec_example_hippo_zzzzzzzz(self):
        """Test from spec: hippo vs zzzzzzzz."""
        assert levenshtein_distance("hippo", "zzzzzzzz") == 8

    def test_spec_example_hello_hallo(self):
        """Test from spec: hello vs hallo."""
        assert levenshtein_distance("hello", "hallo") == 1

    def test_spec_empty_and_a(self):
        """Test from spec: empty string vs a."""
        assert levenshtein_distance("", "a") == 1

    def test_spec_aaapppp_and_empty(self):
        """Test from spec: aaapppp vs empty."""
        assert levenshtein_distance("aaapppp", "") == 7

    # ========== EXCEPTION CASES ==========

    def test_both_none(self):
        """Test with both arguments None raises TypeError."""
        with pytest.raises(TypeError, match="Both arguments cannot be None"):
            levenshtein_distance(None, None)

    def test_first_none(self):
        """Test with first argument None returns -1."""
        assert levenshtein_distance(None, "abc") == -1

    def test_second_none(self):
        """Test with second argument None returns -1."""
        assert levenshtein_distance("abc", None) == -1

    # ========== ADDITIONAL EDGE CASES ==========

    def test_unicode_strings(self):
        """Test with Unicode strings."""
        assert levenshtein_distance("café", "cafe") == 1

    def test_very_long_strings(self):
        """Test with long strings."""
        long_str1 = "a" * 1000
        long_str2 = "a" * 1000
        assert levenshtein_distance(long_str1, long_str2) == 0

    def test_case_sensitivity(self):
        """Test that function is case-sensitive."""
        assert levenshtein_distance("Hello", "hello") == 1

    def test_symmetric_property(self):
        """Test that distance is symmetric."""
        assert levenshtein_distance("kitten", "sitting") == levenshtein_distance(
            "sitting", "kitten"
        )

    def test_triangle_inequality(self):
        """Test triangle inequality property."""
        a = "cat"
        b = "bat"
        c = "bet"
        d_ab = levenshtein_distance(a, b)
        d_bc = levenshtein_distance(b, c)
        d_ac = levenshtein_distance(a, c)
        assert d_ac <= d_ab + d_bc

    # ========== PARAMETRIZED TESTS ==========

    @pytest.mark.parametrize(
        "s,t,expected",
        [
            ("", "", 0),
            ("a", "", 1),
            ("", "a", 1),
            ("a", "a", 0),
            ("ab", "ac", 1),
            ("abc", "ac", 1),
            ("abc", "abcd", 1),
            ("kitten", "sitting", 3),
            ("flaw", "lawn", 2),
            ("book", "back", 2),
        ],
    )
    def test_parametrized_distances(self, s, t, expected):
        """Parametrized test for various string pairs."""
        assert levenshtein_distance(s, t) == expected

    @pytest.mark.parametrize(
        "s,t",
        [
            (None, "abc"),
            ("abc", None),
            (None, ""),
            ("", None),
        ],
    )
    def test_one_none_returns_minus_one(self, s, t):
        """Test that None with non-None returns -1."""
        assert levenshtein_distance(s, t) == -1
