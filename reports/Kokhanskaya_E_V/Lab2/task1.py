class IntegerSet:
<<<<<<< HEAD
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
=======
    
    def __init__(self, initial_elements=None):
       
        # Поле: список для хранения элементов множества
        self.__elements = []
        
        # Если переданы начальные элементы, добавляем их
        if initial_elements is not None:
            for element in initial_elements:
                self.add(element)
    
    def add(self, element):
        
        # Проверяем, что элемент целое число
        if not isinstance(element, int):
            raise TypeError("Множество может содержать только целые числа")
        
        # Добавляем только если элемент еще не в множестве
        if element not in self.__elements:
            self.__elements.append(element)
            # Сортируем для удобства (опционально)
            self.__elements.sort()
    
    def remove(self, element):
       
        if element in self.__elements:
            self.__elements.remove(element)
            return True
        return False
    
    def contains(self, element):
       
        return element in self.__elements
    
    def intersection(self, other_set):
       
        if not isinstance(other_set, IntegerSet):
            raise TypeError("Аргумент должен быть объектом класса IntegerSet")
        
        # Находим общие элементы
        common_elements = []
        for element in self.__elements:
            if element in other_set.__elements:
                common_elements.append(element)
        
        # Создаем новое множество с общими элементами
        return IntegerSet(common_elements)
    
    def __str__(self):
        
        if not self.__elements:
            return "{}"
        
        elements_str = ", ".join(str(e) for e in self.__elements)
        return "{" + elements_str + "}"
    
    def __eq__(self, other):
       
        if not isinstance(other, IntegerSet):
            return False
        
        return self.__elements == other.__elements
    
    # Свойство для получения количества элементов (геттер)
    @property
    def size(self):
       
        return len(self.__elements)
    
    # Свойство для получения всех элементов (геттер)
    @property
    def elements(self):
       
        return self.__elements.copy()
    
    # Свойство для установки элементов (сеттер)
    @elements.setter
    def elements(self, new_elements):
        
        self.__elements = []
        for element in new_elements:
            self.add(element)
    
    def display(self):
        
        print(self.__str__())
>>>>>>> lab2
