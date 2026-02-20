import math


class EquilateralTriangle:
    """Класс равностороннего треугольника"""

    def __init__(self, side: float):
        """Конструктор с начальной инициализацией"""
        self._side = side

    @property
    def side(self) -> float:
        """Геттер для стороны"""
        return self._side

    @side.setter
    def side(self, value: float):
        """Сеттер для стороны с проверкой"""
        if value <= 0:
            raise ValueError("Сторона должна быть положительной")
        self._side = value

    def is_valid(self) -> bool:
        """Проверка существования треугольника"""
        return self._side > 0

    def perimeter(self) -> float:
        """Вычисление периметра"""
        if not self.is_valid():
            raise ValueError("Треугольник не существует")
        return 3 * self._side

    def area(self) -> float:
        """Вычисление площади"""
        if not self.is_valid():
            raise ValueError("Треугольник не существует")
        return (math.sqrt(3) / 4) * self._side**2

    def __str__(self) -> str:
        """Строковое представление"""
        status = "существует" if self.is_valid() else "не существует"
        return (
            f"Равносторонний треугольник (сторона={self._side}), " f"статус: {status}"
        )

    def __eq__(self, other) -> bool:
        """Сравнение треугольников по площади"""
        if not isinstance(other, EquilateralTriangle):
            return NotImplemented
        return math.isclose(self.area(), other.area())


# === Демонстрация работы ===
if __name__ == "__main__":
    print("=" * 50)
    print("ЗАДАНИЕ 1: РАВНОСТОРОННИЙ ТРЕУГОЛЬНИК")
    print("=" * 50)

    # Создание объектов
    t1 = EquilateralTriangle(5.0)
    t2 = EquilateralTriangle(5.0)
    t3 = EquilateralTriangle(10.0)
    t_invalid = EquilateralTriangle(-3.0)

    # Вывод информации
    print(f"\nТреугольник 1: {t1}")
    print(f"  Периметр: {t1.perimeter():.2f}")
    print(f"  Площадь: {t1.area():.2f}")

    print(f"\nТреугольник 2: {t2}")
    print(f"\nТреугольник 3: {t3}")

    # Проверка невалидного
    print(f"\nНевалидный: {t_invalid}")
    print(f"  Существует? {t_invalid.is_valid()}")

    # Сравнение
    print(f"\nСравнение t1 == t2 (одинаковые): {t1 == t2}")
    print(f"Сравнение t1 == t3 (разные): {t1 == t3}")

    # Изменение стороны
    print(f"\nИзменение стороны t1 на 10...")
    t1.side = 10.0
    print(f"Теперь t1 == t3: {t1 == t3}")
