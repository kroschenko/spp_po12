"""
Модуль string_repeat - реализация функции repeat для строк.

Предоставляет функции для повторения строки заданное количество раз.
"""


def repeat_string(pattern: str, repeat_count: int) -> str:
    """
    Строит строку из указанного паттерна, повторённого заданное количество раз.

    Спецификация:
        repeat_string("e", 0) = ""
        repeat_string("e", 3) = "eee"
        repeat_string("ABC", 2) = "ABCABC"
        repeat_string("e", -2) = ValueError
        repeat_string(None, 1) = TypeError

    Args:
        pattern: строка-паттерн для повторения
        repeat_count: количество повторений (неотрицательное целое)

    Returns:
        Строка, составленная из повторённого паттерна

    Raises:
        TypeError: если pattern не является строкой
        ValueError: если repeat_count отрицательный
    """
    if pattern is None:
        raise TypeError("pattern must be a string, not NoneType")

    if not isinstance(pattern, str):
        raise TypeError(f"pattern must be a string, got {type(pattern).__name__}")

    if not isinstance(repeat_count, int):
        raise TypeError(f"repeat_count must be an integer, got {type(repeat_count).__name__}")

    if repeat_count < 0:
        raise ValueError("repeat count cannot be negative")

    return pattern * repeat_count


def repeat_string_optimized(pattern: str, repeat_count: int) -> str:
    """
    Оптимизированная версия с использованием join для больших строк.

    Args:
        pattern: строка-паттерн для повторения
        repeat_count: количество повторений

    Returns:
        Строка из повторённого паттерна
    """
    if pattern is None:
        raise TypeError("pattern must be a string")

    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    if repeat_count < 0:
        raise ValueError("repeat count cannot be negative")

    if repeat_count == 0:
        return ""

    return ''.join([pattern] * repeat_count)


def repeat_string_with_validation(pattern: str, repeat_count: int) -> str:
    """
    Версия с дополнительной валидацией для очень больших повторений.

    Args:
        pattern: строка-паттерн для повторения
        repeat_count: количество повторений

    Returns:
        Строка из повторённого паттерна

    Raises:
        ValueError: если repeat_count превышает максимально допустимое значение
    """
    max_repeat = 10_000_000  # ограничение для защиты памяти

    if pattern is None:
        raise TypeError("pattern must be a string")

    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    if not isinstance(repeat_count, int):
        raise TypeError("repeat_count must be an integer")

    if repeat_count < 0:
        raise ValueError("repeat count cannot be negative")

    if repeat_count > max_repeat:
        raise ValueError(f"repeat count exceeds maximum allowed ({max_repeat})")

    return pattern * repeat_count
