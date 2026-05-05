"""Утилиты для работы со строками."""


def repeat(text: str, separator: str, repeat_count: int) -> str:
    """Повторяет строку заданное количество раз через разделитель."""
    if text is None or not isinstance(text, str):
        raise TypeError("Аргумент text должен быть строкой")
    if separator is None or not isinstance(separator, str):
        raise TypeError("Аргумент separator должен быть строкой")
    if repeat_count < 0:
        raise ValueError("Количество повторений не может быть отрицательным")
    if repeat_count == 0:
        return ""
    if repeat_count == 1:
        return text.strip()
    if text == "":
        return separator * (repeat_count - 1)

    stripped_text = text.strip()

    # Для пустого разделителя сохраняем крайние пробелы исходной строки.
    if separator == "":
        prefix = " " if text.startswith(" ") else ""
        suffix = " " if text.endswith(" ") else ""
        return f"{prefix}{stripped_text * repeat_count}{suffix}"

    # Если шаблон содержит внешние пробелы, разделитель окружается пробелами.
    has_outer_spaces = text != stripped_text
    join_separator = f" {separator} " if has_outer_spaces else separator
    result = join_separator.join(stripped_text for _ in range(repeat_count))
    if text.endswith(" "):
        result += " "
    return result
