"""Модуль с функциями для работы со строками."""


def index_of_difference(str1, str2):
    """Находит индекс первого различия между двумя строками.

    Args:
        str1: Первая строка (не None).
        str2: Вторая строка (не None).

    Returns:
        Индекс первого различия, -1 если строки идентичны,
        0 если одна из строк пуста.

    Raises:
        TypeError: Если любой из аргументов равен None.
    """
    if str1 is None or str2 is None:
        raise TypeError("Arguments cannot be None")

    if str1 == str2:
        return -1

    if not str1 or not str2:
        return 0

    # Сравниваем посимвольно до конца кратчайшей строки
    length = min(len(str1), len(str2))
    for i in range(length):
        if str1[i] != str2[i]:
            return i

    return length
