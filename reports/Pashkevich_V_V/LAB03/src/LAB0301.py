from abc import ABC, abstractmethod


# Продукт
class Coffee(ABC):
    @abstractmethod
    def recipe(self) -> str:
        pass

    @abstractmethod
    def price(self) -> float:
        pass

    def prepare(self) -> str:
        return f"Готовится напиток: {self.__class__.__name__}\nРецепт: {self.recipe()}\nЦена: {self.price()} руб."


# Конкретные продукты
class Espresso(Coffee):
    def recipe(self) -> str:
        return "30 мл воды, 7 г молотого кофе"

    def price(self) -> float:
        return 120.0


class Americano(Coffee):
    def recipe(self) -> str:
        return "Эспрессо + 100 мл горячей воды"

    def price(self) -> float:
        return 140.0


class Cappuccino(Coffee):
    def recipe(self) -> str:
        return "Эспрессо + 120 мл вспененного молока"

    def price(self) -> float:
        return 180.0


class Latte(Coffee):
    def recipe(self) -> str:
        return "Эспрессо + 200 мл молока + молочная пена"

    def price(self) -> float:
        return 190.0


class Mocha(Coffee):
    def recipe(self) -> str:
        return "Эспрессо + шоколад + молоко + молочная пена"

    def price(self) -> float:
        return 210.0


# Создатель
class CoffeeFactory(ABC):
    @abstractmethod
    def create_coffee(self) -> Coffee:
        pass


# Конкретные создатели
class EspressoFactory(CoffeeFactory):
    def create_coffee(self) -> Coffee:
        return Espresso()


class AmericanoFactory(CoffeeFactory):
    def create_coffee(self) -> Coffee:
        return Americano()


class CappuccinoFactory(CoffeeFactory):
    def create_coffee(self) -> Coffee:
        return Cappuccino()


class LatteFactory(CoffeeFactory):
    def create_coffee(self) -> Coffee:
        return Latte()


class MochaFactory(CoffeeFactory):
    def create_coffee(self) -> Coffee:
        return Mocha()


# Клиент
class CoffeeMachine:
    def __init__(self):
        self.factories = {
            "espresso": EspressoFactory(),
            "americano": AmericanoFactory(),
            "cappuccino": CappuccinoFactory(),
            "latte": LatteFactory(),
            "mocha": MochaFactory(),
        }

    def make_coffee(self, coffee_name: str) -> Coffee:
        coffee_name = coffee_name.lower()

        factory = self.factories.get(coffee_name)
        if not factory:
            raise ValueError(f"Напиток '{coffee_name}' не поддерживается автоматом.")

        coffee = factory.create_coffee()
        print(coffee.prepare())
        return coffee


# Демонстрация работы
if __name__ == "__main__":
    machine = CoffeeMachine()

    orders = ["espresso", "latte", "mocha", "americano", "cappuccino"]

    for order in orders:
        print("=" * 50)
        machine.make_coffee(order)
