from abc import ABC, abstractmethod


class Pizzeria:

    def create_order(self, items):
        print("Заказ создан:")
        for item in items:
            print(f"- {item}")

    def cancel_order(self):
        print("Заказ отменен")


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class OrderCommand(Command):

    def __init__(self, pizzeria, items):
        self.pizzeria = pizzeria
        self.items = items

    def execute(self):
        self.pizzeria.create_order(self.items)

    def undo(self):
        self.pizzeria.cancel_order()


class Waiter:

    def __init__(self):
        self.history = []
        self.last_command = None

    def take_order(self, command):
        self.last_command = command
        self.history.append(command)
        command.execute()

    def cancel_last(self):
        if self.history:
            command = self.history.pop()
            command.undo()
        else:
            print("Нет заказов для отмены")

    def repeat_last(self):
        if self.last_command:
            print("Повтор последнего заказа:")
            self.last_command.execute()
        else:
            print("Нет заказа для повторения")


def choose_items():
    items = []

    while True:
        print("\nДобавить позицию:")
        print("1. Пицца Маргарита")
        print("2. Пицца Пепперони")
        print("3. Кола")
        print("4. Завершить заказ")

        item_choice = input("Выбор: ")

        if item_choice == "1":
            items.append("Пицца Маргарита")
        elif item_choice == "2":
            items.append("Пицца Пепперони")
        elif item_choice == "3":
            items.append("Кола")
        elif item_choice == "4":
            break

    return items


def process_order(pizzeria, waiter):
    items = choose_items()
    if items:
        command = OrderCommand(pizzeria, items)
        waiter.take_order(command)


def main():

    pizzeria = Pizzeria()
    waiter = Waiter()

    while True:
        print("\nМеню:")
        print("1. Сделать заказ")
        print("2. Отменить последний заказ")
        print("3. Повторить последний заказ")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            process_order(pizzeria, waiter)

        elif choice == "2":
            waiter.cancel_last()

        elif choice == "3":
            waiter.repeat_last()

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
