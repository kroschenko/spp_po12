"""
Тесты для модуля factorial (Задание 2)
"""

import pytest
from factorial import factorial, factorial_recursive

# ========== Тесты для итеративной версии ==========


class TestFactorialIterative:
    """Тесты для итеративной версии факториала"""

    def test_factorial_zero(self):
        """Проверка: 0! = 1"""
        assert factorial(0) == 1

    def test_factorial_one(self):
        """Проверка: 1! = 1"""
        assert factorial(1) == 1

    def test_factorial_two(self):
        """Проверка: 2! = 2"""
        assert factorial(2) == 2

    def test_factorial_three(self):
        """Проверка: 3! = 6"""
        assert factorial(3) == 6

    def test_factorial_five(self):
        """Проверка: 5! = 120"""
        assert factorial(5) == 120

    def test_factorial_ten(self):
        """Проверка: 10! = 3628800"""
        assert factorial(10) == 3628800

    # Параметризованный тест для нескольких значений
    @pytest.mark.parametrize(
        "n,expected",
        [
            (0, 1),
            (1, 1),
            (2, 2),
            (3, 6),
            (4, 24),
            (5, 120),
            (6, 720),
            (7, 5040),
        ],
    )
    def test_factorial_parametrized(self, n, expected):
        """Параметризованная проверка факториала"""
        assert factorial(n) == expected

    # Тесты на исключения
    def test_factorial_negative(self):
        """Проверка выброса ValueError для отрицательных чисел"""
        with pytest.raises(
            ValueError, match="Factorial not defined for negative numbers"
        ):
            factorial(-1)

    def test_factorial_negative_large(self):
        """Проверка для большого отрицательного числа"""
        with pytest.raises(ValueError):
            factorial(-100)

    def test_factorial_float(self):
        """Проверка выброса TypeError для чисел с плавающей точкой"""
        with pytest.raises(TypeError, match="n must be an integer"):
            factorial(5.5)

    def test_factorial_string(self):
        """Проверка выброса TypeError для строк"""
        with pytest.raises(TypeError):
            factorial("5")

    def test_factorial_none(self):
        """Проверка выброса TypeError для None"""
        with pytest.raises(TypeError):
            factorial(None)

    # Граничные случаи
    def test_factorial_large_number(self):
        """Проверка для большого числа (должно работать без переполнения в Python)"""
        # Python поддерживает длинную арифметику
        result = factorial(20)
        assert result == 2432902008176640000

    def test_factorial_type_error_message(self):
        """Проверка сообщения об ошибке типа"""
        with pytest.raises(TypeError) as exc_info:
            factorial(3.14)
        assert "must be an integer" in str(exc_info.value)


# ========== Тесты для рекурсивной версии ==========


class TestFactorialRecursive:
    """Тесты для рекурсивной версии факториала"""

    @pytest.mark.parametrize(
        "n,expected", [(0, 1), (1, 1), (2, 2), (3, 6), (4, 24), (5, 120)]
    )
    def test_recursive_parametrized(self, n, expected):
        """Параметризованная проверка рекурсивной версии"""
        assert factorial_recursive(n) == expected

    def test_recursive_negative(self):
        """Проверка исключения для отрицательных чисел"""
        with pytest.raises(ValueError):
            factorial_recursive(-5)

    def test_recursive_type_error(self):
        """Проверка исключения для неверного типа"""
        with pytest.raises(TypeError):
            factorial_recursive(5.5)

    def test_recursive_large(self):
        """Проверка для большого числа"""
        assert factorial_recursive(10) == 3628800
        assert factorial_recursive(15) == 1307674368000


# ========== Сравнительные тесты ==========


def test_both_versions_agree():
    """Проверка, что обе версии дают одинаковые результаты"""
    for n in range(10):
        assert factorial(n) == factorial_recursive(n)
