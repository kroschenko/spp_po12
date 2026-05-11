def substring_between(s, open_str, close_str):
    """
    Выделяет подстроку между открывающей (open_str) и закрывающей (close_str) строками.

    Спецификация:
        substringBetween(None, None, None)      -> TypeError
        substringBetween(None, *, *)            -> None
        substringBetween(*, None, *)            -> None
        substringBetween(*, *, None)            -> None
        substringBetween("", "", "")            -> ""
        substringBetween("", "", "]")           -> None
        substringBetween("", "[", "]")          -> None
        substringBetween("yabcz", "", "")       -> ""
        substringBetween("yabcz", "y", "z")     -> "abc"
        substringBetween("yabczyabcz", "y", "z")-> "abc"
        substringBetween("wx[b]yz", "[", "]")   -> "b"
    """
    # Все три аргумента None — TypeError
    if s is None and open_str is None and close_str is None:
        raise TypeError("Все аргументы не могут быть None одновременно.")

    # Любой из аргументов None — возвращаем None
    if s is None or open_str is None or close_str is None:
        return None

    # Оба разделителя — пустые строки
    if open_str == "" and close_str == "":
        return ""

    # Ищем вхождение открывающей строки
    start_index = s.find(open_str)
    if start_index == -1:
        return None

    # Начало подстроки — сразу после open_str
    after_open = start_index + len(open_str)

    # Ищем закрывающую строку начиная после open_str
    end_index = s.find(close_str, after_open)
    if end_index == -1:
        return None

    return s[after_open:end_index]
