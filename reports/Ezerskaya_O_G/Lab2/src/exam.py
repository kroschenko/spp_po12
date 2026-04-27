"""Модуль для системы вступительных экзаменов."""

from abc import ABC, abstractmethod


class Person(ABC):
    """Абстрактный класс человека."""

    def __init__(self, name):
        """Инициализация человека."""
        self.name = name

    @abstractmethod
    def get_role(self):
        """Получить роль человека."""

    def get_name(self):
        """Получить имя."""
        return self.name


class Applicant(Person):
    """Класс абитуриента."""

    def __init__(self, name, faculty):
        """Инициализация абитуриента."""
        super().__init__(name)
        self.faculty = faculty
        self.grades = []
        self.avg_score = 0
        self.enrolled = False

    def get_role(self):
        """Получить роль."""
        return "Абитуриент"

    def add_grade(self, grade):
        """Добавить оценку."""
        self.grades.append(grade)
        self.avg_score = sum(self.grades) / len(self.grades)

    def get_avg_score(self):
        """Получить средний балл."""
        return self.avg_score


class Teacher(Person):
    """Класс преподавателя."""

    def get_role(self):
        """Получить роль."""
        return "Преподаватель"

    def set_grade(self, applicant, grade):
        """Выставить оценку."""
        applicant.add_grade(grade)
        print(f"{self.name} поставила {grade} {applicant.name}")


class Faculty:
    """Класс факультета."""

    def __init__(self, name, capacity):
        """Инициализация факультета."""
        self.name = name
        self.capacity = capacity
        self.applicants = []

    def add_applicant(self, applicant):
        """Добавить абитуриента."""
        self.applicants.append(applicant)

    def get_applicants(self):
        """Получить список абитуриентов."""
        return self.applicants


class AdmissionSystem:
    """Класс системы приема."""

    def __init__(self):
        """Инициализация системы."""
        self.faculties = []

    def add_faculty(self, faculty):
        """Добавить факультет."""
        self.faculties.append(faculty)

    def determine_enrolled(self):
        """Определить зачисленных."""
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ ЗАЧИСЛЕНИЯ")
        print("=" * 50)

        for faculty in self.faculties:
            print(f"\nФакультет: {faculty.name} (мест: {faculty.capacity})")
            faculty.applicants.sort(key=lambda x: x.get_avg_score(), reverse=True)

            for i, app in enumerate(faculty.applicants):
                name = app.get_name()
                score = app.get_avg_score()

                if i < faculty.capacity:
                    app.enrolled = True
                    print("✓ " + name + " - средний балл: " + f"{score:.1f} - ЗАЧИСЛЕН")
                else:
                    print("✗ " + name + " - средний балл: " + f"{score:.1f} - НЕ ЗАЧИСЛЕН")


def process_faculties():
    """Обработка ввода факультетов."""
    faculties = []
    f_count = int(input("\nСколько факультетов? "))
    for i in range(f_count):
        print(f"\nФакультет {i+1}:")
        name = input("Название: ")
        cap = int(input("Количество мест: "))
        faculties.append(Faculty(name, cap))
    return faculties


def process_applicants(faculties):
    """Обработка ввода абитуриентов."""
    applicants = []
    a_count = int(input("\nСколько абитуриентов? "))
    for i in range(a_count):
        print(f"\nАбитуриент {i+1}:")
        name = input("Имя: ")
        print("Выберите факультет:")
        for j, fac in enumerate(faculties):
            print(f"{j+1}. {fac.name}")
        faculty_choice = int(input("Номер: ")) - 1
        applicant = Applicant(name, faculties[faculty_choice])
        faculties[faculty_choice].add_applicant(applicant)
        applicants.append(applicant)
    return applicants


def process_exams(applicants, teachers):
    """Обработка проведения экзаменов."""
    print("\n" + "=" * 50)
    print("ЭКЗАМЕНЫ")
    print("=" * 50)
    for applicant in applicants:
        print(f"\n{applicant.get_name()}:")
        e_count = int(input("Сколько экзаменов? "))
        for _ in range(e_count):
            print("\n  Выберите преподавателя:")
            print(f"  1. {teachers[0].get_name()}")
            print(f"  2. {teachers[1].get_name()}")
            t_choice = int(input("  Номер (1 или 2): ")) - 1
            grade = float(input("  Оценка (2-5): "))
            teachers[t_choice].set_grade(applicant, grade)


def main():
    """Основная функция."""
    print("=" * 50)
    print("СИСТЕМА ВСТУПИТЕЛЬНЫХ ЭКЗАМЕНОВ")
    print("=" * 50)

    teachers = [Teacher("Марго Александровна"), Teacher("Вика Александровна")]
    print(f"\nПреподаватели: {teachers[0].get_name()} и {teachers[1].get_name()}")

    faculties = process_faculties()
    applicants = process_applicants(faculties)
    process_exams(applicants, teachers)

    system = AdmissionSystem()
    for faculty in faculties:
        system.add_faculty(faculty)
    system.determine_enrolled()


if __name__ == "__main__":
    main()
