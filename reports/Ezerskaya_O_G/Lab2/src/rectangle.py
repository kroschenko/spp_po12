"""Модуль для работы с прямоугольниками."""


class Rectangle:
    """Класс, представляющий прямоугольник."""

    def __init__(self, side_a, side_b=None):
        """Инициализация прямоугольника."""
        if side_b is None:
            side_b = side_a
        self._side_a = side_a
        self._side_b = side_b

    @property
    def side_a(self):
        """Геттер для стороны A."""
        return self._side_a

    @side_a.setter
    def side_a(self, value):
        """Сеттер для стороны A."""
        self._side_a = value

    @property
    def side_b(self):
        """Геттер для стороны B."""
        return self._side_b

    @side_b.setter
    def side_b(self, value):
        """Сеттер для стороны B."""
        self._side_b = value

    def area(self):
        """Вычисление площади."""
        return self._side_a * self._side_b

    def perimeter(self):
        """Вычисление периметра."""
        return 2 * (self._side_a + self._side_b)

    def is_square(self):
        """Проверка, является ли квадратом."""
        return self._side_a == self._side_b

    def is_valid(self):
        """Проверка существования прямоугольника."""
        return self._side_a > 0 and self._side_b > 0

    def __str__(self):
        """Строковое представление."""
        return f"Прямоугольник {self._side_a} x {self._side_b}"

    def __eq__(self, other):
        """Сравнение прямоугольников."""
        if not isinstance(other, Rectangle):
            return False
        return (self._side_a == other._side_a and self._side_b == other._side_b) or (
            self._side_a == other._side_b and self._side_b == other._side_a
        )


# Ввод данных с клавиатуры
print("Введите стороны прямоугольника:")
a = float(input("Сторона a: "))
b_input = input("Сторона b (если квадрат, нажмите Enter): ")
if b_input == "":
    rect = Rectangle(a)
else:
    rect = Rectangle(a, float(b_input))

print("\nРезультат:")
print(rect)
print(f"Площадь: {rect.area()}")
print(f"Периметр: {rect.perimeter()}")
print(f"Это квадрат? {rect.is_square()}")
print(f"Существует? {rect.is_valid()}")

print("\nИзменяем сторону a:")
rect.side_a = 10
print(f"Новая сторона a: {rect.side_a}")
print(f"Новая площадь: {rect.area()}")
