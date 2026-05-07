# pylint: disable=invalid-name
"""
Модуль для управления структурой IT-компании.
Реализует иерархию сотрудников через паттерн Компоновщик.
"""


class Employee:
    """Класс сотрудника, поддерживающий древовидную структуру подчинения."""

    def __init__(self, name: str, department: str, position: str, salary: float):
        """Инициализация данных сотрудника."""
        self.name: str = name
        self.department: str = department
        self.position: str = position
        self.salary: float = salary
        self._subordinates: list = []
        self.manager: Employee = None

    def add_subordinate(self, employee: "Employee") -> None:
        """Добавляет другого сотрудника в список подчиненных."""
        if employee not in self._subordinates:
            employee.manager = self
            self._subordinates.append(employee)
            print(f"-> {employee.name} теперь подчиняется {self.name}")

    def remove_subordinate(self, employee: "Employee") -> None:
        """Удаляет сотрудника из списка подчиненных."""
        if employee in self._subordinates:
            employee.manager = None
            self._subordinates.remove(employee)
            print(f"-> {employee.name} удален из подчинения {self.name}")
        else:
            print(f"-> Ошибка: {employee.name} не подчиняется {self.name}")

    def get_subordinates(self) -> list:
        """Возвращает список всех прямых подчиненных."""
        return self._subordinates

    def show_details(self, level: int = 0) -> None:
        """Рекурсивно выводит структуру подчинения сотрудника."""
        indent = "  " * level
        m_name = self.manager.name if self.manager else "Никто (Топ-менеджер)"
        print(f"{indent}👤 {self.name} [{self.position}]")
        print(f"{indent}   Отдел: {self.department}, Зарплата: {self.salary}")
        print(f"{indent}   Подчиняется: {m_name}")

        if self._subordinates:
            print(f"{indent}   Подчиненные ({len(self._subordinates)}):")
            for sub in self._subordinates:
                sub.show_details(level + 2)

    def __str__(self) -> str:
        """Возвращает краткую информацию о сотруднике в виде строки."""
        return f"{self.name} ({self.position})"


if __name__ == "__main__":
    print("--- Формирование структуры IT-компании ---\n")

    main_ceo = Employee("Иван Иванов", "Управление", "Генеральный директор", 500000)
    tech_cto = Employee("Сергей Петров", "IT", "Технический директор", 350000)
    hr_director = Employee("Анна Сидорова", "HR", "Глава HR", 200000)

    main_ceo.add_subordinate(tech_cto)
    main_ceo.add_subordinate(hr_director)

    lead = Employee("Алексей Сорокин", "IT", "Team Lead", 250000)
    junior = Employee("Дмитрий Лукин", "IT", "Junior Developer", 80000)
    hr_recruiter = Employee("Елена Кравц", "HR", "Рекрутер", 90000)

    tech_cto.add_subordinate(lead)
    lead.add_subordinate(junior)
    hr_director.add_subordinate(hr_recruiter)

    print("\n--- Полная иерархия компании ---")
    main_ceo.show_details()

    print("\n--- Проверка удаления из структуры ---")
    lead.remove_subordinate(junior)

    print("\n--- Иерархия отдела IT после изменений ---")
    tech_cto.show_details()
