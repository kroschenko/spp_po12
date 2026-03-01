# test_rectangle.py
from rectangle import Rectangle

def test_rectangle():
    print("=== Тест 1: создание ===")
    r = Rectangle(4, 6)
    print(r)

    print("\n=== Тест 2: площадь ===")
    print("Ожидаем 24, получили:", r.area())

    print("\n=== Тест 3: периметр ===")
    print("Ожидаем 20, получили:", r.perimeter())

    print("\n=== Тест 4: квадрат ===")
    print("Ожидаем False, получили:", r.is_square())

    print("\n=== Тест 5: существование ===")
    print("Ожидаем True, получили:", r.exists())

    print("\n=== Тест 6: сравнение ===")
    r2 = Rectangle(6, 4)
    print("r == r2 (ожидаем True):", r == r2)

    r3 = Rectangle(4, 6)
    print("r == r3 (ожидаем True):", r == r3)

    r4 = Rectangle(5, 5)
    print("r == r4 (ожидаем False):", r == r4)

    print("\n=== Тест 7: строковое представление ===")
    print(str(r))

    print("\n=== Тест 8: проверка ошибок ===")
    try:
        Rectangle(-1, 5)
    except ValueError as e:
        print("Ошибка (ожидаемо):", e)

    try:
        r.a = -3
    except ValueError as e:
        print("Ошибка при изменении стороны:", e)

if __name__ == "__main__":
    test_rectangle()
