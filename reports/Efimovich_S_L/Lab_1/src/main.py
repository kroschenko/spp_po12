class LimitedSet:
    def __init__(self, capacity, items=None):
        if capacity <= 0:
            raise ValueError("Moshnost > 0")
        self._cap = capacity
        self._items = []
        if items:
            unique = []
            for x in items:
                if isinstance(x, int) and x not in unique:
                    unique.append(x)
            if len(unique) > capacity:
                raise ValueError("Previshenie moshnosti")
            self._items = unique

    @property
    def cap(self):
        return self._cap

    @property
    def size(self):
        return len(self._items)

    def add(self, x):
        if not isinstance(x, int):
            raise TypeError("Need cheloe")
        if x in self._items:
            return False
        if len(self._items) >= self._cap:
            raise OverflowError("Mnosestvo polno")
        self._items.append(x)
        return True

    def remove(self, x):
        if isinstance(x, int) and x in self._items:
            self._items.remove(x)
            return True
        return False

    def contains(self, x):
        return isinstance(x, int) and x in self._items

    def union(self, other):
        if not isinstance(other, LimitedSet):
            raise TypeError("Waiting LimitedSet")

        unique = list(set(self._items + other._items))
        total_capacity = self.cap + other.cap

        if len(unique) > total_capacity:
            raise ValueError("Dont have any space")

        return LimitedSet(total_capacity, unique)

    def display(self):
        print(f"Elements: {', '.join(map(str, self._items)) if self._items else 'пусто'} [{self.size}/{self.cap}]")

    def __str__(self):
        if self._items:
            return f"LimitedSet({{{', '.join(map(str, self._items))}}}, {self.size}/{self.cap})"
        return f"LimitedSet(empty, {self.cap})"

    def __eq__(self, other):
        if not isinstance(other, LimitedSet):
            return False
        return set(self._items) == set(other._items)


if __name__ == "__main__":
    s1 = LimitedSet(5, [1, 2, 3])
    s2 = LimitedSet(3)
    s2.add(10)
    s2.add(20)
    print(s1)
    print(s2)
    print(f"Contains 2? {s1.contains(2)}")
    s1.remove(2)
    print(s1)
    s3 = s1.union(s2)
    print(f"Union: {s3}")
    print(f"Equals? {s1 == LimitedSet(5, [1, 3])}")
