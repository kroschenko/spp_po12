"""
Модуль для создания туров с использованием паттерна "Строитель".
Определяет структуру тура, строителей и директора для управления процессом сборки.
"""


class Tour:
    """Класс, представляющий объект Тура."""

    def __init__(self):
        """Инициализация характеристик тура."""
        self.transport = None
        self.accommodation = None
        self.meals = []
        self.excursions = []
        self.total_cost = 0

    def add_cost(self, amount):
        """Добавляет стоимость к общей сумме тура."""
        self.total_cost += amount

    def __str__(self):
        """Возвращает строковое представление деталей тура."""
        meals_str = ", ".join(self.meals) if self.meals else "Нет"
        excursions_str = ", ".join(self.excursions) if self.excursions else "Нет"
        return (
            f"Тур:\n"
            f"  Транспорт: {self.transport}\n"
            f"  Проживание: {self.accommodation}\n"
            f"  Питание: {meals_str}\n"
            f"  Экскурсии: {excursions_str}\n"
            f"  Итоговая стоимость: {self.total_cost} бун."
        )


class TourBuilder:
    """Базовый класс строителя туров."""

    def __init__(self):
        """Создает новый экземпляр тура."""
        self.tour = Tour()

    def build_transport(self, option):
        """Метод для выбора транспорта (должен быть переопределен)."""
        raise NotImplementedError

    def build_accommodation(self, option):
        """Метод для выбора проживания (должен быть переопределен)."""
        raise NotImplementedError

    def add_meal(self, option):
        """Метод для добавления питания (должен быть переопределен)."""
        raise NotImplementedError

    def add_excursion(self, option):
        """Метод для добавления экскурсии (должен быть переопределен)."""
        raise NotImplementedError

    def get_tour(self):
        """Возвращает готовый объект тура."""
        return self.tour


class StandardTourBuilder(TourBuilder):
    """Реализация стандартного строителя туров с логикой расчета цен."""

    def build_transport(self, option):
        """Устанавливает транспорт и обновляет стоимость."""
        self.tour.transport = option
        costs = {"Самолет": 15000, "Поезд": 5000, "Автобус": 2000}
        self.tour.add_cost(costs.get(option, 0))
        return self

    def build_accommodation(self, option):
        """Устанавливает проживание и обновляет стоимость (за 3 дня)."""
        self.tour.accommodation = option
        costs = {"5-звездочный отель": 10000 * 3, "3-звездочный отель": 4000 * 3}
        self.tour.add_cost(costs.get(option, 0))
        return self

    def add_meal(self, option):
        """Добавляет питание и обновляет стоимость (за 3 дня)."""
        self.tour.meals.append(option)
        costs = {"Завтрак": 500 * 3, "Завтрак и ужин": 1200 * 3}
        self.tour.add_cost(costs.get(option, 0))
        return self

    def add_excursion(self, option):
        """Добавляет экскурсию и обновляет стоимость."""
        self.tour.excursions.append(option)
        costs = {"Обзорная по городу": 1500, "Посещение музея": 800}
        self.tour.add_cost(costs.get(option, 0))
        return self


class TourDirector:
    """Класс-директор для управления процессом построения готовых туров."""

    def __init__(self, builder):
        """Инициализация директора с конкретным строителем."""
        self.builder = builder

    def construct_budget_tour(self):
        """Создает бюджетный тур."""
        return (
            self.builder.build_transport("Автобус")
            .build_accommodation("3-звездочный отель")
            .add_meal("Завтрак")
            .get_tour()
        )

    def construct_luxury_tour(self):
        """Создает люкс тур."""
        return (
            self.builder.build_transport("Самолет")
            .build_accommodation("5-звездочный отель")
            .add_meal("Завтрак и ужин")
            .add_excursion("Обзорная по городу")
            .add_excursion("Посещение музея")
            .get_tour()
        )


def main():
    """Основная функция для демонстрации работы паттерна."""
    # Использование Директора
    builder = StandardTourBuilder()
    director = TourDirector(builder)

    budget_tour = director.construct_budget_tour()
    print(budget_tour)

    print("\n" + "=" * 30 + "\n")

    # Ручная сборка (Fluent Interface)
    custom_builder = StandardTourBuilder()
    custom_tour = (
        custom_builder.build_transport("Поезд")
        .build_accommodation("3-звездочный отель")
        .add_meal("Завтрак и ужин")
        .add_excursion("Посещение музея")
        .get_tour()
    )
    print(custom_tour)


if __name__ == "__main__":
    main()
