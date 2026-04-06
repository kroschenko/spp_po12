"""Making Course system"""


class Course:
    """Course class"""

    def __init__(self, name, teacher):
        self.name = name
        self.students = []
        self.teacher = teacher

    def add_student(self, student):
        """Add a student to the class"""

        self.students.append(student)

    def conduct_course(self):
        """Conducting course"""

        print(f"\nCourse '{self.name}' started. Teacher: {self.teacher.name}")
        for student in self.students:
            print(f"{student.name} is studying...")


class Teacher:
    """Teacher class"""

    def __init__(self, name):
        self.name = name

    def assign_mark(self, student, course, value):
        """Assign mark to student"""

        mark = Mark(student, course, value)
        Archive.add_record(mark)
        print(
            f"{self.name} gave mark {mark.value} to {student.name} for course {course.name}"
        )

    def show_teacher(self):
        """Showing teacher"""

        print(f"\nTeacher {self.name} is teaching...")


class Student:
    """Student class"""

    def __init__(self, name):
        self.name = name
        self.courses = []

    def enroll(self, course):
        """Enroll student with course"""

        self.courses.append(course)
        course.add_student(self)
        print(f"{self.name} enrolled on {course.name}")

    def show_student(self):
        """Showing student"""
        print(f"\nStudent {self.name} is enrolled...")


class Mark:
    """Mark class"""

    def __init__(self, student, course, value):
        self.student = student
        self.course = course
        self.value = value

    def __str__(self):
        return f"{self.student.name} | {self.course.name} | {self.value}"

    def show_mark(self):
        """Showing mark"""
        print(self)


class Archive:
    """Archive class"""

    records = []

    @classmethod
    def add_record(cls, mark):
        """Adding record"""

        cls.records.append(mark)

    @classmethod
    def show_archive(cls):
        """Showing archive"""

        print("\n=== Archive ===")
        for mark in cls.records:
            print(mark)


def main():
    """Main function"""

    teacher1 = Teacher("Rogers")
    teacher2 = Teacher("Stark")

    course1 = Course("Course1", teacher1)
    course2 = Course("Course2", teacher2)

    s1 = Student("Bucky")
    s2 = Student("Sam")
    s3 = Student("Peter")

    s1.enroll(course1)
    s2.enroll(course1)
    s3.enroll(course2)

    course1.conduct_course()
    course2.conduct_course()

    teacher1.assign_mark(s1, course1, 9)
    teacher1.assign_mark(s2, course1, 10)
    teacher2.assign_mark(s3, course2, 10)

    Archive.show_archive()


main()
