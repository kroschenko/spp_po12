"""
Система 'Факультатив'. Демонстрация связей ООП.
"""


class Course:
    """Класс учебного курса."""

    def __init__(self, title):
        """Инициализация курса."""
        self.title = title
        self.students = []

    def __str__(self):
        """Название курса."""
        return f"Курс: {self.title}"


class Student:
    """Класс студента."""

    def __init__(self, name):
        """Имя студента."""
        self.name = name

    def __str__(self):
        """Представление студента."""
        return f"Студент: {self.name}"


class Teacher:
    """Класс преподавателя."""

    def __init__(self, name):
        """Имя преподавателя."""
        self.name = name

    def announce_course(self, title):
        """Объявляет о начале записи на курс."""
        print(f"Преподаватель {self.name} открыл курс '{title}'")
        return Course(title)

    def set_grade(self, student, course, value, archive_obj):
        """Выставляет оценку в архив."""
        print(f"Преподаватель {self.name} оценил {student.name} на {value}")
        archive_obj.save_record(student.name, course.title, value)


class Archive:
    """Класс для хранения истории оценок."""

    def __init__(self):
        """Инициализация списка записей."""
        self.records = []

    def save_record(self, student_name, course_title, grade):
        """Сохранение записи в список."""
        self.records.append({
            "student": student_name,
            "course": course_title,
            "grade": grade
        })

    def show_all(self):
        """Вывод всех записей."""
        print("\n--- АРХИВ ОЦЕНОК ---")
        for record in self.records:
            print(f"{record['student']} | {record['course']} | {record['grade']}")


def main():
    """Основная логика системы."""
    archive = Archive()
    teacher = Teacher("Иванов И.И.")
    student = Student("Марчук М.Т.")
    course = teacher.announce_course("Python")

    teacher.set_grade(student, course, "10", archive)
    archive.show_all()


if __name__ == "__main__":
    main()
