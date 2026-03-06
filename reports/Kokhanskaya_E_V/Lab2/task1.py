class IntegerSet:
    def __init__(self, initial_elements=None):
        # Инициализация: убираем дубликаты из входного списка
        self.elements = []
        if initial_elements:
            for item in initial_elements:
                self.add(item)

    def add(self, value):
        #Добавляет элемент
        if value not in self.elements:
            self.elements.append(value)

    def remove(self, value):
        #Удаляет элемент из множества
        if value in self.elements:
            self.elements.remove(value)

    def contains(self, value):
        #Проверяет, принадлежит ли значение множеству
        return value in self.elements

    def intersection(self, other):
        #Возвращает новое множество — пересечение текущего с другим
        common = [x for x in self.elements if x in other.elements]
        return IntegerSet(common)

    def __str__(self):
        #Вывод элементов множества на консоль
        return f"{{{', '.join(map(str, self.elements))}}}"

    def __eq__(self, other):
        #Сравнение двух множеств (порядок не важен)
        if not isinstance(other, IntegerSet):
            return False
        
        return len(self.elements) == len(other.elements) and \
               all(item in other.elements for item in self.elements)

# Пример
set1 = IntegerSet([1, 2, 3, 3, 4])
set2 = IntegerSet([3, 4, 5, 6])

print(f"Множество 1: {set1}") 
print(f"Принадлежит ли 2 множеству 1? {set1.contains(2)}")

inter = set1.intersection(set2)
print(f"Пересечение: {inter}")

set3 = IntegerSet([4, 3, 2, 1])
print(f"Множество 1 равно Множеству 3? {set1 == set3}") 
