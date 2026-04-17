"""String repeat module."""


def repeat(pattern: str, n: int) -> str:
    """Repeat string n times."""
    if pattern is None:
        raise TypeError("pattern must be string")
    if not isinstance(n, int) or n < 0:
        raise ValueError("repeat count must be >= 0")
    return pattern * n
