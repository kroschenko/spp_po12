class IntegerSet:
    
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