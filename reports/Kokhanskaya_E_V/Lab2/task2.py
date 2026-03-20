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
        self.__user_id = user_id  # инкапсуляция
        self.__name = name
        self.__email = email
        self.__registration_date = datetime.now()
    
    @abstractmethod
    def get_role(self) -> str:
        """Абстрактный метод - должен быть реализован в наследниках"""
        pass
    
    # Геттеры и сеттеры (свойства)
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
        self.__orders: List[Order] = []  # Агрегация: клиент имеет список заказов
        self.__is_blacklisted = False
    
    def get_role(self) -> str:
        return "Клиент"
    
    @property
    def phone(self) -> str:
        return self.__phone
    
    @property
    def orders(self) -> List['Order']:
        return self.__orders.copy()
    
    @property
    def is_blacklisted(self) -> bool:
        return self.__is_blacklisted
    
    @is_blacklisted.setter
    def is_blacklisted(self, value: bool):
        self.__is_blacklisted = value
    
    def add_order(self, order: 'Order'):
        
        self.__orders.append(order)
    
    def get_total_spent(self) -> float:
        
        return sum(order.total_amount for order in self.__orders if order.status == OrderStatus.PAID)
    
    def __str__(self) -> str:
        status = " (в черном списке)" if self.__is_blacklisted else ""
        return f"{super().__str__()}, тел: {self.__phone}{status}"


class Admin(User):
    
    
    def __init__(self, user_id: int, name: str, email: str, position: str):
        super().__init__(user_id, name, email)
        self.__position = position
        self.__managed_products: List[Product] = []  # Ассоциация: администратор управляет товарами
    
    def get_role(self) -> str:
        return "Администратор"
    
    @property
    def position(self) -> str:
        return self.__position
    
    def add_product(self, product: 'Product'):
        
        self.__managed_products.append(product)
        print(f"Администратор {self.name} добавил товар: {product.name}")
    
    def register_sale(self, order: 'Order'):
        
        if order.status == OrderStatus.PAID:
            order.status = OrderStatus.SHIPPED
            print(f"Продажа зарегистрирована: Заказ #{order.order_id} отправлен клиенту {order.client.name}")
            return True
        return False
    
    def add_to_blacklist(self, client: Client):
        
        if not client.is_blacklisted:
            client.is_blacklisted = True
            print(f"Клиент {client.name} добавлен в черный список")
            return True
        return False
    
    def remove_from_blacklist(self, client: Client):
       
        if client.is_blacklisted:
            client.is_blacklisted = False
            print(f"Клиент {client.name} удален из черного списка")
            return True
        return False
    
    def __str__(self) -> str:
        return f"{super().__str__()}, должность: {self.__position}"


# ОСНОВНЫЕ КЛАССЫ 

class Product:
    
    
    def __init__(self, product_id: int, name: str, price: float, quantity: int):
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
        return f"Товар: {self.__name} (ID: {self.__product_id}), цена: {self.__price} руб., в наличии: {self.__quantity}"


class OrderItem:
   
    
    def __init__(self, product: Product, quantity: int):
        self.__product = product  # Ассоциация с Product
        self.__quantity = quantity
        self.__price_at_order = product.price  # фиксируем цену на момент заказа
    
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
    
    
    _order_counter = 0  # счетчик для генерации ID
    
    def __init__(self, client: Client):
        Order._order_counter += 1
        self.__order_id = Order._order_counter
        self.__client = client  # Агрегация: заказ принадлежит клиенту
        self.__items: List[OrderItem] = []  # Композиция: позиции существуют только в рамках заказа
        self.__status = OrderStatus.NEW
        self.__order_date = datetime.now()
        self.__payment_method = None
    
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
    
    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.__items)
    
    def add_item(self, product: Product, quantity: int):
        
        if product.quantity >= quantity:
            item = OrderItem(product, quantity)
            self.__items.append(item)
            product.reduce_quantity(quantity)
            print(f"Товар {product.name} добавлен в заказ #{self.__order_id}")
        else:
            raise ValueError(f"Недостаточно товара {product.name} на складе")
    
    def pay(self, payment_method: PaymentMethod):
        
        if self.__status != OrderStatus.NEW:
            raise ValueError("Заказ уже оплачен или отменен")
        
        if self.__client.is_blacklisted:
            raise ValueError("Клиент в черном списке. Оплата невозможна")
        
        self.__payment_method = payment_method
        self.__status = OrderStatus.PAID
        print(f"Заказ #{self.__order_id} оплачен через {payment_method.value}")
        return True
    
    def __str__(self) -> str:
        items_str = "\n  ".join(str(item) for item in self.__items)
        return (f"Заказ #{self.__order_id}\n"
                f"Клиент: {self.__client.name}\n"
                f"Статус: {self.__status.value}\n"
                f"Дата: {self.__order_date.strftime('%d.%m.%Y %H:%M')}\n"
                f"Товары:\n  {items_str}\n"
                f"ИТОГО: {self.total_amount} руб.")


#  ДОПОЛНИТЕЛЬНЫЙ КЛАСС ДЛЯ УПРАВЛЕНИЯ 

