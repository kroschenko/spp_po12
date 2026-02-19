class VariableSet:
    def __init__(self, initial_elements=None):
        self.elements = []

        if initial_elements:
            for item in initial_elements:
                self.add(item)

    def add(self, element):
        if element not in self.elements:
            self.elements.append(element)

    def remove(self, element):
        if element in self.elements:
            self.elements.remove(element)
        else:
            print(f"Элемент {element} не найден в множестве")

    def contains(self, element):
        return element in self.elements

    def intersection(self, other_set):
        result = VariableSet()

        for element in self.elements:
            if other_set.contains(element):
                result.add(element)

        return result

    def display(self):
        elements_str = ", ".join(str(e) for e in self.elements)
        print(f"{{{elements_str}}}")

    def __eq__(self, other):
        if len(self.elements) != len(other.elements):
            return False

        for element in self.elements:
            if not other.contains(element):
                return False

        return True

    def __len__(self):
        return len(self.elements)


if __name__ == "__main__":
    set1 = VariableSet([1, 2, 3, 4, 5])
    set2 = VariableSet([4, 5, 6, 7, 8])

    print("Множество 1:", end=" ")
    set1.display()

    print("Множество 2:", end=" ")
    set2.display()

    print(f"3 есть в множестве 1? {set1.contains(3)}")
    print(f"10 есть в множестве 1? {set1.contains(10)}")

    intersection_set = set1.intersection(set2)
    print("Пересечение:", end=" ")
    intersection_set.display()

    set1.add(10)
    set1.remove(3)
    print("После изменений:", end=" ")
    set1.display()

    set3 = VariableSet([1, 2, 4, 5, 10])
    print(f"set1 == set3? {set1 == set3}")

    set1.add(5)
    print("Попытка добавить дубликат 5:", end=" ")
    set1.display()
