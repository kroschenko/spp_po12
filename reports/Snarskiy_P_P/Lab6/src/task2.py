"""
Тесты для лабораторной работы №1.
Запуск: pytest test_lab1.py -v
"""

import pytest
from lab1 import generate_sequence, is_palindrome


class TestGenerateSequence:
    """Testing generating sequence."""

    def test_simple_ascending(self):
        """Стандартная возрастающая последовательность."""
        assert generate_sequence(1, 5, 1) == [1, 2, 3, 4]

    def test_simple_descending(self):
        """Стандартная убывающая последовательность."""
        assert generate_sequence(5, 1, -1) == [5, 4, 3, 2]

    def test_step_greater_than_one(self):
        """Шаг больше 1 — берём каждый второй элемент."""
        assert generate_sequence(0, 10, 2) == [0, 2, 4, 6, 8]

    def test_negative_step_greater_than_one(self):
        """Отрицательный шаг больше 1 по модулю."""
        assert generate_sequence(10, 0, -3) == [10, 7, 4, 1]

    def test_negative_range_positive_step(self):
        """Диапазон из отрицательных чисел, шаг положительный."""
        assert generate_sequence(-5, 0, 1) == [-5, -4, -3, -2, -1]

    def test_all_negative(self):
        """Оба конца отрицательные, убывание."""
        assert generate_sequence(-1, -5, -1) == [-1, -2, -3, -4]

    def test_start_equals_end(self):
        """start == end → пустой список независимо от шага."""
        assert not generate_sequence(3, 3, 1)
        assert not generate_sequence(3, 3, -1)

    def test_single_element(self):
        """Ровно один элемент: end = start + step."""
        assert generate_sequence(7, 8, 1) == [7]

    def test_step_larger_than_range(self):
        """Шаг больше длины диапазона → только start."""
        assert generate_sequence(0, 3, 10) == [0]

    def test_zero_start(self):
        """start = 0."""
        assert generate_sequence(0, 3, 1) == [0, 1, 2]

    def test_large_step_skips_all_but_start(self):
        """Шаг равен длине диапазона — ровно один элемент."""
        assert generate_sequence(1, 6, 5) == [1]

    def test_step_zero_raises(self):
        """Шаг 0 должен вызывать ValueError."""
        with pytest.raises(ValueError, match="нулю"):
            generate_sequence(1, 10, 0)

    def test_wrong_sign_positive_raises(self):
        """start < end, но step < 0 — недостижимый диапазон."""
        with pytest.raises(ValueError, match="Недостижимый"):
            generate_sequence(1, 10, -1)

    def test_wrong_sign_negative_raises(self):
        """start > end, но step > 0 — недостижимый диапазон."""
        with pytest.raises(ValueError, match="Недостижимый"):
            generate_sequence(10, 1, 1)

    @pytest.mark.parametrize(
        "start, end, step, expected",
        [
            (0, 0, 1, []),  # пустой
            (0, 1, 1, [0]),  # один элемент
            (0, 4, 1, [0, 1, 2, 3]),  # четыре элемента
            (-3, 3, 2, [-3, -1, 1]),  # шаг 2 через ноль
            (6, 0, -2, [6, 4, 2]),  # убывание с шагом -2
        ],
    )
    def test_parametrized(self, start, end, step, expected):
        """Параметризованный тест"""
        assert generate_sequence(start, end, step) == expected


class TestIsPalindrome:
    """Testing palindrome"""

    def test_simple_true(self):
        """Простое слово-палиндром."""
        assert is_palindrome("madam") is True

    def test_simple_false(self):
        """Обычное слово — не палиндром."""
        assert is_palindrome("hello") is False

    def test_classic_phrase(self):
        """Классическая фраза с пробелами и знаками."""
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_with_punctuation(self):
        """Знаки препинания игнорируются."""
        assert is_palindrome("No 'x' in Nixon") is True

    def test_mixed_case(self):
        """Регистр не важен."""
        assert is_palindrome("RaceCar") is True

    def test_numbers(self):
        """Цифровой палиндром."""
        assert is_palindrome("12321") is True

    def test_numbers_false(self):
        """Цифровая строка — не палиндром."""
        assert is_palindrome("12345") is False

    def test_mixed_alpha_and_digits(self):
        """Буквы и цифры вместе."""
        assert is_palindrome("a1b2b1a") is True

    def test_empty_string(self):
        """Пустая строка считается палиндромом."""
        assert is_palindrome("") is True

    def test_single_char(self):
        """Один символ — всегда палиндром."""
        assert is_palindrome("x") is True

    def test_two_same_chars(self):
        """Два одинаковых символа."""
        assert is_palindrome("aa") is True

    def test_two_different_chars(self):
        """Два разных символа."""
        assert is_palindrome("ab") is False

    def test_only_spaces_and_punctuation(self):
        """Строка только из пробелов и знаков — пустая после очистки → палиндром."""
        assert is_palindrome("   !!!   ") is True

    def test_unicode_letters(self):
        """Unicode-буквы: isalnum() должен их учитывать."""
        assert is_palindrome("шалаш") is True

    def test_long_non_palindrome(self):
        """Длинная строка — не палиндром."""
        assert is_palindrome("abcdefghij") is False

    def test_none_raises_type_error(self):
        """None вместо строки → TypeError."""
        with pytest.raises(TypeError, match="str"):
            is_palindrome(None)

    def test_int_raises_type_error(self):
        """Целое число вместо строки → TypeError."""
        with pytest.raises(TypeError, match="str"):
            is_palindrome(12321)

    def test_list_raises_type_error(self):
        """Список вместо строки → TypeError."""
        with pytest.raises(TypeError):
            is_palindrome(["m", "a", "d", "a", "m"])

    @pytest.mark.parametrize(
        "phrase, expected",
        [
            ("", True),  # пустая строка
            ("a", True),  # один символ
            ("aba", True),  # нечётная длина
            ("abba", True),  # чётная длина
            ("abcba", True),  # нечётная длина 5
            ("abc", False),  # не палиндром
            ("Madam", True),  # регистр
            ("Was it a car or a cat I saw", True),  # фраза с пробелами
            ("Never odd or even", True),  # классический
            ("Not a palindrome", False),  # явно не палиндром
        ],
    )
    def test_parametrized(self, phrase, expected):
        """Параметризованный тест"""
        assert is_palindrome(phrase) is expected
