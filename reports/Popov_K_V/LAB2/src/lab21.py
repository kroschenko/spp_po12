"""
Модуль системы Интернет-магазин.
Содержит классы для управления пользователями, товарами и заказами.
"""


# pylint: disable=too-few-public-methods
class User:
    """Базовый класс для всех пользователей системы."""

    def __init__(self, name):
        """Инициализация пользователя именем."""
        self.name = name

    def __str__(self):
        """Строковое представление пользователя."""
        return f"Пользователь: {self.name}"


class Client(User):
    """Класс клиента магазина с балансом и статусом блокировки."""

    def __init__(self, name, balance=0):
        """Инициализация клиента."""
        super().__init__(name)
        self.balance = balance
        self.is_blocked = False

    def pay(self, amount):
        """Метод для проведения оплаты заказа."""
        if self.is_blocked:
            print(f"Клиент {self.name} находится в черном списке")
            return False

        if self.balance >= amount:
            self.balance -= amount
            print(f"Оплата {amount} прошла успешно. Остаток: {self.balance}")
            return True

        print(f"Отказ: Недостаточно средств на счету {self.name}.")
        return False

    def __str__(self):
        """Строковое представление статуса клиента."""
        status = "Заблокирован" if self.is_blocked else "Активен"
        return f"Клиент: {self.name} | Баланс: {self.balance} | Статус: {status}"


class Administrator(User):
    """Класс администратора для управления товарами и продажами."""

    def add_product_info(self, name, price):
        """Добавление информации о новом товаре."""
        print(f"Админ {self.name} добавил в магазин товар: {name} за {price}")
        return Product(name, price)

    def reg_sale(self, order):
        """Регистрация продажи на основе статуса оплаты заказа."""
        print(f"\nАдмин {self.name} проверяет заказ клиента {order.client.name}")
        if order.is_paid:
            print("Продажа зарегистрирована")
        else:
            print("Продажа отменена")

    def black_list(self, client):
        """Занесение клиента в черный список."""
        client.is_blocked = True
        print(f"Админ {self.name} занес пользователя {client.name} в список")


# pylint: disable=too-few-public-methods
class Product:
    """Класс, описывающий товар в магазине."""

    def __init__(self, name, price):
        """Инициализация товара названием и ценой."""
        self.name = name
        self.price = price

    def __eq__(self, value):
        """Сравнение товаров по названию и цене."""
        if not isinstance(value, Product):
            return False
        return self.name == value.name and self.price == value.price

    def __str__(self):
        """Строковое описание товара."""
        return f"{self.name} ({self.price} руб.)"


class Order:
    """Класс заказа, агрегирующий список товаров."""

    def __init__(self, client):
        """Инициализация заказа для конкретного клиента."""
        self.client = client
        self.items = []
        self.is_paid = False

    def add_item(self, product):
        """Добавление товара в корзину заказа."""
        self.items.append(product)
        print(f"В корзину {self.client.name} добавлен: {product.name}")

    def calculate(self):
        """Подсчет общей стоимости всех товаров в заказе."""
        return sum(item.price for item in self.items)

    def process_payment(self):
        """Процесс инициации оплаты заказа клиентом."""
        total = self.calculate()
        if self.client.pay(total):
            self.is_paid = True
            print("Статус заказа изменен на: ОПЛАЧЕН")
            return True

        print("Статус заказа: ОЖИДАЕТ ОПЛАТЫ")
        return False

    def __str__(self):
        """Строковое представление состава и статуса заказа."""
        items_str = ", ".join([p.name for p in self.items])
        status = "Оплачен" if self.is_paid else "Ожидает Оплаты"
        return f"Заказ: [{items_str}] | Итого: {self.calculate()} | {status}"


def main():
    """Основная функция демонстрации работы системы."""
    admin = Administrator("Степан")
    p1 = admin.add_product_info("Ноутбук", 10000)
    p2 = admin.add_product_info("Телефон", 5000)

    customer = Client("Гоша", balance=200)

    print("\nДобавление товаров клиентом и попытка оплаты")
    order = Order(customer)
    order.add_item(p1)
    order.add_item(p2)
    order.process_payment()
    admin.reg_sale(order)

    print("\nЕсли у пользователя вдруг появились деньги")
    customer.balance = 20000
    order.process_payment()
    admin.reg_sale(order)


if __name__ == "__main__":
    main()
