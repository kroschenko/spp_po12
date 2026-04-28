"""
Модуль для поиска наибольшей общей подстроки двух строк.
"""


def common(str1: str, str2: str) -> str:
    """
    Находит наибольшую общую часть (подстроку) двух строк.
    Реализовано с помощью динамического программирования.
    """
    if str1 is None or str2 is None:
        raise TypeError("Аргументы не могут быть None")

    len1, len2 = len(str1), len(str2)
    matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    max_len = 0
    end_index = 0

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
                if matrix[i][j] > max_len:
                    max_len = matrix[i][j]
                    end_index = i
            else:
                matrix[i][j] = 0

    return str1[end_index - max_len : end_index]
