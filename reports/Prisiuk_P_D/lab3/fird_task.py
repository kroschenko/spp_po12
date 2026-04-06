# pylint: disable=too-few-public-methods
"""
Модуль реализует паттерн Команда для настраиваемой клавиатуры калькулятора.
Позволяет динамически изменять функционал кнопок.
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """
    Абстрактный базовый класс для всех команд калькулятора.
    """

    @abstractmethod
    def execute(self) -> None:
        """Метод для выполнения команды."""


class AddCommand(Command):
    """Команда для выполнения операции сложения."""

    def execute(self) -> None:
        print("Выполнение: Сложение")


class MemoryClearCommand(Command):
    """Команда для очистки памяти калькулятора."""

    def execute(self) -> None:
        print("Выполнение: Очистка памяти")


class SquareRootCommand(Command):
    """Команда для вычисления квадратного корня."""

    def execute(self) -> None:
        print("Выполнение: Квадратный корень")


class Button:
    """
    Класс кнопки клавиатуры. Хранит команду и вызывает её при нажатии.
    """

    def __init__(self, command: Command):
        self.command = command

    def press(self) -> None:
        """Эмуляция нажатия кнопки."""
        self.command.execute()


if __name__ == "__main__":
    # Создаем кнопку с начальной командой
    custom_button = Button(MemoryClearCommand())
    print("Нажатие кнопки с начальной функцией:")
    custom_button.press()

    # Динамически меняем поведение кнопки (настройка)
    print("\nПеренастройка кнопки на извлечение корня:")
    custom_button.command = SquareRootCommand()
    custom_button.press()
