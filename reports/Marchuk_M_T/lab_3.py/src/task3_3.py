"""
Задание 3: Клавиатура калькулятора (Паттерн: Стратегия).
Позволяет менять функцию кнопки 'F1' на лету.
"""
from abc import ABC, abstractmethod
import math

class ButtonFunction(ABC):
    @abstractmethod
    def calculate(self, x): pass

class SqrtStrategy(ButtonFunction):
    def calculate(self, x): return math.sqrt(x)

class CalculatorButton:
    def __init__(self, strategy):
        self.strategy = strategy

    def press(self, value):
        return self.strategy.calculate(value)

if __name__ == "__main__":
    btn = CalculatorButton(SqrtStrategy())
    print(f"Корень из 16: {btn.press(16)}")
