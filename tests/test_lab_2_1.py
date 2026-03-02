"""
Модуль тестирования системы Факультатив из lab_2_1.
"""

import unittest
from reports.Mihnovec_S_E.Lab_2.src.lab_2_1 import Teacher, Student, Course, Archive


class TestFacultySystem(unittest.TestCase):
    """Тесты для проверки взаимодействия классов системы обучения."""

    def setUp(self):
        """Подготовка окружения для каждого теста."""
        self.teacher = Teacher("Тестов Т.Т.")
        self.student = Student("Иван")
        self.archive = Archive()
        self.course = self.teacher.announce_course("Python Test")

    def test_user_roles(self):
        """Проверка корректности ролей."""
        self.assertEqual(self.teacher.get_role(), "Преподаватель")
        self.assertEqual(self.student.get_role(), "Студент")

    def test_enrollment(self):
        """Проверка записи студента на курс."""
        self.student.enroll(self.course)
        self.assertEqual(self.course.get_student_count(), 1)
        self.assertIn(self.student, self.course.students)

    def test_grading_and_archive(self):
        """Проверка выставления оценок и сохранения в архив."""
        self.teacher.set_grade(self.student, self.course, 5, self.archive)
        
        # Проверяем, что в архиве появилась запись
        self.assertEqual(len(self.archive.history), 1)
        
        record = self.archive.history[0]
        self.assertEqual(record["student"], "Иван")
        self.assertEqual(record["course"], "Python Test")
        self.assertEqual(record["grade"], 5)

    def test_course_creation(self):
        """Проверка создания курса учителем."""
        new_course = self.teacher.announce_course("New Science")
        self.assertIsInstance(new_course, Course)
        self.assertEqual(new_course.teacher, self.teacher)


if __name__ == "__main__":
    unittest.main()