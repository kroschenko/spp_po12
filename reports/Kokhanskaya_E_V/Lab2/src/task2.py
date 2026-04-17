from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

#  ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ


class OrderStatus(Enum):
    """Статусы заказа"""

    NEW = "Новый"
    PAID = "Оплачен"
    SHIPPED = "Отправлен"
    DELIVERED = "Доставлен"
    CANCELLED = "Отменен"


class PaymentMethod(Enum):
    """Способы оплаты"""

    CARD = "Банковская карта"
    CASH = "Наличные"
    ONLINE = "Онлайн-оплата"


#  АБСТРАКТНЫЙ КЛАСС (ОБОБЩЕНИЕ)


class User(ABC):

    def __init__(self, user_id: int, name: str, email: str):
        self.__user_id = user_id
        self.__name = name
        self.__email = email
        self.__registration_date = datetime.now()

    @abstractmethod
    def get_role(self) -> str:
        """Абстрактный метод - должен быть реализован в наследниках"""
        pass

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, new_email: str):
        if "@" in new_email:
            self.__email = new_email
        else:
            raise ValueError("Некорректный email")

    def __str__(self) -> str:
        return f"{self.get_role()}: {self.__name} (ID: {self.__user_id})"


#  КЛАССЫ-НАСЛЕДНИКИ


class Client(User):

    def __init__(self, user_id: int, name: str, email: str, phone: str):
        super().__init__(user_id, name, email)
        self.__phone = phone
        self.__orders: List["Order"] = []
        self.__is_blacklisted = False
        self.__balance = 5000  # баланс для оплаты (из первого варианта)

    def get_role(self) -> str:
        return "Клиент"

    @property
    def phone(self) -> str:
        return self.__phone

    @property
    def orders(self) -> List["Order"]:
        return self.__orders.copy()

    @property
    def is_blacklisted(self) -> bool:
        return self.__is_blacklisted

    @property
    def balance(self) -> int:
        return self.__balance

    @balance.setter
    def balance(self, value: int):
        self.__balance = value

    @is_blacklisted.setter
    def is_blacklisted(self, value: bool):
        self.__is_blacklisted = value

    def add_order(self, order: "Order"):
        self.__orders.append(order)

    def get_total_spent(self) -> float:
        return sum(
            order.total_amount
            for order in self.__orders
            if order.status == OrderStatus.PAID
        )

    def pay_order(self, order: "Order") -> bool:
        """Упрощенный метод оплаты из первого варианта"""
        total = order.total_amount
        if not self.is_blacklisted and self.__balance >= total:
            self.__balance -= total
            order.status = OrderStatus.PAID
            print(f"{self.name} успешно оплатил заказ.")
            return True
        elif self.is_blacklisted:
            print(f"Клиент {self.name} в черном списке!")
            return False
        else:
            print(f"У {self.name} недостаточно средств!")
            return False

    def make_order(self, products: List["Product"]) -> "Order":
        """Упрощенный метод создания заказа из первого варианта"""
        from order_simple import Order as SimpleOrder

        order = SimpleOrder(self)
        for p in products:
            order.add_item(p)
        return order

    def __str__(self) -> str:
        status = " (в черном списке)" if self.__is_blacklisted else ""
        return f"{super().__str__()}, тел: {self.__phone}{status}, баланс: {self.__balance} руб."


