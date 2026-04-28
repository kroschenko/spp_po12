"""Модуль для создания туристических туров с использованием паттерна Строитель."""

from abc import ABC, abstractmethod


class Tour:
    """Класс тура, содержащий информацию о поездке."""

    def __init__(self):
        self.transport = None
        self.accommodation = None
        self.meals = None
        self.museums = []
        self.exhibitions = []
        self.excursions = []
        self.price = 0

    def get_price(self):
        """Возвращает стоимость тура."""
        return self.price

    def __str__(self):
        result = "\n" + "=" * 50
        result += "\nВАШ ИНДИВИДУАЛЬНЫЙ ТУР"
        result += "\n" + "=" * 50
        result += f"\nТранспорт: {self.transport or 'не выбран'}"
        result += f"\nПроживание: {self.accommodation or 'не выбрано'}"
        result += f"\nПитание: {self.meals or 'не выбрано'}"

        if self.museums:
            result += f"\nМузеи: {', '.join(self.museums)}"
        else:
            result += "\nМузеи: не выбраны"

        if self.exhibitions:
            result += f"\nВыставки: {', '.join(self.exhibitions)}"
        else:
            result += "\nВыставки: не выбраны"

        if self.excursions:
            result += f"\nЭкскурсии: {', '.join(self.excursions)}"
        else:
            result += "\nЭкскурсии: не выбраны"

        result += f"\nИТОГОВАЯ СТОИМОСТЬ: {self.price} руб."
        result += "\n" + "=" * 50
        return result


class TourBuilder(ABC):
    """Абстрактный строитель для создания тура."""

    @abstractmethod
    def reset(self):
        """Сброс строителя."""

    @abstractmethod
    def build_transport(self, transport_type):
        """Добавление транспорта."""

    @abstractmethod
    def build_accommodation(self, accommodation_type, nights):
        """Добавление проживания."""

    @abstractmethod
    def build_meals(self, meals_type, days):
        """Добавление питания."""

    @abstractmethod
    def build_museum(self, museum_name):
        """Добавление музея."""

    @abstractmethod
    def build_exhibition(self, exhibition_name):
        """Добавление выставки."""

    @abstractmethod
    def build_excursion(self, excursion_name):
        """Добавление экскурсии."""

    @abstractmethod
    def get_tour(self):
        """Получение готового тура."""


class TourBuilderImpl(TourBuilder):
    """Конкретный строитель тура."""

    def __init__(self):
        self.tour = None
        self.reset()

    def reset(self):
        """Сброс строителя."""
        self.tour = Tour()

    def build_transport(self, transport_type):
        """Добавление транспорта."""
        prices = {
            "автобус": 5000,
            "поезд": 8000,
            "самолет": 15000,
            "нет": 0,
        }
        self.tour.transport = transport_type
        self.tour.price += prices.get(transport_type.lower(), 0)

    def build_accommodation(self, accommodation_type, nights):
        """Добавление проживания."""
        prices = {
            "хостел": 2000,
            "отель 3*": 3500,
            "отель 4*": 5000,
            "отель 5*": 8000,
            "нет": 0,
        }
        price_per_night = prices.get(accommodation_type.lower(), 0)
        self.tour.accommodation = f"{accommodation_type} ({nights} ночей)"
        self.tour.price += price_per_night * nights

    def build_meals(self, meals_type, days):
        """Добавление питания."""
        prices = {
            "без питания": 0,
            "завтрак": 1000,
            "полупансион": 2000,
            "полный пансион": 3000,
            "все включено": 5000,
        }
        price_per_day = prices.get(meals_type.lower(), 0)
        self.tour.meals = f"{meals_type} ({days} дней)"
        self.tour.price += price_per_day * days

    def build_museum(self, museum_name):
        """Добавление музея."""
        self.tour.museums.append(museum_name)
        self.tour.price += 500

    def build_exhibition(self, exhibition_name):
        """Добавление выставки."""
        self.tour.exhibitions.append(exhibition_name)
        self.tour.price += 400

    def build_excursion(self, excursion_name):
        """Добавление экскурсии."""
        self.tour.excursions.append(excursion_name)
        self.tour.price += 800

    def get_tour(self):
        """Получение готового тура."""
        tour = self.tour
        self.reset()
        return tour


