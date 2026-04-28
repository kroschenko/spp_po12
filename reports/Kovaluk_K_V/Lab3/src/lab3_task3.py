from copy import deepcopy


class Pizza:
    def __init__(self, name, size, price, ingredients=None):
        self.name = name
        self.size = size
        self.price = price
        self.ingredients = ingredients or []

    def __str__(self):
        return f"{self.name} ({self.size}) - {self.price} руб"


class Order:
    def __init__(self, order_id=None):
        self.order_id = order_id
        self.items = []
        self.status = "создан"

    def add_pizza(self, pizza):
        self.items.append(pizza)

    def remove_pizza(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def total_cost(self):
        return sum(pizza.price for pizza in self.items)

    def get_items_description(self):
        return [str(pizza) for pizza in self.items]

    def __str__(self):
        items_str = ", ".join([pizza.name for pizza in self.items])
        return f"Заказ #{self.order_id}: {items_str} - Итого: {self.total_cost()} руб"


class Command:
    def execute(self):
        pass

    def undo(self):
        pass


class CreateOrderCommand(Command):
    def __init__(self, pizzeria, pizzas, order_id=None):
        self.pizzeria = pizzeria
        self.pizzas = pizzas
        self.order_id = order_id
        self.created_order = None

    def execute(self):
        self.created_order = self.pizzeria.create_order(self.pizzas, self.order_id)
        print(f"{self.created_order}")
        return self.created_order

    def undo(self):
        if self.created_order:
            self.pizzeria.cancel_order(self.created_order.order_id)
            print(f"Отменён {self.created_order}")


class CancelOrderCommand(Command):
    def __init__(self, pizzeria, order_id):
        self.pizzeria = pizzeria
        self.order_id = order_id
        self.cancelled_order = None

    def execute(self):
        self.cancelled_order = self.pizzeria.cancel_order(self.order_id)
        if self.cancelled_order:
            print(f"Отменён {self.cancelled_order}")
        else:
            print(f"Заказ #{self.order_id} не найден")
        return self.cancelled_order

    def undo(self):
        if self.cancelled_order:
            restored = self.pizzeria.create_order(
                self.cancelled_order.items,
                self.cancelled_order.order_id
            )
            print(f"Восстановлен {restored}")


class RepeatLastOrderCommand(Command):
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria
        self.repeated_order = None
        self.original_order = None

    def execute(self):
        self.original_order = self.pizzeria.get_last_order()
        if self.original_order:
            copied_pizzas = deepcopy(self.original_order.items)
            self.repeated_order = self.pizzeria.create_order(copied_pizzas)
            print(f"Повторный {self.repeated_order} (копия заказа #{self.original_order.order_id})")
        else:
            print("Нет предыдущих заказов для повторения")
        return self.repeated_order

    def undo(self):
        if self.repeated_order:
            self.pizzeria.cancel_order(self.repeated_order.order_id)
            print(f"Отменён повторный {self.repeated_order}")


class AddPizzaCommand(Command):
    def __init__(self, pizzeria, order_id, pizza):
        self.pizzeria = pizzeria
        self.order_id = order_id
        self.pizza = pizza
        self.added = False

    def execute(self):
        self.added = self.pizzeria.add_pizza_to_order(self.order_id, self.pizza)
        if self.added:
            print(f"Добавлена {self.pizza} в заказ #{self.order_id}")
        else:
            print(f"Заказ #{self.order_id} не найден")
        return self.added

    def undo(self):
        if self.added:
            self.pizzeria.remove_last_pizza(self.order_id)
            print(f"Удалена последняя пицца из заказа #{self.order_id}")


class Pizzeria:
    def __init__(self):
        self.orders = {}
        self.next_order_id = 1
        self.order_history = []

    def create_order(self, pizzas, custom_id=None):
        order_id = custom_id if custom_id else self.next_order_id
        if not custom_id:
            self.next_order_id += 1

        order = Order(order_id)
        for pizza in pizzas:
            order.add_pizza(pizza)

        self.orders[order_id] = order
        return order

    def cancel_order(self, order_id):
        if order_id in self.orders:
            cancelled = self.orders.pop(order_id)
            cancelled.status = "отменён"
            return cancelled
        return None

    def get_order(self, order_id):
        return self.orders.get(order_id)

    def get_last_order(self):
        if self.orders:
            last_id = max(self.orders.keys())
            return self.orders[last_id]
        return None

    def add_pizza_to_order(self, order_id, pizza):
        order = self.get_order(order_id)
        if order:
            order.add_pizza(pizza)
            return True
        return False

    def remove_last_pizza(self, order_id):
        order = self.get_order(order_id)
        if order and order.items:
            return order.remove_pizza(-1)
        return None

    def show_all_orders(self):
        print("\n--- Текущие заказы в пиццерии ---")
        if not self.orders:
            print("Нет активных заказов")
        else:
            for order in self.orders.values():
                print(f"  {order}")


class CommandInvoker:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        result = command.execute()
        self.history.append(command)
        return result

    def undo_last(self):
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("Нет команд для отмены")


if __name__ == "__main__":
    pizzeria = Pizzeria()
    invoker = CommandInvoker()

    margherita = Pizza("Маргарита", "30см", 450)
    pepperoni = Pizza("Пепперони", "35см", 580)
    quattro_formaggi = Pizza("Четыре сыра", "30см", 520)
    hawaiian = Pizza("Гавайская", "35см", 550)

    print("\n--- 1. Создание первого заказа ---")
    cmd1 = CreateOrderCommand(pizzeria, [margherita, pepperoni])
    invoker.execute_command(cmd1)
    pizzeria.show_all_orders()

    print("\n--- 2. Добавление пиццы в заказ ---")
    cmd2 = AddPizzaCommand(pizzeria, 1, quattro_formaggi)
    invoker.execute_command(cmd2)
    order = pizzeria.get_order(1)
    print(f"Заказ #{order.order_id}: {order.get_items_description()}")
    print(f"Общая стоимость: {order.total_cost()} руб")

    print("\n--- 3. Создание второго заказа ---")
    cmd3 = CreateOrderCommand(pizzeria, [hawaiian])
    invoker.execute_command(cmd3)
    pizzeria.show_all_orders()

    print("\n--- 4. Отмена последней команды (добавление пиццы) ---")
    invoker.undo_last()
    order = pizzeria.get_order(1)
    print(f"После отмены: заказ #{order.order_id}: {order.get_items_description()}")
    print(f"Стоимость: {order.total_cost()} руб")

    print("\n--- 5. Повтор последнего заказа ---")
    cmd4 = RepeatLastOrderCommand(pizzeria)
    invoker.execute_command(cmd4)
    pizzeria.show_all_orders()

    print("\n--- 6. Отмена заказа через команду ---")
    cmd5 = CancelOrderCommand(pizzeria, 2)
    invoker.execute_command(cmd5)
    pizzeria.show_all_orders()

    print("\n--- 7. Восстановление отменённого заказа (undo) ---")
    invoker.undo_last()
    pizzeria.show_all_orders()

    print("\n--- 8. Итоговая информация ---")
    print(f"Всего заказов в системе: {len(pizzeria.orders)}")
    for order in pizzeria.orders.values():
        print(f"  {order}")
        print(f"    Статус: {order.status}")
        print(f"    Позиции: {order.get_items_description()}")
