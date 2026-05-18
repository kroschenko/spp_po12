import pytest


def rep(start, end, step):
    if start >= end:
        raise ValueError("start должно быть меньше end")
    result = []
    current = start
    while current <= end:
        result.append(current)
        current += step
    return result


def is_palindrome(s: str) -> bool:
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def test_rep_basic():
    assert rep(1, 5, 1) == [1, 2, 3, 4, 5]


def test_rep_step_2():
    assert rep(1, 10, 2) == [1, 3, 5, 7, 9]


def test_rep_error_start_greater():
    with pytest.raises(ValueError, match="start должно быть меньше end"):
        rep(5, 1, 1)


def test_palindrome_word():
    assert is_palindrome("radar") == True


def test_palindrome_phrase():
    assert is_palindrome("A man a plan a canal panama") == True


def test_non_palindrome():
    assert is_palindrome("hello") == False


def test_palindrome_with_punctuation():
    assert is_palindrome("Was it a car or a cat I saw?") == True


def test_palindrome_mixed_case():
    assert is_palindrome("RaceCar") == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
