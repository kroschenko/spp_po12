"""
Модуль, реализующий паттерн Строитель (Builder) для сборки заказа
в бургер-закусочной.
"""


class Item:
    """Базовый класс для любой позиции меню."""
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    def name(self) -> str:
        """Возвращает название позиции."""
        return self._name

    def price(self) -> float:
        """Возвращает цену позиции."""
        return self._price


class Packaging:
    """Базовый класс для типа упаковки."""
    def __init__(self, pack_type: str, extra_cost: float):
        self._pack_type = pack_type
        self._extra_cost = extra_cost

    def pack_type(self) -> str:
        """Возвращает текстовое описание типа упаковки."""
        return self._pack_type

    def extra_cost(self) -> float:
        """Возвращает добавочную стоимость за упаковку."""
        return self._extra_cost


class Menu:
    """Пространство имен для фабричных методов позиций меню."""

    @staticmethod
    def vegan_burger() -> Item:
        """Создает и возвращает веганский бургер."""
        return Item("Веганский бургер", 350.0)

    @staticmethod
    def chicken_burger() -> Item:
        """Создает и возвращает куриный бургер."""
        return Item("Куриный бургер", 300.0)

    @staticmethod
    def pepsi() -> Item:
        """Создает и возвращает Пепси."""
        return Item("Холодный напиток (Пепси)", 100.0)

    @staticmethod
    def coffee() -> Item:
        """Создает и возвращает кофе."""
        return Item("Горячий напиток (Кофе)", 150.0)


class PackagingType:
    """Пространство имен для фабричных методов типов упаковки."""

    @staticmethod
    def take_away() -> Packaging:
        """Создает упаковку 'С собой'."""
        return Packaging("С собой (в пакете)", 20.0)

    @staticmethod
    def dine_in() -> Packaging:
        """Создает упаковку 'На месте'."""
        return Packaging("На месте (на подносе)", 0.0)


class Order:
    """Класс заказа, который конструируется Строителем."""
    def __init__(self):
        self.items = []
        self.packaging = None

    def add_item(self, item: Item):
        """Добавляет новую позицию (Item) в список заказа."""
        self.items.append(item)

    def set_packaging(self, packaging: Packaging):
        """Устанавливает выбранный тип упаковки для заказа."""
        self.packaging = packaging

    def get_total_cost(self) -> float:
        """Рассчитывает итоговую стоимость заказа с учетом упаковки."""
        cost = sum(item.price() for item in self.items)
        return cost + (self.packaging.extra_cost() if self.packaging else 0)

    def print_receipt(self):
        """Выводит чек заказа в консоль."""
        print("ЧЕК ЗАКАЗА")
        for item in self.items:
            print(f"- {item.name()}: {item.price()} руб.")
        if self.packaging:
            print(f"- Упаковка [{self.packaging.pack_type()}]: "
                  f"+{self.packaging.extra_cost()} руб.")
        print(f"ИТОГО К ОПЛАТЕ: {self.get_total_cost()} руб.\n")



class OrderBuilder:
    """Строитель для пошагового создания заказа."""
    def __init__(self):
        self.order = Order()

    def add(self, item_creator):
        """Универсальный метод добавления любой позиции."""
        self.order.add_item(item_creator())
        return self

    def pack(self, packaging_creator):
        """Универсальный метод выбора упаковки."""
        self.order.set_packaging(packaging_creator())
        return self

    def build(self) -> Order:
        """Возвращает готовый собранный заказ."""
        return self.order


if __name__ == "__main__":
    order1 = (OrderBuilder()
              .add(Menu.chicken_burger)
              .add(Menu.pepsi)
              .pack(PackagingType.take_away)
              .build())
    order1.print_receipt()

    order2 = (OrderBuilder()
              .add(Menu.vegan_burger)
              .add(Menu.coffee)
              .pack(PackagingType.dine_in)
              .build())
    order2.print_receipt()
