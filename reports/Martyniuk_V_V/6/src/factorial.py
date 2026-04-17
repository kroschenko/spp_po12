"""Factorial module."""


def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if not isinstance(n, int):
        raise TypeError("n must be integer")
    if n < 0:
        raise ValueError("n must be >= 0")
    return 1 if n == 0 else n * factorial(n - 1)
