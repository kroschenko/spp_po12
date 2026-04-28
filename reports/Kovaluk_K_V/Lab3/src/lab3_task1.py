class Teacher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.students = []
            cls._instance.name = "Преподаватель Иванов"
        return cls._instance

    def add_student(self, student):
        self.students.append(student)
        print(f"{student.name} добавлен в группу")

    def check_laboratory_work(self, student, lab_name):
        if student in self.students:
            print(f"{self.name}: Проверил лабораторную работу '{lab_name}' у {student.name}")
            student.lab_results[lab_name] = "Проверено"
        else:
            print(f"Студент {student.name} не числится в группе")

    def conduct_consultation(self, topic):
        print(f"{self.name}: Провёл консультацию по теме '{topic}'")
        for student in self.students:
            print(f"  - {student.name} присутствовал на консультации")

    def take_exam(self, student, exam_name):
        if student in self.students:
            print(f"{self.name}: Принял экзамен '{exam_name}' у {student.name}")
        else:
            print(f"Студент {student.name} не числится в группе")

    def set_grade(self, student, subject, grade):
        if student in self.students:
            student.grades[subject] = grade
            print(f"{self.name}: Выставил отметку {grade} студенту {student.name} по предмету '{subject}'")
        else:
            print(f"Студент {student.name} не числится в группе")

    def conduct_lecture(self, topic):
        print(f"{self.name}: Провёл лекцию на тему '{topic}'")
        for student in self.students:
            print(f"  - {student.name} прослушал лекцию")


class Student:
    def __init__(self, name):
        self.name = name
        self.grades = {}
        self.lab_results = {}


if __name__ == "__main__":
    teacher1 = Teacher()
    teacher2 = Teacher()

    print(f"teacher1 is teacher2: {teacher1 is teacher2}")
    print(f"Имя преподавателя: {teacher1.name}")

    student1 = Student("Анна Петрова")
    student2 = Student("Иван Сидоров")
    student3 = Student("Мария Иванова")

    teacher1.add_student(student1)
    teacher1.add_student(student2)
    teacher1.add_student(student3)

    print("\n--- Проведение лекции ---")
    teacher1.conduct_lecture("Основы программирования")

    print("\n--- Проверка лабораторных работ ---")
    teacher1.check_laboratory_work(student1, "Лабораторная работа №1")
    teacher1.check_laboratory_work(student2, "Лабораторная работа №2")

    print("\n--- Консультация ---")
    teacher1.conduct_consultation("Паттерны проектирования")

    print("\n--- Приём экзамена ---")
    teacher1.take_exam(student1, "Экзамен по Python")
    teacher1.take_exam(student3, "Экзамен по Python")

    print("\n--- Выставление оценок ---")
    teacher1.set_grade(student1, "Программирование", 5)
    teacher1.set_grade(student2, "Программирование", 4)
    teacher1.set_grade(student3, "Программирование", 5)

    print("\n--- Итоговые данные студентов ---")
    for student in [student1, student2, student3]:
        print(f"Студент: {student.name}, Оценки: {student.grades}")
