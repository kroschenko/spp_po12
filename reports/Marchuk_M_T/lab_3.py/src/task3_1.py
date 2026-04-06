"""
Задание 1: Кофе-автомат (Паттерн: Фабричный метод).
Позволяет создавать различные типы кофе через единый интерфейс.
"""
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def get_name(self): pass

class Espresso(Coffee):
    def get_name(self): return "Эспрессо"

class Latte(Coffee):
    def get_name(self): return "Латте"

class CoffeeMachine:
    @staticmethod
    def order_coffee(coffee_type):
        menu = {"1": Espresso(), "2": Latte()} # Добавьте остальные 3 класса по аналогии
        return menu.get(coffee_type, Espresso())

if __name__ == "__main__":
    choice = input("Выберите кофе (1-Эспрессо, 2-Латте): ")
    drink = CoffeeMachine.order_coffee(choice)
    print(f"Ваш напиток: {drink.get_name()}")
