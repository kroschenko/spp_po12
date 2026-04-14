"""
Модуль реализует класс BoundedIntSet.
Это пользовательская структура данных, представляющая собой 
множество целых чисел с ограничением по максимальной мощности.
"""


class BoundedIntSet:
    """Класс для работы с множеством целых чисел ограниченной мощности."""

    def __init__(self, capacity: int, initial_elements=None):
        """Инициализирует множество заданной мощности."""
        if capacity < 0:
            raise ValueError("Мощность множества не может быть отрицательной.")

        self._capacity = capacity
        self._elements =[]

        if initial_elements is not None:
            for item in initial_elements:
                self.add(item)

    @property
    def capacity(self) -> int:
        """Возвращает максимальную мощность множества."""
        return self._capacity

    @capacity.setter
    def capacity(self, value: int):
        """Устанавливает новую мощность множества."""
        if value < 0:
            raise ValueError("Мощность множества не может быть отрицательной.")
        if value < len(self._elements):
            raise ValueError(
                "Новая мощность меньше текущего количества элементов в множестве."
            )
        self._capacity = value

    @property
    def elements(self) -> list:
        """Возвращает копию списка элементов множества."""
        return self._elements.copy()

    def add(self, value: int):
        """Добавляет новый уникальный элемент в множество."""
        if not isinstance(value, int):
            raise TypeError("Множество может содержать только целые числа.")

        if value not in self._elements:
            if len(self._elements) >= self._capacity:
                raise OverflowError(
                    f"Невозможно добавить элемент {value}: "
                    f"мощность множества ({self._capacity})."
                )
            self._elements.append(value)

    def remove(self, value: int):
        """Удаляет элемент из множества. Выбрасывает ошибку, если его нет."""
        if value in self._elements:
            self._elements.remove(value)
        else:
            raise ValueError(f"Элемент {value} не найден в множестве.")

    def contains(self, value: int) -> bool:
        """Проверяет, принадлежит ли элемент множеству."""
        return value in self._elements

    def union(self, other: "BoundedIntSet") -> "BoundedIntSet":
        """Возвращает новое множество, являющееся объединением текущего и другого."""
        if not isinstance(other, BoundedIntSet):
            raise TypeError("Объединять можно только с объектом типа BoundedIntSet.")

        new_capacity = self.capacity + other.capacity
        new_set = BoundedIntSet(new_capacity)

        for item in self._elements:
            new_set.add(item)
        for item in other.elements:
            new_set.add(item)

        return new_set

    def __str__(self) -> str:
        """Возвращает строковое представление множества."""
        return (
            f"{{ {', '.join(map(str, self._elements))} }} (Мощность: {self._capacity})"
        )

    def __eq__(self, other) -> bool:
        """Сравнивает два множества на равенство элементов."""
        if not isinstance(other, BoundedIntSet):
            return False
        return sorted(self._elements) == sorted(other.elements)


if __name__ == "__main__":
    print("1. Создание объектов с начальной инициализацией:")
    set1 = BoundedIntSet(capacity=5, initial_elements=[1, 2, 3, 3])
    set2 = BoundedIntSet(capacity=4, initial_elements=[3, 4, 5])
    print(f"Множество 1: {set1}")
    print(f"Множество 2: {set2}")

    print("\n2. Проверка на принадлежность элемента множеству:")
    print(f"Принадлежит ли 2 первому множеству? -> {set1.contains(2)}")
    print(f"Принадлежит ли 10 первому множеству? -> {set1.contains(10)}")

    print("\n3. Добавление и удаление элементов:")
    set1.add(10)
    print(f"Множество 1 после добавления 10: {set1}")
    set1.remove(2)
    print(f"Множество 1 после удаления 2: {set1}")

    print("\n4. Объединение двух множеств:")
    union_set = set1.union(set2)
    print(f"Объединение множества 1 и 2: {union_set}")

    print("\n5. Сравнение объектов (__eq__):")
    set3 = BoundedIntSet(capacity=10, initial_elements=[1, 3, 10])
    set4 = BoundedIntSet(capacity=3, initial_elements=[10, 3, 1])
    print(f"Множество 3: {set3}")
    print(f"Множество 4: {set4}")
    print(f"Равны ли Множество 3 и Множество 4? -> {set3 == set4}")

    print("\n6. Проверка ограничения мощности:")
    try:
        set_full = BoundedIntSet(capacity=2, initial_elements=[100, 200])
        set_full.add(300)
    except OverflowError as err:
        print(f"Исключение при добавлении: {err}")
