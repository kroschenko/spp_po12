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
        for s in self.students:
            print(f"  - {s.name} присутствовал на консультации")

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
        for s in self.students:
            print(f"  - {s.name} прослушал лекцию")


class Student:
    def __init__(self, name):
        self.name = name
        self.grades = {}
        self.lab_results = {}


if __name__ == "__main__":
    t1 = Teacher()
    t2 = Teacher()

    print(f"teacher1 is teacher2: {t1 is t2}")
    print(f"Имя преподавателя: {t1.name}")

    s1 = Student("Анна Петрова")
    s2 = Student("Иван Сидоров")
    s3 = Student("Мария Иванова")

    t1.add_student(s1)
    t1.add_student(s2)
    t1.add_student(s3)

    print("\n--- Проведение лекции ---")
    t1.conduct_lecture("Основы программирования")

    print("\n--- Проверка лабораторных работ ---")
    t1.check_laboratory_work(s1, "Лабораторная работа №1")
    t1.check_laboratory_work(s2, "Лабораторная работа №2")

    print("\n--- Консультация ---")
    t1.conduct_consultation("Паттерны проектирования")

    print("\n--- Приём экзамена ---")
    t1.take_exam(s1, "Экзамен по Python")
    t1.take_exam(s3, "Экзамен по Python")

    print("\n--- Выставление оценок ---")
    t1.set_grade(s1, "Программирование", 5)
    t1.set_grade(s2, "Программирование", 4)
    t1.set_grade(s3, "Программирование", 5)

    print("\n--- Итоговые данные студентов ---")
    for s in [s1, s2, s3]:
        print(f"Студент: {s.name}, Оценки: {s.grades}")
