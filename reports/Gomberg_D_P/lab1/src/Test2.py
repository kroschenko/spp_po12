def str_str(haystack: str, needle: str) -> int:
    # Базовые проверки
    if not needle:
        return 0

    n, m = len(haystack), len(needle)

    # Проходим по основной строке
    for i in range(n - m + 1):
        # Вместо создания среза [i:i+m], проверяем символы по одному
        for j in range(m):
            if haystack[i + j] != needle[j]:
                break
        else:
            # Если цикл for не был прерван по break, значит нашли совпадение
            return i

    return -1


# Тест
print(str_str("ffsadbutsad", "sad"))  # Output: 0
