"""Утилиты для обработки строк."""


def keep(string: str, pattern: str) -> str:
    """
    Оставляет в строке только те символы, которые есть в паттерне,
    сохраняя при этом все пробелы.
    """
    if string is None and pattern is None:
        raise TypeError("Оба аргумента не могут быть None")

    if string is None:
        return None

    if string == "":
        return ""

    if not pattern:
        return ""

    return "".join(char for char in string if char in pattern or char == " ")
