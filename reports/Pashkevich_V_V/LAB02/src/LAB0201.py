class Rectangle:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Длина стороны должна быть числом")
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Длина стороны должна быть числом")
        self._b = value

    def exists(self) -> bool:
        return self.a > 0 and self.b > 0

    def area(self):
        if self.exists():
            return self.a * self.b
        return 0

    def perimeter(self):
        if self.exists():
            return 2 * (self.a + self.b)
        return 0

    def is_square(self) -> bool:
        return self.exists() and self.a == self.b

    def __str__(self):
        if self.exists():
            return (f"Прямоугольник со сторонами {self.a} и {self.b}. "
                    f"Площадь: {self.area()}, Периметр: {self.perimeter()}, "
                    f"Квадрат: {'да' if self.is_square() else 'нет'}")
        return f"Прямоугольник со сторонами {self.a} и {self.b} не существует"

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return False
        return self.a == other.a and self.b == other.b


# Пример использования
r1 = Rectangle(5, 10)
r2 = Rectangle(5, 10)
r3 = Rectangle(7, 7)
r4 = Rectangle(-2, 4)

print(r1)
print(r3)
print(r4)

print("r1 == r2:", r1 == r2)
print("r1 == r3:", r1 == r3)
print("Площадь r1:", r1.area())
print("Периметр r1:", r1.perimeter())
print("r3 является квадратом:", r3.is_square())
print("r4 существует:", r4.exists())
