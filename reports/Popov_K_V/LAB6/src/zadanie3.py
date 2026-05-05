"""
Модуль для работы со строками (Задание 3, Вариант 1).
"""

def repeat(pattern, times):
    """
    Строит строку из указанного паттерна, повторённого заданное количество раз.
    """
    if pattern is None:
        raise TypeError("Паттерн не может быть None")
    if times < 0:
        raise ValueError("Количество повторений не может быть отрицательным")
    return pattern * times
