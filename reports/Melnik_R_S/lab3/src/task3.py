# pylint: disable=invalid-name, too-many-arguments, too-many-positional-arguments, too-few-public-methods
"""
Модуль для расчета зарплаты сотрудников IT-компании.
Реализует формирование отчета через паттерн Посетитель.
"""

from typing import List, Dict


class Employee:
    """Класс, представляющий сотрудника как элемент для посещения."""

    def __init__(self, name: str, dept: str, pos: str, sal: float, level: int):
        """Инициализация данных сотрудника и его уровня в иерархии."""
        self.name: str = name
        self.department: str = dept
        self.position: str = pos
        self.salary: float = sal
        self.level: int = level
        self.subordinates: List["Employee"] = []

    def add_subordinate(self, emp: "Employee") -> None:
        """Добавляет сотрудника в список подчиненных."""
        self.subordinates.append(emp)

    def accept(self, visitor: "CompanyVisitor") -> None:
        """Принимает посетителя и передает его подчиненным."""
        visitor.visit_employee(self)
        for sub in self.subordinates:
            sub.accept(visitor)


class CompanyVisitor:
    """Абстрактный базовый класс для посетителей компании."""

    def visit_employee(self, employee: Employee) -> None:
        """Метод для обработки данных конкретного сотрудника."""
        raise NotImplementedError


class SalaryReportVisitor(CompanyVisitor):
    """Посетитель для генерации иерархического отчета по зарплате."""

    def __init__(self):
        """Инициализация хранилища данных по отделам."""
        super().__init__()
        self.data: Dict[str, List[Employee]] = {}

    def visit_employee(self, employee: Employee) -> None:
        """Собирает сотрудников в группы по их отделам."""
        if employee.department not in self.data:
            self.data[employee.department] = []
        self.data[employee.department].append(employee)

    def print_report(self) -> None:
        """Выводит отчет, отсортированный по отделам и старшинству."""
        header = (
            f"{'ОТДЕЛ':<15} | {'СТАТУС':<5} | {'ДОЛЖНОСТЬ':<20} | "
            f"{'ФИО':<18} | {'ЗАРПЛАТА':<10}"
        )
        print(header)
        print("-" * 80)

        total_company_salary = 0.0

        for dept in sorted(self.data.keys()):
            # Сортировка по уровню (старшинству)
            employees = sorted(self.data[dept], key=lambda x: x.level)
            dept_total = 0.0

            for emp in employees:
                print(
                    f"{emp.department:<15} | Lvl {emp.level} | "
                    f"{emp.position:<20} | {emp.name:<18} | {emp.salary:<10.2f}"
                )
                dept_total += emp.salary

            print(f"{' ' * 45} Итого по отделу {dept}: {dept_total:.2f} руб.")
            print("-" * 80)
            total_company_salary += dept_total

        print(f"ОБЩИЙ ФОНД ОПЛАТЫ ТРУДА КОМПАНИИ: {total_company_salary:.2f} руб.")


if __name__ == "__main__":
    # Инициализация структуры
    top_ceo = Employee("Иван Иванов", "Управление", "Ген. директор", 500000, 0)

    tech_dir = Employee("Сергей Петров", "IT", "Тех. директор", 350000, 1)
    hr_dir = Employee("Анна Сидорова", "HR", "Глава HR", 200000, 1)

    lead_dev = Employee("Алексей Сорокин", "IT", "Team Lead", 250000, 2)
    junior_dev = Employee("Дмитрий Лукин", "IT", "Junior Dev", 80000, 3)
    recruiter = Employee("Елена Кравц", "HR", "Рекрутер", 90000, 2)

    # Построение дерева
    top_ceo.add_subordinate(tech_dir)
    top_ceo.add_subordinate(hr_dir)
    tech_dir.add_subordinate(lead_dev)
    lead_dev.add_subordinate(junior_dev)
    hr_dir.add_subordinate(recruiter)

    # Генерация отчета
    salary_visitor = SalaryReportVisitor()
    print("Генерация отчета по зарплате...\n")
    top_ceo.accept(salary_visitor)
    salary_visitor.print_report()
