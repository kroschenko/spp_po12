"""
Этот модуль содержит класс Rectangle для работы с геометрическими прямоугольниками.
"""


class Rectangle:
    """
    Класс, представляющий прямоугольник.
    """

    def __init__(self, length: float, width: float):
        """Инициализация прямоугольника длиной и шириной."""
        self.length = length
        self.width = width

    def perimeter(self) -> float:
        """Вычисляет периметр прямоугольника."""
        return (self.length + self.width) * 2

    def area(self) -> float:
        """Вычисляет площадь прямоугольника."""
        return self.length * self.width

    def is_rectangle(self) -> bool:
        """Проверяет, являются ли стороны положительными (валидный прямоугольник)."""
        return self.length >= 0 and self.width >= 0

    def is_square(self) -> bool:
        """Проверяет, является ли прямоугольник квадратом."""
        return self.length == self.width

    def __eq__(self, other: object) -> bool:
        """Сравнивает два прямоугольника по их размерам."""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.length == other.length and self.width == other.width


def main():
    """Основная функция для демонстрации работы класса."""
    rec1 = Rectangle(10, 5)
    print(f"Площадь rec1: {rec1.area()}")
    print(f"Периметр rec1: {rec1.perimeter()}")
    print(f"rec1 - это прямоугольник: {rec1.is_rectangle()}")
    print(f"rec1 - это квадрат: {rec1.is_square()}")

    rec2 = Rectangle(3, 5)
    print(f"rec1 == rec2: {rec1 == rec2}")


if __name__ == "__main__":
    main()
