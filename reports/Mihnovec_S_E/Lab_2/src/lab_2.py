"""
Модуль для работы с равнобедренными треугольниками.
Предоставляет расчет площади, периметра и проверку существования.
"""

import math


class Triangle:
    """
    Класс, представляющий равнобедренный треугольник.
    """

    def __init__(self, side, base):
        """Инициализация сторон треугольника."""
        self.side = side
        self.base = base

    def is_exists(self):
        """Проверяет, существует ли треугольник с данными сторонами."""
        return self.side > 0 and self.base > 0 and (2 * self.side > self.base)

    def calc_square(self):
        """Вычисляет площадь треугольника через высоту."""
        if not self.is_exists():
            return 0.0
        height = math.sqrt(self.side**2 - (self.base / 2) ** 2)
        area = (self.base * height) / 2
        return area

    def calc_perimetr(self):
        """Вычисляет периметр треугольника."""
        return self.side * 2 + self.base

    def __eq__(self, other):
        """Сравнивает два треугольника по их сторонам."""
        if not isinstance(other, Triangle):
            return False
        return self.side == other.side and self.base == other.base


def main():
    """Демонстрация работы класса Triangle."""
    tri1 = Triangle(5, 6)
    tri2 = Triangle(5, 6)
    tri3 = Triangle(10, 6)
    tri4 = Triangle(-1, 6)

    print(f"Треугольник 5, 5, 6 существует? {tri1.is_exists()}")
    print(f"Треугольник 10, 10, 6 существует? {tri3.is_exists()}")
    print(f"Треугольник -1, -1, 6 существует? {tri4.is_exists()}")
    print(f"Треугольник tri1 и tri2 равны? {tri1 == tri2}")
    print(f"Треугольник tri1 - периметр: {tri1.calc_perimetr()}")
    print(f"Треугольник tri1 - площадь: {tri1.calc_square()}")


if __name__ == "__main__":
    main()
