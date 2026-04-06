"""
Модуль для лабораторной работы №3.
Вариант 7: Взаимодействие преподавателя и студентов.
"""

# pylint: disable=too-few-public-methods


class Student:
    """Базовый класс для представления студента."""

    def __init__(self, name):
        """Инициализация студента."""
        self.name = name

    def get_type(self):
        """Возвращает тип обучения."""
        return "Не определен"


class FullTimeStudent(Student):
    """Класс студента очного отделения."""

    def get_type(self):
        """Возвращает тип обучения."""
        return "Очник"


class PartTimeStudent(Student):
    """Класс студента заочного отделения."""

    def get_type(self):
        """Возвращает тип обучения."""
        return "Заочник"


class Teacher:
    """Класс преподавателя для взаимодействия со студентами."""

    def check_lab(self, student):
        """Проверяет лабораторную работу студента."""
        print(
            f"\n[!] Преподаватель проверил ЛР у {student.name} ({student.get_type()})"
        )

    def consult(self, student):
        """Проводит консультацию для студента."""
        print(f"\n[!] Проведена консультация для {student.name}")

    def take_exam(self, student):
        """Принимает экзамен у студента."""
        print(f"\n[!] Экзамен у {student.name} принят. Оценка выставлена.")


def main():
    """Основная функция программы с меню."""
    teacher = Teacher()
    students = []

    while True:
        print("\n--- МЕНЮ: ПРЕПОДАВАТЕЛЬ ---")
        print("1. Добавить студента-очника")
        print("2. Добавить студента-заочника")
        print("3. Проверить ЛР у всех")
        print("4. Провести консультацию")
        print("5. Принять экзамен (у последнего добавочного)")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите имя студента: ")
            students.append(FullTimeStudent(name))
        elif choice == "2":
            name = input("Введите имя студента: ")
            students.append(PartTimeStudent(name))
        elif choice == "3":
            for student in students:
                teacher.check_lab(student)
        elif choice == "4":
            if students:
                teacher.consult(students[-1])
        elif choice == "5":
            if students:
                teacher.take_exam(students.pop())
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
