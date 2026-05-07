# pylint: disable=invalid-name
"""
Модуль реализует систему заказа в бургерной с использованием паттерна Строитель.
"""


class Order:
    """Класс, представляющий готовый заказ клиента."""

    def __init__(self):
        """Инициализация пустого заказа."""
        self.items = []
        self.packaging = ""
        self.total_price = 0.0

    def add_item(self, name: str, price: float):
        """Добавление позиции в заказ."""
        self.items.append(name)
        self.total_price += price

    def set_packaging(self, pack_type: str, price: float):
        """Установка типа упаковки."""
        self.packaging = pack_type
        self.total_price += price

    def __str__(self):
        """Строковое представление заказа."""
        items_str = ", ".join(self.items)
        return (
            f"--- ВАШ ЗАКАЗ ---\n"
            f"Состав: {items_str}\n"
            f"Упаковка: {self.packaging}\n"
            f"Итоговая стоимость: {self.total_price:.2f} руб.\n"
            f"-----------------"
        )


class OrderBuilder:
    """Абстрактный класс строителя заказов."""

    def reset(self):
        """Сброс состояния строителя."""
        raise NotImplementedError

    def add_burger(self, burger_type: str):
        """Метод добавления бургера."""
        raise NotImplementedError

    def add_drink(self, drink_name: str):
        """Метод добавления напитка."""
        raise NotImplementedError

    def set_packaging(self, to_go: bool):
        """Метод выбора упаковки."""
        raise NotImplementedError

    def get_result(self) -> Order:
        """Получение готового объекта заказа."""
        raise NotImplementedError


class BurgerOrderBuilder(OrderBuilder):
    """Конкретная реализация строителя для бургер-закусочной."""

    def __init__(self):
        """Инициализация строителя и прейскуранта цен."""
        self._order = Order()
        self._prices = {
            "веганский": 250.0,
            "куриный": 300.0,
            "говяжий": 350.0,
            "пепси": 100.0,
            "кока-кола": 100.0,
            "кофе": 150.0,
            "чай": 80.0,
            "с собой": 20.0,
            "на месте": 0.0,
        }

    def reset(self):
        """Создание нового чистого объекта заказа."""
        self._order = Order()

    def add_burger(self, burger_type: str):
        """Добавление бургера в заказ."""
        name = f"Бургер ({burger_type})"
        price = self._prices.get(burger_type.lower(), 0.0)
        self._order.add_item(name, price)
        return self

    def add_drink(self, drink_name: str):
        """Добавление напитка в заказ."""
        name = f"Напиток ({drink_name})"
        price = self._prices.get(drink_name.lower(), 0.0)
        self._order.add_item(name, price)
        return self

    def set_packaging(self, to_go: bool):
        """Выбор типа упаковки (на месте или с собой)."""
        if to_go:
            self._order.set_packaging("С собой", self._prices["с собой"])
        else:
            self._order.set_packaging("На месте", self._prices["на месте"])
        return self

    def get_result(self) -> Order:
        """Возврат собранного заказа и подготовка к следующему."""
        result = self._order
        self.reset()
        return result


class Waiter:
    """Класс Директора (Официанта), управляющий процессом сборки."""

    def __init__(self):
        """Инициализация официанта без назначенного строителя."""
        self._builder = None

    @property
    def builder(self) -> OrderBuilder:
        """Свойство для получения текущего строителя."""
        return self._builder

    @builder.setter
    def builder(self, value: OrderBuilder):
        """Свойство для установки строителя."""
        self._builder = value

    def construct_vegan_combo(self):
        """Сборка стандартного веганского набора."""
        self._builder.add_burger("веганский")
        self._builder.add_drink("чай")
        self._builder.set_packaging(False)

    def construct_meat_to_go(self):
        """Сборка мясного набора на вынос."""
        self._builder.add_burger("говяжий")
        self._builder.add_drink("кока-кола")
        self._builder.set_packaging(True)


if __name__ == "__main__":
    burger_builder = BurgerOrderBuilder()

    waiter_service = Waiter()
    waiter_service.builder = burger_builder

    print("--- Демонстрация работы Строителя ---\n")

    print("Заказ №1 (Веган-комбо через Директора):")
    waiter_service.construct_vegan_combo()
    print(burger_builder.get_result())

    print("\nЗаказ №2 (Индивидуальный заказ напрямую через Строителя):")
    burger_builder.add_burger("куриный").add_drink("кофе").set_packaging(True)
    print(burger_builder.get_result())

    print("\nЗаказ №3 (Мясной набор с собой):")
    waiter_service.construct_meat_to_go()
    print(burger_builder.get_result())
