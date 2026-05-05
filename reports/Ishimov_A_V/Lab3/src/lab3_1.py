from abc import ABC, abstractmethod


class Student(ABC):

    def __init__(self, name):
        self.name = name
        self.grade = None

    @abstractmethod
    def study(self):
        pass


class BachelorStudent(Student):

    def study(self):
        print(f"Бакалавр {self.name} изучает базовый курс.")


class MasterStudent(Student):

    def study(self):
        print(f"Магистр {self.name} изучает углубленный курс.")


class StudentFactory:

    @staticmethod
    def create_student(student_type, name):
        if student_type == "1":
            return BachelorStudent(name)
        if student_type == "2":
            return MasterStudent(name)
        raise ValueError("Неизвестный тип студента")


class Teacher:

    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print("Студент добавлен")

    def check_lab(self, student):
        print(f"Преподаватель {self.name} проверяет лабораторную работу студента {student.name}")

    def consult(self, student):
        print(f"Преподаватель {self.name} проводит консультацию со студентом {student.name}")

    def exam(self, student):
        print(f"Преподаватель {self.name} принимает экзамен у студента {student.name}")

    def grade(self, student, grade):
        student.grade = grade
        print(f"Преподаватель {self.name} выставил оценку {grade} студенту {student.name}")

    def lecture(self):
        print(f"\nПреподаватель {self.name} проводит лекцию для студентов:")
        for student in self.students:
            print(f" - {student.name}")

    def show_students(self):
        if not self.students:
            print("Нет студентов")
            return

        print("\nСписок студентов:")
        for i, student in enumerate(self.students):
            print(f"{i + 1}. {student.name}")


def menu_add_student(teacher):
    print("1 - Бакалавр")
    print("2 - Магистр")
    student_type = input("Тип студента: ")
    name = input("Имя студента: ")

    student = StudentFactory.create_student(student_type, name)
    teacher.add_student(student)


def menu_student_action(teacher, choice):
    teacher.show_students()
    num = int(input("Выберите студента: ")) - 1

    if num < 0 or num >= len(teacher.students):
        print("Неверный выбор")
        return

    student = teacher.students[num]

    if choice == "3":
        teacher.check_lab(student)
    elif choice == "4":
        teacher.consult(student)
    elif choice == "5":
        teacher.exam(student)
    elif choice == "6":
        grade = input("Введите оценку: ")
        teacher.grade(student, grade)


def main():

    teacher = Teacher("Иванов")

    while True:
        print("\nМеню:")
        print("1. Добавить студента")
        print("2. Провести лекцию")
        print("3. Проверить лабораторную")
        print("4. Провести консультацию")
        print("5. Принять экзамен")
        print("6. Выставить оценку")
        print("7. Показать студентов")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            menu_add_student(teacher)

        elif choice == "2":
            teacher.lecture()

        elif choice in ["3", "4", "5", "6"]:
            menu_student_action(teacher, choice)

        elif choice == "7":
            teacher.show_students()

        elif choice == "0":
            break

        else:
            print("Неверный пункт меню")


if __name__ == "__main__":
    main()
