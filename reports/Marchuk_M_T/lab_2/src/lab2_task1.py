"""
Модуль для работы с объектом Равнобедренный треугольник.
"""
import math


class IsoscelesTriangle:
    """Класс для представления равнобедренного треугольника."""

    def __init__(self, base, side):
        """Инициализация сторон."""
        self._base = float(base)
        self._side = float(side)

    @property
    def base(self):
        """Возвращает основание."""
        return self._base

    @base.setter
    def base(self, value):
        """Устанавливает основание с проверкой."""
        if value <= 0:
            raise ValueError("Сторона должна быть положительной")
        self._base = value

    @property
    def side(self):
        """Возвращает боковую сторону."""
        return self._side

    @side.setter
    def side(self, value):
        """Устанавливает боковую сторону с проверкой."""
        if value <= 0:
            raise ValueError("Сторона должна быть положительной")
        self._side = value

    def is_exists(self):
        """Проверка существования треугольника."""
        return 2 * self._side > self._base > 0 and self._side > 0

    def get_perimeter(self):
        """Расчет периметра."""
        if not self.is_exists():
            return 0.0
        return self._base + 2 * self._side

    def get_area(self):
        """Расчет площади."""
        if not self.is_exists():
            return 0.0
        # h = sqrt(side^2 - (base/2)**2)
        height = math.sqrt(self._side**2 - (self._base / 2) ** 2)
        return 0.5 * self._base * height

    def __str__(self):
        """Строковое представление."""
        if self.is_exists():
            return f"Треугольник (осн={self._base}, бок={self._side})"
        return "Треугольник не существует"

    def __eq__(self, other):
        """Сравнение двух объектов."""
        if not isinstance(other, IsoscelesTriangle):
            return False
        return self._base == other.base and self._side == other.side


def main():
    """Точка входа."""
    try:
        tri = IsoscelesTriangle(10, 13)
        print(tri)
        print(f"Периметр: {tri.get_perimeter()}")
        print(f"Площадь: {tri.get_area():.2f}")
    except ValueError as err:
        print(f"Ошибка: {err}")


if __name__ == "__main__":
    main()
