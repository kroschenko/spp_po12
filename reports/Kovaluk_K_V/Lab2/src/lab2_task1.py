class CharSet:
    def get_items(self):
        return self._items.copy()

    def get_max_size(self):
        return self._max_size

    def __init__(self, max_size=10, initial_chars=None):
        self._max_size = max_size
        self._items = []
        if initial_chars:
            for char in initial_chars:
                self.add(char)

    def add(self, char):
        if len(char) != 1:
            print(f"Ошибка: '{char}' не является одиночным символом.")
            return False
        if char in self._items:
            print(f"Элемент '{char}' уже существует в множестве.")
            return False
        if len(self._items) >= self._max_size:
            print(
                f"Ошибка: Достигнута максимальная мощность множества ({self._max_size}). Элемент '{char}' не добавлен."
            )
            return False
        self._items.append(char)
        print(f"Элемент '{char}' успешно добавлен.")
        return True

    def remove(self, char):
        if char in self._items:
            self._items.remove(char)
            print(f"Элемент '{char}' удален.")
            return True
        print(f"Ошибка: Элемент '{char}' не найден.")
        return False

    def contains(self, char):
        return char in self._items

    def union(self, other):
        combined_chars = list(set(self.get_items() + other.get_items()))
        new_set = CharSet(max(self.get_max_size(), other.get_max_size()))
        for char in combined_chars:
            new_set.add(char)
        return new_set

    def intersection(self, other):
        intersected_chars = [char for char in self.get_items() if char in other.get_items()]
        new_set = CharSet(min(self.get_max_size(), other.get_max_size()))
        for char in intersected_chars:
            new_set.add(char)
        return new_set

    def difference(self, other):
        diff_chars = [char for char in self.get_items() if char not in other.get_items()]
        new_set = CharSet(self.get_max_size())
        for char in diff_chars:
            new_set.add(char)
        return new_set

    def display(self):
        print(f"Множество (мощность {len(self._items)}/{self._max_size}): {self._items}")

    def __str__(self):
        return f"CharSet(capacity={self._max_size}, items={self._items})"

    def __eq__(self, other):
        if not isinstance(other, CharSet):
            return False
        return self._max_size == other._max_size and set(self._items) == set(other._items)


if __name__ == "__main__":
    print("--- Демонстрация работы класса CharSet ---")

    set1 = CharSet(5, ["a", "b", "c"])
    print("\nСоздано set1 из списка ['a','b','c'] (макс. 5):")
    set1.display()

    set2 = CharSet(3, "xyz")
    print("\nСоздано set2 из строки 'xyz' (макс. 3):")
    set2.display()

    print("\n--- Операции добавления/удаления ---")
    set1.add("c")
    set1.add("d")
    set1.add("e")
    set1.add("f")
    set1.display()

    set1.remove("a")
    set1.display()
    set1.remove("z")

    print("\n--- Проверка принадлежности ---")
    print(f"Содержит ли set1 символ 'b'? {set1.contains('b')}")
    print(f"Содержит ли set1 символ 'z'? {set1.contains('z')}")

    print("\n--- Теоретико-множественные операции ---")
    set3 = CharSet(4, ["a", "b", "c", "d"])
    set4 = CharSet(4, ["c", "d", "e", "f"])

    print("set3:", set3)
    print("set4:", set4)

    union_set = set3.union(set4)
    print(f"Объединение set3 и set4: {union_set}")

    intersection_set = set3.intersection(set4)
    print(f"Пересечение set3 и set4: {intersection_set}")

    diff_set = set3.difference(set4)
    print(f"Разность set3 и set4 (set3 - set4): {diff_set}")

    print("\n--- Сравнение множеств ---")
    set5 = CharSet(3, "xyz")
    set6 = CharSet(4, "xyz")

    print(f"set2 == set4? {set2 == set4}")
    print(f"set2 == set5? {set2 == set5}")
    print(f"set2 == set6? {set2 == set6}")
