"""
Модуль для реализации паттерна 'Стратегия'.
Позволяет изменять функционал кнопок калькулятора во время выполнения.
"""
import math
from abc import ABC, abstractmethod


class ButtonFunction(ABC):
    """Абстрактный класс стратегии функции кнопки."""

    @abstractmethod
    def calculate(self, value: float) -> float:
        """
        Выполняет расчет.
        :param value: Входное число.
        """


class SqrtStrategy(ButtonFunction):
    """Стратегия для вычисления квадратного корня."""

    def calculate(self, value: float) -> float:
        """Расчет корня."""
        return math.sqrt(value)


class CalculatorButton:
    """Класс кнопки калькулятора, использующий стратегию."""

    def __init__(self, strategy: ButtonFunction):
        """
        Инициализация с конкретной стратегией.
        :param strategy: Объект функции кнопки.
        """
        self.strategy = strategy

    def press(self, value: float) -> float:
        """
        Нажатие на кнопку.
        :param value: Число для обработки.
        :return: Результат вычисления.
        """
        return self.strategy.calculate(value)


def main():
    """Точка входа в программу."""
    button = CalculatorButton(SqrtStrategy())
    print(f"Корень из 16: {button.press(16.0)}")


if __name__ == "__main__":
    main()
