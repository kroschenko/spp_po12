"""Module implementing IntegerSet class for integer collections."""

from typing import List, Union, Iterator


class IntegerSet:
    """A set implementation for integers only."""

    def __init__(self, initial_elements: Union[List[int], None] = None) -> None:
        """Initialize IntegerSet with optional initial elements."""
        self._elements: List[int] = []
        if initial_elements:
            for element in initial_elements:
                self.add(element)

    @property
    def elements(self) -> List[int]:
        """Return sorted list of elements."""
        return sorted(self._elements)

    @property
    def size(self) -> int:
        """Return number of elements in the set."""
        return len(self._elements)

    def add(self, value: int) -> bool:
        """
        Add integer to set.

        Args:
            value: Integer to add.

        Returns:
            True if added, False if already exists.

        Raises:
            TypeError: If value is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"Only integers are allowed, got {type(value).__name__}")
        if value not in self._elements:
            self._elements.append(value)
            return True
        return False

    def remove(self, value: int) -> bool:
        """
        Remove integer from set.

        Args:
            value: Integer to remove.

        Returns:
            True if removed, False if not found.

        Raises:
            TypeError: If value is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"Only integers are allowed, got {type(value).__name__}")
        if value in self._elements:
            self._elements.remove(value)
            return True
        return False

    def contains(self, value: int) -> bool:
        """
        Check if value exists in set.

        Args:
            value: Integer to check.

        Returns:
            True if exists, False otherwise.

        Raises:
            TypeError: If value is not an integer.
        """
        if not isinstance(value, int):
            raise TypeError(f"Only integers are allowed, got {type(value).__name__}")
        return value in self._elements

    def intersection(self, other: "IntegerSet") -> "IntegerSet":
        """
        Return intersection with another IntegerSet.

        Args:
            other: Another IntegerSet instance.

        Returns:
            New IntegerSet with common elements.

        Raises:
            TypeError: If other is not an IntegerSet.
        """
        if not isinstance(other, IntegerSet):
            raise TypeError(
                f"Can only intersect with IntegerSet, " f"got {type(other).__name__}"
            )
        result = IntegerSet()
        for element in self._elements:
            if other.contains(element):
                result.add(element)
        return result

    def display(self) -> None:
        """Print set in {a, b, c} format."""
        if not self._elements:
            print("{}")
        else:
            sorted_elements = sorted(self._elements)
            print(f"{{{', '.join(map(str, sorted_elements))}}}")

    def __str__(self) -> str:
        """Return string representation in {a, b, c} format."""
        if not self._elements:
            return "{}"
        sorted_elements = sorted(self._elements)
        return f"{{{', '.join(map(str, sorted_elements))}}}"

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"IntegerSet({self._elements})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another IntegerSet."""
        if not isinstance(other, IntegerSet):
            return NotImplemented
        return set(self._elements) == set(other._elements)

    def __len__(self) -> int:
        """Return number of elements."""
        return len(self._elements)

    def __iter__(self) -> Iterator[int]:
        """Return iterator over sorted elements."""
        return iter(sorted(self._elements))

    def __contains__(self, value: int) -> bool:
        """Check if value is in set using 'in' operator."""
        return self.contains(value)
