class Rectangle:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    # --- Свойства с проверкой ---

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value <= 0:
            raise ValueError("Сторона должна быть положительным числом")
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value <= 0:
            raise ValueError("Сторона должна быть положительным числом")
        self._b = value

    # --- Методы ---

    def area(self) -> float:
        return self.a * self.b

    def perimeter(self) -> float:
        return 2 * (self.a + self.b)

    def is_square(self) -> bool:
        return self.a == self.b

    def exists(self) -> bool:
        return self.a > 0 and self.b > 0

    # --- Магические методы ---

    def __str__(self):
        return f"Прямоугольник со сторонами {self.a} и {self.b}"

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return False
        return (self.a == other.a and self.b == other.b) or \
               (self.a == other.b and self.b == other.a)


# Пример использования
if __name__ == "__main__":
    r1 = Rectangle(5, 10)
    r2 = Rectangle(10, 5)

    print(r1)
    print("Площадь:", r1.area())
    print("Периметр:", r1.perimeter())
    print("Является квадратом:", r1.is_square())
    print("Существует:", r1.exists())
    print("Равны ли r1 и r2:", r1 == r2)
