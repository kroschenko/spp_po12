class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Order:
    def __init__(self, client):
        self.client = client
        self.items = []
        self.is_paid = False

    def add_item(self, product):
        self.items.append(product)

    def get_total(self):
        return sum(item.price for item in self.items)

    def __str__(self):
        status = "Оплачен" if self.is_paid else "Не оплачен"
        return f"Заказ {self.client.name}: {len(self.items)} тов., Сумма: {self.get_total()} руб. [{status}]"


class User:
    def __init__(self, name):
        self.name = name


class Client(User):
    def __init__(self, name):
        super().__init__(name)
        self.balance = 5000  #баланс для примера

    def make_order(self, products):
        order = Order(self)
        for p in products:
            order.add_item(p)
        return order

    def pay_order(self, order):
        total = order.get_total()
        if self.balance >= total:
            self.balance -= total
            order.is_paid = True
            print(f"{self.name} успешно оплатил заказ.")
            return True
        print(f"У {self.name} недостаточно средств!")
        return False


class Admin(User):
    def __init__(self, name):
        super().__init__(name)
        self.black_list = []

    def add_product(self, catalog, product):
        catalog.append(product)
        print(f"Админ {self.name} добавил товар: {product.name}")

    def register_sale(self, order):
        if order.is_paid:
            print(f"Продажа зарегистрирована: {order}")
        else:
            print(f"Ошибка: Заказ не оплачен!")

    def ban_user(self, client):
        if client.name not in self.black_list:
            self.black_list.append(client.name)
            print(f"Пользователь {client.name} занесен в черный список.")


# Пример
catalog = []
admin = Admin("Лена")
client = Client("Катя")

# Добавление товаров
p1 = Product("Ноутбук", 3500)
p2 = Product("Мышь", 500)
admin.add_product(catalog, p1)
admin.add_product(catalog, p2)

# Заказ
my_order = client.make_order([p1, p2])
print(my_order)

# Оплаьа
if client.pay_order(my_order):
    admin.register_sale(my_order)
else:
    admin.ban_user(client)

print(f"Черный список админа: {admin.black_list}")
