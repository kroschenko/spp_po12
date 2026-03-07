class LimitedSet:
    def __init__(self, capacity, initial=None):
        self.capacity = capacity
        self._data = []

        if initial:
            for item in initial:
                self.add(item)

    def items(self):
        return list(self._data)

    def add(self, item):
        if len(self._data) >= self.capacity:
            raise ValueError("Множество заполнено")
        if item not in self._data:
            self._data.append(item)

    def remove(self, item):
        if item in self._data:
            self._data.remove(item)

    def contains(self, item):
        return item in self._data

    def union(self, other):
        if not isinstance(other, LimitedSet):
            raise TypeError("Можно объединять только с LimitedSet")

        new_capacity = self.capacity + other.capacity
        result = LimitedSet(new_capacity)

        for item in self.items():
            result.add(item)

        for item in other.items():
            result.add(item)

        return result

    def __str__(self):
        return "{" + ", ".join(self._data) + "}"

    def __eq__(self, other):
        if not isinstance(other, LimitedSet):
            return False
        return sorted(self._data) == sorted(other._data)


s1 = LimitedSet(5, ["a", "b", "c"])
s2 = LimitedSet(5, ["c", "d", "e"])

print("Set 1:", s1)
print("Set 2:", s2)
print("Union:", s1.union(s2))
print("Contains 'b':", s1.contains("b"))
