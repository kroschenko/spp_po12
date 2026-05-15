"""
Реализация метода keep(str, pattern).

Спецификация:
    keep(None, None)  → TypeError
    keep(None, *)     → None
    keep("", *)       → ""
    keep(*, None)     → ""
    keep(*, "")       → ""
    keep(" hello ", "hl") → " hll "
    keep(" hello ", "le") → " ell "
"""


def keep(s: str | None, pattern: str | None) -> str | None:
    """
    Оставляет в строке s только те символы, которые присутствуют в pattern.

    Args:
        s:       Исходная строка (или None).
        pattern: Строка-фильтр (или None).

    Returns:
        - None,  если s is None (и pattern не None).
        - "",    если s == "" — независимо от pattern.
        - "",    если pattern is None или pattern == "".
        - Отфильтрованную строку в остальных случаях.

    Raises:
        TypeError: если оба аргумента равны None.
    """
    # keep(None, None) → TypeError
    if s is None and pattern is None:
        raise TypeError("Оба аргумента не могут быть None одновременно.")

    # keep(None, *) → None
    if s is None:
        return None

    # keep("", *) → ""
    if s == "":
        return ""

    # keep(*, None) → ""  |  keep(*, "") → ""
    if pattern is None or pattern == "":
        return ""

    # Основная логика: оставляем только символы, входящие в pattern
    allowed = set(pattern)
    return "".join(c for c in s if c in allowed)
