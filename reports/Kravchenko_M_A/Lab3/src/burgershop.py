"""
Система Бургер-закусочная.
Паттерн: Builder (Строитель).
"""


class Burger:
    """Класс бургера."""

    def __init__(self, burger_type: str):
        self.burger_type = burger_type
        self.price = self._get_price()

    def _get_price(self) -> float:
        """Получить цену бургера."""
        prices = {
            "веганский": 10.6,
            "куриный": 4.3,
            "говяжий": 4.3,
            "рыбный": 9.5,
            "двойной": 8.7,
        }
        return prices.get(self.burger_type.lower(), 150)

    def get_price(self) -> float:
        """Получить цену."""
        return self.price

    def get_type(self) -> str:
        """Получить тип."""
        return self.burger_type

    def __str__(self):
        return f"{self.burger_type} бургер ({self.price} руб.)"


class Drink:
    """Класс напитка."""

    def __init__(self, drink_type: str):
        self.drink_type = drink_type
        self.price = self._get_price()

    def _get_price(self) -> float:
        """Получить цену напитка."""
        prices = {
            "фанта": 5.2,
            "кока-кола": 5.2,
            "спрайт": 5.2,
            "кофе": 6.0,
            "чай": 3.8,
            "капучино": 6.2,
        }
        return prices.get(self.drink_type.lower(), 80)

    def get_price(self) -> float:
        """Получить цену."""
        return self.price

    def get_type(self) -> str:
        """Получить тип."""
        return self.drink_type

    def __str__(self):
        return f"{self.drink_type} ({self.price} руб.)"


class Packaging:
    """Класс упаковки."""

    def __init__(self, packaging_type: str):
        self.packaging_type = packaging_type
        self.price = self._get_price()

    def _get_price(self) -> float:
        """Получить цену упаковки."""
        prices = {
            "с собой": 0,
            "на месте": 0,
            "доставка": 3.0,
        }
        return prices.get(self.packaging_type.lower(), 0)

    def get_price(self) -> float:
        """Получить цену."""
        return self.price

    def get_type(self) -> str:
        """Получить тип."""
        return self.packaging_type

    def __str__(self):
        price_str = f"+{self.price} руб." if self.price > 0 else "бесплатно"
        return f"Упаковка: {self.packaging_type} ({price_str})"


class Order:
    """Класс заказа."""

    def __init__(self):
        self.burger = None
        self.drink = None
        self.packaging = None
        self.total_price = 0

    def set_burger(self, burger: Burger):
        """Установить бургер."""
        self.burger = burger
        self._update_total()

    def set_drink(self, drink: Drink):
        """Установить напиток."""
        self.drink = drink
        self._update_total()

    def set_packaging(self, packaging: Packaging):
        """Установить упаковку."""
        self.packaging = packaging
        self._update_total()

    def _update_total(self):
        """Обновить итоговую стоимость."""
        total = 0
        if self.burger:
            total += self.burger.get_price()
        if self.drink:
            total += self.drink.get_price()
        if self.packaging:
            total += self.packaging.get_price()
        self.total_price = total

    def get_total(self) -> float:
        """Получить итоговую сумму."""
        return self.total_price

    def __str__(self):
        lines = ["\n" + "=" * 40, "ВАШ ЗАКАЗ:", "=" * 40]
        if self.burger:
            lines.append(f"Бургер: {self.burger}")
        if self.drink:
            lines.append(f"Напиток: {self.drink}")
        if self.packaging:
            lines.append(f"{self.packaging}")
        lines.append("-" * 40)
        lines.append(f"ИТОГО: {self.total_price} руб.")
        lines.append("=" * 40)
        return "\n".join(lines)


class OrderBuilder:
    """Строитель заказа (паттерн Builder)."""

    def __init__(self):
        self.order = Order()

    def choose_burger(self):
        """Выбрать бургер."""
        print("\nДоступные бургеры:")
        burgers = ["веганский", "куриный", "говяжий", "рыбный", "двойной"]
        for i, b in enumerate(burgers, 1):
            print(f"  {i}. {b}")

        choice = int(input("Выберите бургер (1-5): "))
        if 1 <= choice <= len(burgers):
            self.order.set_burger(Burger(burgers[choice - 1]))
            print(f"Добавлен: {burgers[choice - 1]} бургер")
        return self

    def choose_drink(self):
        """Выбрать напиток."""
        print("\nДоступные напитки:")
        drinks = ["пепси", "кока-кола", "спрайт", "кофе", "чай", "капучино"]
        for i, d in enumerate(drinks, 1):
            print(f"  {i}. {d}")

        choice = int(input("Выберите напиток (1-6): "))
        if 1 <= choice <= len(drinks):
            self.order.set_drink(Drink(drinks[choice - 1]))
            print(f"Добавлен: {drinks[choice - 1]}")
        return self

    def choose_packaging(self):
        """Выбрать упаковку."""
        print("\nТип упаковки:")
        pack_types = ["с собой", "на месте", "доставка"]
        for i, p in enumerate(pack_types, 1):
            print(f"  {i}. {p}")

        choice = int(input("Выберите упаковку (1-3): "))
        if 1 <= choice <= len(pack_types):
            self.order.set_packaging(Packaging(pack_types[choice - 1]))
            print(f"Выбрано: {pack_types[choice - 1]}")
        return self

    def get_order(self) -> Order:
        """Вернуть готовый заказ."""
        return self.order

    def build(self) -> Order:
        """Вернуть готовый заказ (алиас)."""
        return self.order


class OrderDirector:
    """Директор для создания предустановленных заказов."""

    def __init__(self):
        self.builder = OrderBuilder()

    def create_standard_burger_order(self) -> Order:
        """Стандартный заказ."""
        self.builder = OrderBuilder()
        order = self.builder.choose_burger().choose_drink().choose_packaging().get_order()
        return order

    def create_vegan_order(self) -> Order:
        """Веганский заказ."""
        order = Order()
        order.set_burger(Burger("веганский"))
        order.set_drink(Drink("чай"))
        order.set_packaging(Packaging("на месте"))
        return order


def main():
    """Основная функция."""
    print("=" * 60)
    print("БУРГЕР-ЗАКУСОЧНАЯ")
    print("=" * 60)

    print("\nСоздание нового заказа:")

    builder = OrderBuilder()
    builder.choose_burger()
    builder.choose_drink()
    builder.choose_packaging()

    order = builder.build()
    print(order)

    print("\n1. Оформить заказ")
    print("2. Отменить")
    choice = input("Выбор: ")

    if choice == "1":
        print("\nЗаказ оформлен. Спасибо!")
    else:
        print("\nЗаказ отменен.")


if __name__ == "__main__":
    main()
