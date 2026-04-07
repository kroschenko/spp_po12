"""
Модуль для работы с множеством вещественных чисел.
Реализует операции добавления, удаления и объединения множеств.
"""


class Mnojestvo:
    """
    Класс для представления математического множества вещественных чисел.
    Элементы хранятся в списке, дубликаты исключаются.
    """

    def __init__(self, init_data=None):
        """Инициализирует множество начальными данными."""
        self.items = []
        if init_data:
            for x in init_data:
                self.add(x)

    def add(self, value):
        """Добавляет вещественное число в множество, если оно отсутствует."""
        if value not in self.items:
            self.items.append(float(value))

    def remove(self, value):
        """Удаляет число из множества, если оно в нем есть."""
        if value in self.items:
            self.items.remove(value)

    def is_member(self, value):
        """Возвращает истину, если число принадлежит множеству."""
        return value in self.items

    def union(self, other_set):
        """Возвращает новое множество, объединяющее текущее и другое."""
        new_set = Mnojestvo(self.items)
        for i in other_set.items:
            new_set.add(i)
        return new_set

    def __eq__(self, value):
        """Сравнивает два множества на равенство элементов."""
        if not isinstance(value, Mnojestvo):
            return False
        if len(self.items) != len(value.items):
            return False
        for i in self.items:
            if i not in value.items:
                return False
        return True

    def __str__(self):
        """Возвращает строковое представление элементов множества."""
        return f"элементы {self.items}"


def main():
    """Демонстрация работы класса Множество."""
    set_a = Mnojestvo([1.1, 2.2, 3.3])
    set_b = Mnojestvo([3.3, 4.4, 5.5])

    print(f"Множество а: {set_a}")
    print(f"Множество b: {set_b}\n")

    print("Добавление элементов")
    set_a.add(4.4)
    print(f"Множество а: {set_a}\n")

    print("Удаление элементов")
    set_a.remove(4.4)
    print(f"Множество а: {set_a}\n")

    print("Принадлежность")
    print("Есть ли 1.1 в множестве а? Ответ:", set_a.is_member(1.1))

    print("\nОбъединение")
    test_set = set_a.union(set_b)
    print(f"Получили объединение: {test_set} \n")

    print("Сравнение")
    print("а равно b? Ответ:", set_a == set_b)


if __name__ == "__main__":
    main()
