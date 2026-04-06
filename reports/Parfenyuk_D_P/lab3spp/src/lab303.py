"""
Модуль для лабораторной работы №3.
Задание 3 (Поведенческий паттерн: Команда).
Вариант 7: Проект «Пиццерия» (Заказ, отмена, повтор).
"""

# pylint: disable=too-few-public-methods


class PizzaOrder:
    """Класс, представляющий конкретный заказ пиццы (Получатель)."""

    def __init__(self, pizza_name):
        """Инициализация заказа названием пиццы."""
        self.pizza_name = pizza_name

    def prepare(self):
        """Метод для начала приготовления пиццы."""
        print(f"-> Пицца '{self.pizza_nam1e}' готовится в печи.")

    def cancel(self):
        """Метод для отмены приготовления."""
        print(f"-> Заказ на пиццу '{self.pizza_name}' успешно ОТМЕНЕН.")


class OrderCommand:
    """Класс команды для управления заказом."""

    def __init__(self, order):
        """Инициализация команды объектом заказа."""
        self.order = order

    def execute(self):
        """Выполнение команды (создание заказа)."""
        self.order.prepare()

    def undo(self):
        """Отмена команды (отмена заказа)."""
        self.order.cancel()


class Waiter:
    """Класс официанта, управляющего историей заказов (Инициатор)."""

    def __init__(self):
        """Инициализация пустого списка истории."""
        self.history = []

    def place_order(self, command):
        """Принимает заказ и сохраняет его в историю."""
        command.execute()
        self.history.append(command)

    def cancel_last(self):
        """Отменяет последний сделанный заказ из истории."""
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("История пуста: нет заказов для отмены.")

    def repeat_last(self):
        """Повторяет последний заказ из истории."""
        if self.history:
            last_command = self.history[-1]
            print(f"ПОВТОР: {last_command.order.pizza_name}")
            self.place_order(last_command)
        else:
            print("История пуста: нет заказов для повтора.")


def main():
    """Основная функция с интерактивным меню пиццерии."""
    waiter = Waiter()

    while True:
        print("\n--- МЕНЮ ПИЦЦЕРИИ ---")
        print("1. Сделать новый заказ")
        print("2. Отменить последний заказ")
        print("3. Повторить последний заказ")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Введите название пиццы: ")
            new_order = PizzaOrder(name)
            command = OrderCommand(new_order)
            waiter.place_order(command)
        elif choice == "2":
            waiter.cancel_last()
        elif choice == "3":
            waiter.repeat_last()
        elif choice == "0":
            break
        else:
            print("Ошибка: выберите пункт из меню.")


if __name__ == "__main__":
    main()
