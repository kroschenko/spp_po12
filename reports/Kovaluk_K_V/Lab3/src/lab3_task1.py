class Teacher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.students = []
            cls._instance.name = "Преподаватель Иванов"
        return cls._instance

    def add_student(self, std):
        self.students.append(std)
        print(f"{std.name} добавлен в группу")

    def check_laboratory_work(self, std, lab_name):
        if std in self.students:
            print(f"{self.name}: Проверил лабораторную работу '{lab_name}' у {std.name}")
            std.lab_results[lab_name] = "Проверено"
        else:
            print(f"Студент {std.name} не числится в группе")

    def conduct_consultation(self, topic):
        print(f"{self.name}: Провёл консультацию по теме '{topic}'")
        for std in self.students:
            print(f"  - {std.name} присутствовал на консультации")

    def take_exam(self, std, exam_name):
        if std in self.students:
            print(f"{self.name}: Принял экзамен '{exam_name}' у {std.name}")
        else:
            print(f"Студент {std.name} не числится в группе")

    def set_grade(self, std, subject, grade):
        if std in self.students:
            std.grades[subject] = grade
            print(f"{self.name}: Выставил отметку {grade} студенту {std.name} по предмету '{subject}'")
        else:
            print(f"Студент {std.name} не числится в группе")

    def conduct_lecture(self, topic):
        print(f"{self.name}: Провёл лекцию на тему '{topic}'")
        for std in self.students:
            print(f"  - {std.name} прослушал лекцию")


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
    for std in [student1, student2, student3]:
        print(f"Студент: {std.name}, Оценки: {std.grades}")
