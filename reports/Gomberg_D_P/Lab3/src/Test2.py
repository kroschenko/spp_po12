class OrganizationComponent:
    """Базовый интерфейс для элементов компании."""

    def display(self, depth=0):
        pass


class Employee(OrganizationComponent):
    """Листовой узел: рядовой сотрудник."""

    def __init__(self, name, department, position, salary):
        self.name = name
        self.department = department
        self.position = position
        self.salary = salary

    def display(self, depth=0):
        print(f"{'  ' * depth}- {self.position}: {self.name} (Отдел: {self.department}, Зарплата: {self.salary})")


class Manager(Employee):
    """Компоновщик: руководитель, имеющий подчиненных."""

    def __init__(self, name, department, position, salary):
        super().__init__(name, department, position, salary)
        self.subordinates = []

    def add(self, component):
        if component not in self.subordinates:
            self.subordinates.append(component)

    def remove(self, component):
        self.subordinates.remove(component)

    def display(self, depth=0):
        super().display(depth)
        for sub in self.subordinates:
            sub.display(depth + 1)


if __name__ == "__main__":
    # Формирование иерархии
    ceo = Manager("Иванов И.И.", "Управление", "Генеральный директор", 500000)
    cto = Manager("Петров П.П.", "IT", "Технический директор", 300000)
    hr_head = Manager("Еленина Е.Е.", "Кадры", "HR-директор", 150000)

    lead_dev = Manager("Сидоров С.С.", "IT", "Тимлид", 200000)
    junior_dev = Employee("Алексеев А.А.", "IT", "Младший разработчик", 80000)

    ceo.add(cto)
    ceo.add(hr_head)
    cto.add(lead_dev)
    lead_dev.add(junior_dev)

    print("Иерархическая структура компании:")
    ceo.display()
