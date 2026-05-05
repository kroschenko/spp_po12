"""Функции, выделенные из лабораторной работы №1."""


def median(numbers: list[int]) -> float:
    """Возвращает медиану списка чисел."""
    if not numbers:
        raise ValueError("Список чисел не должен быть пустым")

    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)
    middle = length // 2

    if length % 2 == 1:
        return float(sorted_numbers[middle])
    return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2


def increment_digits(digits: list[int]) -> list[int]:
    """Прибавляет единицу к числу, представленному списком цифр."""
    if not digits:
        raise ValueError("Список цифр не должен быть пустым")
    if any(digit < 0 or digit > 9 for digit in digits):
        raise ValueError("Все элементы должны быть цифрами от 0 до 9")

    result = digits.copy()
    index = len(result) - 1

    while index >= 0 and result[index] == 9:
        result[index] = 0
        index -= 1

    if index < 0:
        result.insert(0, 1)
    else:
        result[index] += 1

    return result
