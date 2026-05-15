import math


class EquilateralTriangle:

    def __init__(self, a: float, b: float, c: float):

        self.a = a
        self.b = b
        self.c = c

    def exists(self) -> bool:

        return self.a == self.b == self.c

    def perimeter(self) -> float:

        return self.a + self.b + self.c

    def area(self) -> float | None:

        if not self.exists():
            return None
        return (math.sqrt(3) / 4) * self.a**2

    def __str__(self) -> str:

        return f"Треугольник: a={self.a}, b={self.b}, c={self.c}"

    def __eq__(self, other) -> bool:

        if not isinstance(other, EquilateralTriangle):
            return False
        return self.a == other.a and self.b == other.b and self.c == other.c


def main():

    a = float(input("Введите сторону a: "))
    b = float(input("Введите сторону b: "))
    c = float(input("Введите сторону c: "))

    triangle = EquilateralTriangle(a, b, c)

    print(triangle)

    if triangle.exists():
        print("Треугольник равносторонний и существует")
        print("Периметр:", triangle.perimeter())
        print("Площадь:", triangle.area())
    else:
        print("Это не равносторонний треугольник")


if __name__ == "__main__":
    main()
