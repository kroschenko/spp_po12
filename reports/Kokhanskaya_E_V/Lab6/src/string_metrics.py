"""String metrics implementation including Levenshtein distance."""

from typing import Optional


def levenshtein_distance(s: Optional[str], t: Optional[str]) -> int:
    """
    Calculate Levenshtein distance between two strings.

    Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, substitutions) required to change one string into another.

    Args:
        s: First string
        t: Second string

    Returns:
        Levenshtein distance as integer

    Raises:
        TypeError: If both arguments are None
    """
    # Handle None cases
    if s is None and t is None:
        raise TypeError("Both arguments cannot be None")
    if s is None or t is None:
        return -1

    # Handle empty strings
    if not s:
        return len(t)
    if not t:
        return len(s)

    len_s = len(s)
    len_t = len(t)

    # Create and initialize distance matrix
    dp = [[0] * (len_t + 1) for _ in range(len_s + 1)]

    for i in range(len_s + 1):
        dp[i][0] = i
    for j in range(len_t + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[len_s][len_t]
