class Order:
    """Класс продукта, содержащий итоговый состав заказа."""

    def __init__(self):
        self.items = []
        self.total_price = 0

    def add_item(self, description, price):
        self.items.append((description, price))
        self.total_price += price

    def __str__(self):
        receipt = "\n--- Ваш заказ ---\n"
        receipt += "\n".join([f"{desc}: {price} руб." for desc, price in self.items])
        receipt += f"\n-----------------\nИтого к оплате: {self.total_price} руб."
        return receipt


class BurgerOrderBuilder:
    """Конкретный строитель для формирования заказов."""

    def __init__(self):
        self.order = Order()

    def set_burger(self, burger_type):
        prices = {"Веганский": 250, "Куриный": 300, "Говяжий": 380}
        price = prices.get(burger_type, 0)
        self.order.add_item(f"Бургер ({burger_type})", price)

    def set_drink(self, drink_name, is_hot):
        # Логика ценообразования: горячие напитки дороже холодных
        price = 150 if is_hot else 120
        temp_str = "горячий" if is_hot else "холодный"
        self.order.add_item(f"Напиток {temp_str} ({drink_name})", price)

    def set_packaging(self, packaging_type):
        price = 15 if packaging_type == "с собой" else 0
        self.order.add_item(f"Упаковка ({packaging_type})", price)

    def get_result(self):
        return self.order


class OrderDirector:
    """Директор, управляющий процессом сборки."""

    def construct_vegan_takeaway(self, order_builder):
        order_builder.set_burger("Веганский")
        order_builder.set_drink("Пепси", is_hot=False)
        order_builder.set_packaging("с собой")


if __name__ == "__main__":
    builder = BurgerOrderBuilder()
    director = OrderDirector()

    director.construct_vegan_takeaway(builder)
    final_order = builder.get_result()
    print(final_order)
