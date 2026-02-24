"""
Модуль тестирования функционала класса Triangle из lab_2.
"""

import unittest
from reports.Mihnovec_S_E.Lab_2.src.lab_2 import Triangle


class TestTriangle(unittest.TestCase):
    """Тесты для проверки логики равнобедренного треугольника."""

    def setUp(self):
        """Инициализация объектов для тестов."""
        self.valid_tri = Triangle(5, 6)
        self.invalid_tri = Triangle(2, 10)
        self.negative_tri = Triangle(-1, 5)

    def test_existence(self):
        """Проверка метода is_exists."""
        self.assertTrue(self.valid_tri.is_exists())
        self.assertFalse(self.invalid_tri.is_exists())
        self.assertFalse(self.negative_tri.is_exists())

    def test_perimeter(self):
        """Проверка расчета периметра."""
        # 5 + 5 + 6 = 16
        self.assertEqual(self.valid_tri.calc_perimetr(), 16)

    def test_square(self):
        """Проверка расчета площади."""
        # Высота h = sqrt(5^2 - 3^2) = 4. Площадь = 0.5 * 6 * 4 = 12
        self.assertAlmostEqual(self.valid_tri.calc_square(), 12.0)
        # Для несуществующего должна возвращать 0.0
        self.assertEqual(self.invalid_tri.calc_square(), 0.0)

    def test_equality(self):
        """Проверка метода сравнения __eq__."""
        same_tri = Triangle(5, 6)
        diff_tri = Triangle(10, 6)
        self.assertEqual(self.valid_tri, same_tri)
        self.assertNotEqual(self.valid_tri, diff_tri)
        self.assertNotEqual(self.valid_tri, "Not a triangle")


if __name__ == "__main__":
    unittest.main()