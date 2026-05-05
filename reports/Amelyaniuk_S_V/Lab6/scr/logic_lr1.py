"""Модуль с функциями для проверки возраста."""


def check_age(age):
    """Проверяет, является ли возраст допустимым и достаточным для совершеннолетия.

    Args:
        age: Возраст для проверки (число).

    Returns:
        True если возраст 18 или больше, иначе False.

    Raises:
        TypeError: Если возраст не является числом.
        ValueError: Если возраст меньше 0.
    """
    if not isinstance(age, (int, float)):
        raise TypeError("Возраст должен быть числом")
    if age < 0:
        raise ValueError("Возраст не может быть меньше 0")
    return age >= 18
