"""
Набор строковых функций для тестирования.
"""

from __future__ import annotations
from typing import Optional


def repeat(pattern: Optional[str], repeat: int) -> str:
    if pattern is None:
        raise TypeError("Pattern cannot be None")
    if repeat < 0:
        raise ValueError("Repeat cannot be negative")
    return pattern * repeat


def keep(string: Optional[str], pattern: Optional[str]) -> Optional[str]:
    if string is None and pattern is None:
        raise TypeError
    if string is None:
        return None
    if pattern is None or pattern == "":
        return ""
    return "".join(ch for ch in string if ch in pattern)


def loose(string: Optional[str], remove: Optional[str]) -> Optional[str]:
    if string is None and remove is None:
        raise TypeError
    if string is None:
        return None
    if remove is None or remove == "":
        return string
    return "".join(ch for ch in string if ch not in remove)


def index_of_difference(str1: Optional[str], str2: Optional[str]) -> int:
    if str1 is None and str2 is None:
        raise TypeError
    if str1 == "" and str2 == "":
        return -1
    if str1 == "" or str2 == "":
        return 0

    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return i

    return -1 if str1 == str2 else min_len


def common(str1: Optional[str], str2: Optional[str]) -> str:
    if str1 is None and str2 is None:
        raise TypeError
    if not str1 or not str2:
        return ""

    result = []
    for a, b in zip(str1, str2):
        if a == b:
            result.append(a)
        else:
            break
    return "".join(result)


def substring_between(string: Optional[str], open_s: Optional[str], close_s: Optional[str]) -> Optional[str]:
    if string is None and open_s is None and close_s is None:
        raise TypeError
    if string is None or open_s is None or close_s is None:
        return None

    if open_s == "" and close_s == "":
        return ""

    start = string.find(open_s)
    if start == -1:
        return None
    start += len(open_s)

    end = string.find(close_s, start)
    if end == -1:
        return None

    return string[start:end]


def levenshtein_distance(s: Optional[str], t: Optional[str]) -> int:
    if s is None and t is None:
        raise TypeError
    if s is None or t is None:
        return -1

    if s == "":
        return len(t)
    if t == "":
        return len(s)

    dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]

    for i in range(len(s) + 1):
        dp[i][0] = i
    for j in range(len(t) + 1):
        dp[0][j] = j

    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            cost = 0 if s[i - 1] == t[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return dp[-1][-1]


def hamming_distance(str1: Optional[str], str2: Optional[str]) -> int:
    if str1 is None and str2 is None:
        raise TypeError
    if str1 is None or str2 is None:
        return -1
    if len(str1) != len(str2):
        raise ValueError("Strings must be same length")

    return sum(a != b for a, b in zip(str1, str2))
