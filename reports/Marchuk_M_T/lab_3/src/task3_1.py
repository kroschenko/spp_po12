"""
Модуль для реализации паттерна 'Фабричный метод'.
Обеспечивает создание различных видов кофе через единый интерфейс.
"""
from abc import ABC, abstractmethod


class Coffee(ABC):
    """Абстрактный класс продукта кофе."""

    @abstractmethod
    def get_name(self) -> str:
        """Возвращает название напитка."""


class Espresso(Coffee):
    """Класс напитка Эспрессо."""

    def get_name(self) -> str:
        """Реализация получения названия."""
        return "Эспрессо"


class Latte(Coffee):
    """Класс напитка Латте."""

    def get_name(self) -> str:
        """Реализация получения названия."""
        return "Латте"


class CoffeeMachine:
    """Класс-фабрика для управления заказами."""

    @staticmethod
    def order_coffee(coffee_type: str) -> Coffee:
        """
        Создает объект кофе на основе выбора пользователя.
        :param coffee_type: Строка с кодом напитка
        :return: Объект класса Coffee
        """
        menu = {
            "1": Espresso(),
            "2": Latte()
        }
        return menu.get(coffee_type, Espresso())


def main():
    """Точка входа в программу."""
    print("--- Кофе-автомат ---")
    user_choice = input("Выберите кофе (1-Эспрессо, 2-Латте): ")
    drink = CoffeeMachine.order_coffee(user_choice)
    print(f"Ваш напиток: {drink.get_name()}")


if __name__ == "__main__":
    main()
