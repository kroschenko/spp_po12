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


def organization_iterator(component, depth=0):
    """Итератор (генератор) для обхода древовидной структуры."""
    yield (component, depth)
    if isinstance(component, Manager):
        for child in component.subordinates:
            yield from organization_iterator(child, depth + 1)


def generate_salary_report(root_manager):
    """Формирование и сортировка отчета."""
    flat_list = list(organization_iterator(root_manager))

    # Сортировка: по названию отдела (группировка), затем по глубине (старшинству)
    sorted_list = sorted(flat_list, key=lambda x: (x[0].department, x[1]))

    print(f"\n{'ОТДЕЛ':<15} | {'ДОЛЖНОСТЬ':<22} | {'ФИО':<15} | {'ЗАРПЛАТА'}")
    print("-" * 70)

    current_dept = ""
    for emp, _ in sorted_list:
        if current_dept and current_dept != emp.department:
            print("-" * 70)

        print(f"{emp.department:<15} | {emp.position:<22} | {emp.name:<15} | {emp.salary:,} руб.")
        current_dept = emp.department


if __name__ == "__main__":
    ceo = Manager("Иванов И.И.", "Управление", "Генеральный директор", 500000)
    cto = Manager("Петров П.П.", "IT", "Технический директор", 300000)
    lead_dev = Manager("Сидоров С.С.", "IT", "Тимлид", 200000)
    junior_dev = Employee("Алексеев А.А.", "IT", "Младший разработчик", 80000)
    hr = Employee("Еленина Е.Е.", "Кадры", "HR-директор", 150000)

    ceo.add(cto)
    ceo.add(hr)
    cto.add(lead_dev)
    lead_dev.add(junior_dev)

    generate_salary_report(ceo)
