"""
Модуль factorial - вычисление факториала (пример для Задания 2)
"""


def factorial(n: int) -> int:
    """
    Вычисление факториала числа n

    Args:
        n: неотрицательное целое число

    Returns:
        n! = 1 * 2 * ... * n

    Raises:
        ValueError: если n отрицательное
        TypeError: если n не целое число
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")

    if n == 0:
        return 1

    result = 1
    for i in range(1, n + 1):
        result *= i

    return result


def factorial_recursive(n: int) -> int:
    """Рекурсивная версия вычисления факториала"""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")

    if n == 0:
        return 1

    return n * factorial_recursive(n - 1)