class Admin(User):

    def __init__(self, user_id: int, name: str, email: str, position: str):
        super().__init__(user_id, name, email)
        self.__position = position
        self.__managed_products: List["Product"] = []
        self.__black_list = []  # черный список из первого варианта

    def get_role(self) -> str:
        return "Администратор"

    @property
    def position(self) -> str:
        return self.__position

    @property
    def black_list(self) -> List[str]:
        return self.__black_list.copy()

    def add_product(self, product: "Product"):
        self.__managed_products.append(product)
        print(f"Администратор {self.name} добавил товар: {product.name}")

    def register_sale(self, order: "Order"):
        if order.status == OrderStatus.PAID:
            if hasattr(order, "status"):
                order.status = OrderStatus.SHIPPED
            print(
                f"Продажа зарегистрирована: Заказ #{getattr(order, 'order_id', '?')} отправлен"
            )
            return True
        else:
            print("Ошибка: Заказ не оплачен!")
            return False

    def ban_user(self, client: Client):
        """Метод из первого варианта"""
        if client.name not in self.__black_list:
            self.__black_list.append(client.name)
            client.is_blacklisted = True
            print(f"Пользователь {client.name} занесен в черный список.")
            return True
        return False

    def unban_user(self, client: Client):
        if client.name in self.__black_list:
            self.__black_list.remove(client.name)
            client.is_blacklisted = False
            print(f"Пользователь {client.name} удален из черного списка.")
            return True
        return False

    def add_to_blacklist(self, client: Client):
        return self.ban_user(client)

    def remove_from_blacklist(self, client: Client):
        return self.unban_user(client)

    def __str__(self) -> str:
        return f"{super().__str__()}, должность: {self.__position}"


# ОСНОВНЫЕ КЛАССЫ


class Product:

    def __init__(self, product_id: int, name: str, price: float, quantity: int = 10):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price > 0:
            self.__price = new_price
        else:
            raise ValueError("Цена должна быть положительной")

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, new_quantity: int):
        if new_quantity >= 0:
            self.__quantity = new_quantity
        else:
            raise ValueError("Количество не может быть отрицательным")

    def reduce_quantity(self, amount: int) -> bool:
        if amount <= self.__quantity:
            self.__quantity -= amount
            return True
        return False

    def __str__(self) -> str:
        return f"{self.__name} ({self.__price} руб.)"  # формат из первого варианта


class OrderItem:

    def __init__(self, product: Product, quantity: int):
        self.__product = product
        self.__quantity = quantity
        self.__price_at_order = product.price

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def subtotal(self) -> float:
        return self.__price_at_order * self.__quantity

    def __str__(self) -> str:
        return f"{self.__product.name} x{self.__quantity} = {self.subtotal} руб."


class Order:

    _order_counter = 0

    def __init__(self, client: Client):
        Order._order_counter += 1
        self.__order_id = Order._order_counter
        self.__client = client
        self.__items: List[OrderItem] = []
        self.__status = OrderStatus.NEW
        self.__order_date = datetime.now()
        self.__payment_method = None
        self.is_paid = False  # для совместимости с первым вариантом

    @property
    def order_id(self) -> int:
        return self.__order_id

    @property
    def client(self) -> Client:
        return self.__client

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @status.setter
    def status(self, new_status: OrderStatus):
        self.__status = new_status
        self.is_paid = new_status == OrderStatus.PAID

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.__items)

    def get_total(self) -> float:  # для совместимости с первым вариантом
        return self.total_amount

    def add_item(self, product: Product, quantity: int = 1):
        if product.quantity >= quantity:
            item = OrderItem(product, quantity)
            self.__items.append(item)
            product.reduce_quantity(quantity)
            print(f"Товар {product.name} добавлен в заказ #{self.__order_id}")
        else:
            raise ValueError(f"Недостаточно товара {product.name} на складе")

    def pay(self, payment_method: PaymentMethod = PaymentMethod.CARD):
        if self.__status != OrderStatus.NEW:
            raise ValueError("Заказ уже оплачен или отменен")

        if self.__client.is_blacklisted:
            raise ValueError("Клиент в черном списке. Оплата невозможна")

        self.__payment_method = payment_method
        self.__status = OrderStatus.PAID
        self.is_paid = True
        print(f"Заказ #{self.__order_id} оплачен через {payment_method.value}")
        return True

    def __str__(self) -> str:
        items_str = "\n  ".join(str(item) for item in self.__items)
        status_str = "Оплачен" if self.is_paid else "Не оплачен"
        return f"Заказ #{self.__order_id}: {len(self.__items)} тов., Сумма: {self.total_amount} руб. [{status_str}]"


