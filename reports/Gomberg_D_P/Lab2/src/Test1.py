import math


class RightTriangle:
    def __init__(self, a, b, c):
        self._a = float(a)
        self._b = float(b)
        self._c = float(c)

    # Свойства (Property) и сеттеры для сторон
    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = float(value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = float(value)

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = float(value)

    def is_exists(self):
        sides = sorted([self._a, self._b, self._c])
        # Проверка неравенства треугольника и теоремы Пифагора (с учетом погрешности float)
        if sides[0] > 0 and sides[0] + sides[1] > sides[2]:
            return math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2)
        return False

    def get_perimeter(self):
        if not self.is_exists():
            return "Треугольник не существует"
        return self._a + self._b + self._c

    def get_area(self):
        if not self.is_exists():
            return "Треугольник не существует"
        sides = sorted([self._a, self._b, self._c])
        return 0.5 * sides[0] * sides[1]

    def __str__(self):
        """Переопределение строкового представления"""
        status = "существует" if self.is_exists() else "не существует"
        return f"Прямоугольный треугольник со сторонами {self._a}, {self._b}, {self._c} ({status})"

    def __eq__(self, other):
        """Переопределение сравнения объектов (по равенству набора сторон)"""
        if not isinstance(other, RightTriangle):
            return False
        return sorted([self._a, self._b, self._c]) == sorted(
            [other.a, other.b, other.c]
        )


tri1 = RightTriangle(3, 4, 5)
tri2 = RightTriangle(5, 4, 3)
tri3 = RightTriangle(1, 1, 1)

print(tri1)  # __str__
print(f"Периметр: {tri1.get_perimeter()}")
print(f"Площадь: {tri1.get_area()}")
print(f"Равны ли tri1 и tri2? {tri1 == tri2}")  # __eq__
print(f"Существует ли tri3 (1,1,1)? {tri3.is_exists()}")
