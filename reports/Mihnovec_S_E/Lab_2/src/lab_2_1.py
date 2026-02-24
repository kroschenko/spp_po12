"""
Модуль для работы с классами для демонстрации обобщения, агрегации и ассоциации.
В Python обобщение реализуется через наследование, ассоциация и агрегация — через
хранение ссылок на другие объекты, а реализация — через интерфейсы.
В системе реализованы роли Преподавателя, Студента и сущности Курса и Архива.
"""

from abc import ABC, abstractmethod


class BaseUser(ABC):
    """
    Абстрактный класс (Интерфейс), демонстрирующий 'Реализацию'.
    """

    @abstractmethod
    def get_role(self):
        """Возвращает роль пользователя."""

    @abstractmethod
    def get_name(self):
        """Возвращает имя пользователя."""


class User(BaseUser):
    """Базовый класс для всех пользователей системы (Обобщение)."""

    def __init__(self, name: str):
        """Инициализация пользователя."""
        self.name = name

    def get_role(self):
        """Реализация метода получения роли."""
        return "Пользователь"

    def get_name(self):
        """Реализация метода получения имени."""
        return self.name

    def __str__(self):
        return f"{self.get_role()}: {self.name}"


class Teacher(User):
    """Преподаватель, который ведет курсы и выставляет оценки."""

    def get_role(self):
        """Переопределение роли."""
        return "Преподаватель"

    def announce_course(self, title: str):
        """Преподаватель создает (объявляет) курс."""
        print(f"Преподаватель {self.name} открыл запись на курс '{title}'.")
        return Course(title, self)

    def set_grade(self, student, course, value: int, archive):
        """Преподаватель выставляет оценку и отправляет её в архив."""
        msg = (
            f"Преподаватель {self.name} выставил оценку {value} "
            f"студенту {student.name} за курс '{course.title}'."
        )
        print(msg)
        archive.save_record(student, course, value)


class Student(User):
    """Студент, который записывается на курсы и обучается."""

    def get_role(self):
        """Переопределение роли."""
        return "Студент"

    def enroll(self, course):
        """Студент записывается на курс."""
        course.add_student(self)
        print(f"Студент {self.name} записался на курс '{course.title}'.")

    def study(self):
        """Процесс обучения."""
        print(f"Студент {self.name} активно изучает материалы курса...")


class Course:
    """Курс, который связывает преподавателя и студентов (Ассоциация)."""

    def __init__(self, title: str, teacher: Teacher):
        """Инициализация курса."""
        self.title = title
        self.teacher = teacher
        self.students = []

    def add_student(self, student: Student):
        """Добавление студента в список курса (Агрегация)."""
        if student not in self.students:
            self.students.append(student)

    def get_student_count(self):
        """Возвращает количество записанных студентов."""
        return len(self.students)


class Archive:
    """Класс-хранилище для результатов обучения."""

    def __init__(self):
        """Инициализация списка истории."""
        self.history = []

    def save_record(self, student, course, grade):
        """Сохранение записи в архив."""
        record = {
            "student": student.get_name(),
            "course": course.title,
            "grade": grade
        }
        self.history.append(record)

    def show_all(self):
        """Вывод всех записей архива."""
        print("\n--- СОДЕРЖИМОЕ АРХИВА ---")
        for entry in self.history:
            output = (
                f"Студент: {entry['student']} | "
                f"Курс: {entry['course']} | "
                f"Оценка: {entry['grade']}"
            )
            print(output)


def main():
    """Основная функция программы."""
    prof = Teacher("Крощенко А. А.")
    archive = Archive()

    python_course = prof.announce_course("Основы Python")

    vodim = Student("Вадим")
    bob = Student("Боб")

    vodim.enroll(python_course)
    bob.enroll(python_course)

    vodim.study()
    bob.study()

    prof.set_grade(vodim, python_course, 5, archive)
    prof.set_grade(bob, python_course, 4, archive)

    count = python_course.get_student_count()
    print(f"Всего студентов на курсе: {count}")
    archive.show_all()


if __name__ == "__main__":
    main()