class OnlineStore:
    
    def __init__(self, name: str):
        self.__name = name
        self.__products: Dict[int, Product] = {}  # каталог товаров
        self.__clients: Dict[int, Client] = {}    # зарегистрированные клиенты
        self.__admins: Dict[int, Admin] = {}      # администраторы
        self.__orders: List[Order] = []           # все заказы
    
    @property
    def name(self) -> str:
        return self.__name
    
    def register_client(self, client: Client):
        
        self.__clients[client.user_id] = client
        print(f"Клиент {client.name} зарегистрирован в магазине {self.__name}")
    
    def register_admin(self, admin: Admin):
        
        self.__admins[admin.user_id] = admin
        print(f"Администратор {admin.name} добавлен в систему")
    
    def add_product(self, admin: Admin, product: Product):
       
        if admin.user_id in self.__admins:
            self.__products[product.product_id] = product
            admin.add_product(product)
        else:
            raise PermissionError("Только администратор может добавлять товары")
    
    def create_order(self, client: Client) -> Order:
        
        if client.user_id not in self.__clients:
            raise ValueError("Клиент не зарегистрирован в магазине")
        
        order = Order(client)
        client.add_order(order)
        self.__orders.append(order)
        print(f"Создан новый заказ #{order.order_id} для клиента {client.name}")
        return order
    
    def process_payment(self, order: Order, payment_method: PaymentMethod):
        
        return order.pay(payment_method)
    
    def get_client_orders(self, client: Client) -> List[Order]:
        
        return client.orders
    
    def get_blacklisted_clients(self) -> List[Client]:
        
        return [c for c in self.__clients.values() if c.is_blacklisted]
    
    def show_catalog(self):
        
        print(f"\n--- Каталог магазина {self.__name} ---")
        if not self.__products:
            print("Каталог пуст")
        else:
            for product in self.__products.values():
                print(f"  {product}")
    
    def __str__(self) -> str:
        return (f"Интернет-магазин '{self.__name}'\n"
                f"Товаров: {len(self.__products)}, "
                f"Клиентов: {len(self.__clients)}, "
                f"Заказов: {len(self.__orders)}")


# ДЕМОНСТРАЦИЯ РАБОТЫ 

def demo_online_store():
    
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ")
    
    print("\n1. СОЗДАНИЕ МАГАЗИНА")
    store = OnlineStore("СуперМаг")
    print(store)
    
    print("\n2. ДОБАВЛЕНИЕ ТОВАРОВ АДМИНИСТРАТОРОМ")
    admin = Admin(1, "Иван Петров", "ivan@store.ru", "Старший администратор")
    store.register_admin(admin)
    
    product1 = Product(101, "Ноутбук", 50000, 10)
    product2 = Product(102, "Мышь", 1500, 50)
    product3 = Product(103, "Клавиатура", 3000, 30)
    
    store.add_product(admin, product1)
    store.add_product(admin, product2)
    store.add_product(admin, product3)
    
    print("\n3. РЕГИСТРАЦИЯ КЛИЕНТОВ")
    client1 = Client(1001, "Анна Смирнова", "anna@mail.ru", "+7-999-123-45-67")
    client2 = Client(1002, "Петр Иванов", "petr@mail.ru", "+7-999-765-43-21")
    
    store.register_client(client1)
    store.register_client(client2)
    
    print(client1)
    print(client2)
    
    print("\n4. ПРОСМОТР КАТАЛОГА")
    store.show_catalog()
    
    print("\n5. СОЗДАНИЕ ЗАКАЗА")
    order1 = store.create_order(client1)
    order1.add_item(product1, 1)  # ноутбук
    order1.add_item(product2, 2)  # 2 мыши
    print()
    print(order1)
    
    print("\n6. ОПЛАТА ЗАКАЗА")
    store.process_payment(order1, PaymentMethod.CARD)
    
    print("\n7. РЕГИСТРАЦИЯ ПРОДАЖИ")
    admin.register_sale(order1)
    
    print("\n8. ВТОРОЙ ЗАКАЗ")
    order2 = store.create_order(client2)
    order2.add_item(product3, 1)  # клавиатура
    order2.add_item(product2, 1)  # мышь
    print()
    print(order2)
    
    print("\n9. РАБОТА С ЧЕРНЫМ СПИСКОМ")
    print(f"До: {client2}")
    admin.add_to_blacklist(client2)
    print(f"После: {client2}")
    
    print("\n10. ПОПЫТКА ОПЛАТЫ КЛИЕНТОМ ИЗ ЧЕРНОГО СПИСКА")
    try:
        store.process_payment(order2, PaymentMethod.ONLINE)
    except ValueError as e:
        print(f"ОШИБКА: {e}")
    
    print("\n11. УДАЛЕНИЕ ИЗ ЧЕРНОГО СПИСКА")
    admin.remove_from_blacklist(client2)
    print(f"После удаления: {client2}")
    
    print("\n12. УСПЕШНАЯ ОПЛАТА")
    store.process_payment(order2, PaymentMethod.ONLINE)
    admin.register_sale(order2)
    
    print("\n13. ИТОГОВАЯ СТАТИСТИКА")
    print(store)
    print(f"Клиент {client1.name} потратил: {client1.get_total_spent()} руб.")
    print(f"Клиент {client2.name} потратил: {client2.get_total_spent()} руб.")
    
    print("\n14. КАТАЛОГ ПОСЛЕ ПРОДАЖ")
    store.show_catalog()
    
    print("\n15. ЧЕРНЫЙ СПИСОК")
    blacklisted = store.get_blacklisted_clients()
    if blacklisted:
        print("Клиенты в черном списке:")
        for client in blacklisted:
            print(f"  {client}")
    else:
        print("Черный список пуст")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_online_store()