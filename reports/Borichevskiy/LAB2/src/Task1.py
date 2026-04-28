import math


class EquilateralTriangle:
    """Класс равностороннего треугольника."""

    def __init__(self, side: float):
        self.side = side

    @property
    def side(self) -> float:
        return self._side

    @side.setter
    def side(self, value: float):
        if value <= 0:
            raise ValueError("Сторона должна быть положительной")
        self._side = value

    def perimeter(self) -> float:
        return 3 * self._side

    def area(self) -> float:
        return (math.sqrt(3) / 4) * self._side**2

    def __eq__(self, other) -> bool:
        if not isinstance(other, EquilateralTriangle):
            return NotImplemented
        return math.isclose(self.area(), other.area())

    def __str__(self) -> str:
        return f"Равносторонний треугольник (сторона={self._side})"


if __name__ == "__main__":
    t1 = EquilateralTriangle(5)
    t2 = EquilateralTriangle(10)

    print(t1)
    print(f"Площадь: {t1.area():.2f}")
    print(f"Периметр: {t1.perimeter():.2f}")

    print("\nСравнение:")
    print("t1 == t2:", t1 == t2)
