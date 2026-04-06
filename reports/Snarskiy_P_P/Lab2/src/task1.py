"""
Make class of triangle
"""

import math


class Triangle:
    """Class Triangle"""

    def __init__(self, a=5, b=5, c=5):
        self.a = a
        self.b = b
        self.c = c
        self.perimeter = self.a + self.b + self.c
        self.area = math.sqrt(
            self.perimeter
            / 2
            * (self.perimeter / 2 - self.a)
            * (self.perimeter / 2 - self.b)
            * (self.perimeter / 2 - self.c)
        )
        self.is_exist = (self.perimeter - max(a, b, c)) > max(a, b, c)
        self.is_equilateral = a == b == c

    def __eq__(self, other):
        sides1 = sorted([self.a, self.b, self.c])
        sides2 = sorted([other.a, other.b, other.c])
        return sides1 == sides2

    def __str__(self):
        return (
            f"Sides: {self.a}, {self.b}, {self.c}\nExists?: {self.is_exist}\n"
            f"Perimeter: {self.perimeter}\n"
            f"Area: {self.area}\n Equilateral?: {self.is_equilateral}\n"
        )


def main():
    """Main function"""
    triangle_1 = Triangle(
        int(input("Enter side a ")),
        int(input("Enter side b ")),
        int(input("Enter side c ")),
    )
    triangle_2 = Triangle(
        int(input("Enter side a ")),
        int(input("Enter side b ")),
        int(input("Enter side c ")),
    )
    print(triangle_1)
    print(triangle_2)
    print(triangle_1 == triangle_2)


main()
