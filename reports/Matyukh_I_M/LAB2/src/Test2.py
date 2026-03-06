class Person:

    def __init__(self, name: str):
        self.name = name


class Student(Person):

    def __init__(self, name: str):
        super().__init__(name)
        self.courses = []

    def enroll(self, course):

        self.courses.append(course)
        course.students.append(self)
        print(f"{self.name} записался на курс {course.title}")


class Teacher(Person):

    def grade_student(self, student, course, grade, archive):

        archive.add_record(student, course, grade)


class Course:

    def __init__(self, title: str, teacher: Teacher):
        self.title = title
        self.teacher = teacher
        self.students = []


class Archive:

    def __init__(self):
        self.records = []

    def add_record(self, student, course, grade):
        """Добавление записи об оценке."""
        self.records.append((student.name, course.title, grade))

    def show(self):
        """Показать архив оценок."""
        print("\nАрхив оценок:")
        for student_name, course_title, grade in self.records:
            print(f"Студент: {student_name} | Курс: {course_title} | Оценка: {grade}")


def main():

    archive = Archive()

    teacher_name = input("Введите имя преподавателя: ")
    teacher = Teacher(teacher_name)

    course_name = input("Введите название курса: ")
    course = Course(course_name, teacher)

    count = int(input("Сколько студентов записывается на курс? "))

    students = []

    for _ in range(count):
        name = input("Введите имя студента: ")
        student = Student(name)
        student.enroll(course)
        students.append(student)

    print("\nВыставление оценок")

    for student in students:
        grade = int(input(f"Введите оценку для {student.name}: "))
        teacher.grade_student(student, course, grade, archive)

    archive.show()


if __name__ == "__main__":
    main()