def get_days():
    """Получение количества дней тура."""
    while True:
        try:
            days = int(input("\nВведите количество дней тура: "))
            if days > 0:
                return days
            print("Количество дней должно быть положительным числом!")
        except ValueError:
            print("Пожалуйста, введите целое число!")


def get_transport(builder):
    """Выбор транспорта."""
    print("\n" + "-" * 40)
    print("ВИДЫ ТРАНСПОРТА:")
    print("1. Автобус (5000 руб)")
    print("2. Поезд (8000 руб)")
    print("3. Самолет (15000 руб)")
    print("4. Без транспорта")

    while True:
        choice = input("Выберите транспорт (1-4): ")
        transport_map = {
            "1": "автобус",
            "2": "поезд",
            "3": "самолет",
            "4": "нет",
        }
        if choice in transport_map:
            builder.build_transport(transport_map[choice])
            break
        print("Неверный выбор! Пожалуйста, выберите 1-4.")


def get_accommodation(builder, days):
    """Выбор проживания."""
    print("\n" + "-" * 40)
    print("ТИПЫ ПРОЖИВАНИЯ (ЦЕНА ЗА НОЧЬ):")
    print("1. Хостел (2000 руб/ночь)")
    print("2. Отель 3* (3500 руб/ночь)")
    print("3. Отель 4* (5000 руб/ночь)")
    print("4. Отель 5* (8000 руб/ночь)")
    print("5. Без проживания")

    while True:
        choice = input("Выберите тип проживания (1-5): ")
        accom_map = {
            "1": "хостел",
            "2": "отель 3*",
            "3": "отель 4*",
            "4": "отель 5*",
            "5": "нет",
        }
        if choice in accom_map:
            builder.build_accommodation(accom_map[choice], days)
            break
        print("Неверный выбор! Пожалуйста, выберите 1-5.")


def get_meals(builder, days):
    """Выбор питания."""
    print("\n" + "-" * 40)
    print("ТИПЫ ПИТАНИЯ (ЦЕНА ЗА ДЕНЬ):")
    print("1. Без питания (0 руб/день)")
    print("2. Только завтрак (1000 руб/день)")
    print("3. Полупансион (2000 руб/день)")
    print("4. Полный пансион (3000 руб/день)")
    print("5. Все включено (5000 руб/день)")

    while True:
        choice = input("Выберите тип питания (1-5): ")
        meals_map = {
            "1": "без питания",
            "2": "завтрак",
            "3": "полупансион",
            "4": "полный пансион",
            "5": "все включено",
        }
        if choice in meals_map:
            builder.build_meals(meals_map[choice], days)
            break
        print("Неверный выбор! Пожалуйста, выберите 1-5.")


def get_additional_services(builder):
    """Добавление дополнительных услуг."""
    print("\n" + "-" * 40)
    print("ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ:")

    while True:
        print("\n1. Добавить музей (500 руб)")
        print("2. Добавить выставку (400 руб)")
        print("3. Добавить экскурсию (800 руб)")
        print("4. Завершить создание тура")

        service = input("Выберите услугу (1-4): ")

        if service == "1":
            museum = input("Введите название музея: ")
            builder.build_museum(museum)
            print(f"Музей '{museum}' добавлен!")
        elif service == "2":
            exhibition = input("Введите название выставки: ")
            builder.build_exhibition(exhibition)
            print(f"Выставка '{exhibition}' добавлена!")
        elif service == "3":
            excursion = input("Введите название экскурсии: ")
            builder.build_excursion(excursion)
            print(f"Экскурсия '{excursion}' добавлена!")
        elif service == "4":
            break
        else:
            print("Неверный выбор! Пожалуйста, выберите 1-4.")


def main():
    """Основная функция программы."""
    print("=" * 60)
    print("ТУРИСТИЧЕСКОЕ БЮРО 'ИНДИВИДУАЛЬНЫЙ ТУР'")
    print("=" * 60)
    print("Создайте свой идеальный тур шаг за шагом!")

    builder = TourBuilderImpl()

    days = get_days()
    get_transport(builder)
    get_accommodation(builder, days)
    get_meals(builder, days)
    get_additional_services(builder)

    tour = builder.get_tour()
    print(tour)
    print("\nСпасибо за использование нашего сервиса!")


if __name__ == "__main__":
    main()
