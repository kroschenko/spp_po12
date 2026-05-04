class IntSet:
    def __init__(self, max_size, values=None):

        self._max_size = max_size
        self._data = []

        if values:
            for v in values:
                self.add(v)

    @property
    def max_size(self):
        return self._max_size

    def add(self, val):
        if not isinstance(val, int):
            print(f"[Ошибка] '{val}' не является целым числом.")
            return

        if val not in self._data:
            if len(self._data) < self._max_size:
                self._data.append(val)
            else:
                print(f"[Ошибка] Множество переполнено! Нельзя добавить {val}")

    def remove(self, val):
        if val in self._data:
            self._data.remove(val)

    def contains(self, val):
        return val in self._data

    def union(self, other):
        new_capacity = self.max_size + other.max_size
        new_set = IntSet(new_capacity)

        for x in self._data:
            new_set.add(x)
        for x in other._data:
            new_set.add(x)

        return new_set

    def __str__(self):
        return f"IntSet({sorted(self._data)}) [Макс. размер: {self._max_size}]"

    def __eq__(self, other):
        if not isinstance(other, IntSet):
            return False
        return sorted(self._data) == sorted(other._data)


if __name__ == "__main__":
    print("\n=== ТЕСТ ===")
    s1 = IntSet(3, [10, 20])
    s2 = IntSet(3, [20, 30, "NotInt"])

    print(f"Сет 1: {s1}")
    print(f"Сет 2: {s2}")

    s3 = s1.union(s2)
    print(f"Объединение (s1 + s2): {s3}")

    s4 = IntSet(5, [30, 10, 20])
    print(f"Равны ли s3 и s4? -> {s3 == s4}")
