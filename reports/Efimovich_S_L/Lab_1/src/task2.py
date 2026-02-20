from typing import List, Optional, Set, Iterable


class LimitedSet:
    def __init__(self, capacity: int, items: Optional[Iterable[int]] = None):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self._capacity = capacity
        self._elements: List[int] = []

        if items is not None:
            unique_items = self._get_unique_integers(items)

            if len(unique_items) > capacity:
                raise ValueError("Number of unique items exceeds capacity")

            self._elements = list(unique_items)

    @staticmethod
    def _get_unique_integers(items: Iterable[int]) -> Set[int]:
        unique = set()
        for item in items:
            if not isinstance(item, int):
                raise TypeError(f"Expected integer, got {type(item).__name__}")
            unique.add(item)
        return unique

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def size(self) -> int:
        return len(self._elements)

    @property
    def elements(self) -> List[int]:
        return self._elements.copy()

    def add(self, value: int) -> bool:
        if not isinstance(value, int):
            raise TypeError(f"Expected integer, got {type(value).__name__}")

        if value in self._elements:
            return False

        if self.size >= self._capacity:
            raise OverflowError(f"Set is at full capacity ({self._capacity})")

        self._elements.append(value)
        return True

    def remove(self, value: int) -> bool:
        if isinstance(value, int) and value in self._elements:
            self._elements.remove(value)
            return True
        return False

    def contains(self, value: int) -> bool:
        return isinstance(value, int) and value in self._elements

    def union(self, other: "LimitedSet") -> "LimitedSet":
        if not isinstance(other, LimitedSet):
            raise TypeError(f"Expected LimitedSet, got {type(other).__name__}")

        combined_elements = list(set(self._elements + other._elements))
        total_capacity = self.capacity + other.capacity

        if len(combined_elements) > total_capacity:
            raise ValueError("Combined unique elements exceed total capacity")

        return LimitedSet(total_capacity, combined_elements)

    def intersection(self, other: "LimitedSet") -> "LimitedSet":
        if not isinstance(other, LimitedSet):
            raise TypeError(f"Expected LimitedSet, got {type(other).__name__}")

        common_elements = [x for x in self._elements if x in other._elements]
        return LimitedSet(min(self.capacity, other.capacity), common_elements)

    def difference(self, other: "LimitedSet") -> "LimitedSet":
        if not isinstance(other, LimitedSet):
            raise TypeError(f"Expected LimitedSet, got {type(other).__name__}")

        diff_elements = [x for x in self._elements if x not in other._elements]
        return LimitedSet(self.capacity, diff_elements)

    def is_subset(self, other: "LimitedSet") -> bool:
        if not isinstance(other, LimitedSet):
            raise TypeError(f"Expected LimitedSet, got {type(other).__name__}")

        return all(x in other._elements for x in self._elements)

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size == self.capacity

    def clear(self) -> None:
        self._elements.clear()

    def display(self) -> None:
        elements_str = ", ".join(map(str, self._elements)) if self._elements else "empty"
        print(f"{{{elements_str}}} [{self.size}/{self.capacity}]")

    def to_list(self) -> List[int]:
        return self._elements.copy()

    def to_set(self) -> Set[int]:
        return set(self._elements)

    def __str__(self) -> str:
        elements_str = ", ".join(map(str, self._elements)) if self._elements else "empty"
        return f"LimitedSet({{{elements_str}}}, {self.size}/{self.capacity})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LimitedSet):
            return False
        return set(self._elements) == set(other._elements)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __len__(self) -> int:
        return self.size

    def __contains__(self, value: int) -> bool:
        return self.contains(value)

    def __iter__(self):
        return iter(self._elements)

    def __add__(self, other: "LimitedSet") -> "LimitedSet":
        return self.union(other)

    def __sub__(self, other: "LimitedSet") -> "LimitedSet":
        return self.difference(other)

    def __and__(self, other: "LimitedSet") -> "LimitedSet":
        return self.intersection(other)

    def __or__(self, other: "LimitedSet") -> "LimitedSet":
        return self.union(other)


if __name__ == "__main__":
    s1 = LimitedSet(5, [1, 2, 3])
    s2 = LimitedSet(3)
    s2.add(10)
    s2.add(20)

    print(s1)
    print(s2)
    print(f"Contains 2? {2 in s1}")

    s1.remove(2)
    print(s1)

    s3 = s1 + s2
    print(f"Union: {s3}")

    print(f"Equals? {s1 == LimitedSet(5, [1, 3])}")

    s4 = LimitedSet(3, [1, 2, 3])
    s5 = LimitedSet(5, [2, 3, 4, 5])

    print(f"Intersection: {s4 & s5}")
    print(f"Difference: {s4 - s5}")
    print(f"Is subset? {s4.is_subset(s5)}")

    print(f"Elements: {list(s4)}")

    for items in s4:
        print(f"Element: {items}")