# ПРОСТАЯ ДЕМОНСТРАЦИЯ (как в первом варианте)


def simple_demo():
    print("=" * 60)
    print("ПРОСТАЯ ДЕМОНСТРАЦИЯ (как в первом варианте)")
    print("=" * 60)

    catalog = []
    admin = Admin(1, "Лена", "lena@store.ru", "Администратор")
    client = Client(1001, "Катя", "katya@mail.ru", "+7-999-123-45-67")

    # Добавление товаров
    p1 = Product(1, "Ноутбук", 3500, 5)
    p2 = Product(2, "Мышь", 500, 20)
    admin.add_product(p1)
    admin.add_product(p2)
    catalog.extend([p1, p2])

    # Заказ
    order = Order(client)
    order.add_item(p1, 1)
    order.add_item(p2, 1)
    print(f"\n{order}")

    # Оплата
    if client.pay_order(order):
        admin.register_sale(order)
    else:
        admin.ban_user(client)

    print(f"Черный список админа: {admin.black_list}")
    print()


# ПОЛНАЯ ДЕМОНСТРАЦИЯ (как во втором варианте)


def full_demo():
    print("=" * 60)
    print("ПОЛНАЯ ДЕМОНСТРАЦИЯ (ООП с композицией и агрегацией)")
    print("=" * 60)

    print("\n1. СОЗДАНИЕ АДМИНИСТРАТОРА И КЛИЕНТОВ")
    admin = Admin(1, "Иван Петров", "ivan@store.ru", "Старший администратор")
    client1 = Client(1001, "Анна Смирнова", "anna@mail.ru", "+7-999-123-45-67")
    client2 = Client(1002, "Петр Иванов", "petr@mail.ru", "+7-999-765-43-21")

    print(admin)
    print(client1)
    print(client2)

    print("\n2. ДОБАВЛЕНИЕ ТОВАРОВ")
    product1 = Product(101, "Ноутбук", 50000, 10)
    product2 = Product(102, "Мышь", 1500, 50)
    product3 = Product(103, "Клавиатура", 3000, 30)

    admin.add_product(product1)
    admin.add_product(product2)
    admin.add_product(product3)

    print("\n3. СОЗДАНИЕ ЗАКАЗА")
    order1 = Order(client1)
    order1.add_item(product1, 1)
    order1.add_item(product2, 2)
    print(f"\n{order1}")

    print("\n4. ОПЛАТА ЗАКАЗА")
    if client1.pay_order(order1):
        admin.register_sale(order1)

    print("\n5. ВТОРОЙ ЗАКАЗ")
    order2 = Order(client2)
    order2.add_item(product3, 1)
    order2.add_item(product2, 1)
    print(f"\n{order2}")

    print("\n6. РАБОТА С ЧЕРНЫМ СПИСКОМ")
    admin.ban_user(client2)
    print(f"Черный список: {admin.black_list}")

    print("\n7. ПОПЫТКА ОПЛАТЫ ЗАБЛОКИРОВАННЫМ КЛИЕНТОМ")
    if client2.pay_order(order2):
        admin.register_sale(order2)
    else:
        print("Оплата отклонена из-за нахождения в черном списке")

    print("\n8. РАЗБЛОКИРОВКА КЛИЕНТА")
    admin.unban_user(client2)

    print("\n9. УСПЕШНАЯ ОПЛАТА ПОСЛЕ РАЗБЛОКИРОВКИ")
    client2.balance = 5000  # пополняем баланс
    if client2.pay_order(order2):
        admin.register_sale(order2)

    print("\n10. СТАТИСТИКА")
    print(f"Баланс {client1.name}: {client1.balance} руб.")
    print(f"Баланс {client2.name}: {client2.balance} руб.")
    print(f"Остаток товаров:")
    print(f"  {product1}")
    print(f"  {product2}")
    print(f"  {product3}")
    print()


if __name__ == "__main__":
    simple_demo()
    full_demo()
