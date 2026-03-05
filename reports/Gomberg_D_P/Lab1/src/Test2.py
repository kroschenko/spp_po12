def str_str(haystack: str, needle: str) -> int:

    if not needle:
        return 0

    n, m = len(haystack), len(needle)

    for i in range(n - m + 1):
        for j in range(m):
            if haystack[i + j] != needle[j]:
                break
        else:
            # Если цикл for не был прерван по break, значит нашли совпадение
            return i

    return -1


# Тест
print(str_str("fadssadbutsad", "sad"))  # Output: 0
