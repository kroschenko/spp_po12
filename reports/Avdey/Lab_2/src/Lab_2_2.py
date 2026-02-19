from abc import ABC, abstractmethod


class Grading(ABC):
    @abstractmethod
    def set_grade(self, student, course, grade):
        pass


class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name):
        super().__init__(name)
        self.courses = []

    def enroll(self, course):
        self.courses.append(course)
        course.add_student(self)

    def study(self):
        print(f"Студент {self.name} обучается")


class Teacher(Person, Grading):

    def announce_course(self, course):
        print(f"Преподаватель {self.name} объявил курс «{course.title}»")

    def set_grade(self, student, course, grade):
        Archive.save_grade(student, course, grade)
        print(
            f"Преподаватель {self.name} поставил студенту {student.name} " f"оценку {grade} по курсу «{course.title}»"
        )


class Course:
    def __init__(self, title):
        self.title = title
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print(f"Студент {student.name} записался на курс «{self.title}»")


class Archive:
    grades = []

    @classmethod
    def save_grade(cls, student, course, grade):
        cls.grades.append({"student": student.name, "course": course.title, "grade": grade})

    @classmethod
    def show_archive(cls):
        print("\nАрхив оценок:")
        for record in cls.grades:
            print(f"Студент: {record['student']}, " f"Курс: {record['course']}, " f"Оценка: {record['grade']}")


if __name__ == "__main__":

    teacher = Teacher("Иванов")

    student1 = Student("Алексей")
    student2 = Student("Мария")

    python_course = Course("Python")

    teacher.announce_course(python_course)

    student1.enroll(python_course)
    student2.enroll(python_course)

    student1.study()
    student2.study()

    teacher.set_grade(student1, python_course, 5)
    teacher.set_grade(student2, python_course, 4)

    Archive.show_archive()
