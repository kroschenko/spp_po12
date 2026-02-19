import math


class IsoscelesTriangle:
    def __init__(self, equal_side: float = 1, base: float = 1):
        self.equal_side = equal_side
        self.base = base

    @property
    def equal_side(self):
        return self._equal_side

    @equal_side.setter
    def equal_side(self, value):
        if value <= 0:
            raise ValueError("Длина стороны должна быть положительной")
        self._equal_side = value

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        if value <= 0:
            raise ValueError("Длина основания должна быть положительной")
        self._base = value

    def exists(self) -> bool:
        return 2 * self.equal_side > self.base

    def perimeter(self) -> float:
        if not self.exists():
            raise ValueError("Треугольник не существует")
        return 2 * self.equal_side + self.base

    def area(self) -> float:
        if not self.exists():
            raise ValueError("Треугольник не существует")
        height = math.sqrt(self.equal_side**2 - (self.base / 2) ** 2)
        return 0.5 * self.base * height

    def __str__(self):
        return f"Равнобедренный треугольник: " f"боковая сторона = {self.equal_side}, " f"основание = {self.base}"

    def __eq__(self, other):
        if not isinstance(other, IsoscelesTriangle):
            return NotImplemented
        return self.equal_side == other.equal_side and self.base == other.base


t1 = IsoscelesTriangle(5, 6)
t2 = IsoscelesTriangle(5, 6)

print(t1)
print("Существует:", t1.exists())
print("Периметр:", t1.perimeter())
print("Площадь:", t1.area())
print("Треугольники равны:", t1 == t2)
