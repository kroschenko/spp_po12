"""Strategy task"""
from abc import ABC, abstractmethod


class PrintStrategy(ABC):
    """Strategy abstract base class"""
    @abstractmethod
    def print(self, text):
        """Print text"""

    @abstractmethod
    def done(self):
        """Print done"""


class ColorPrint(PrintStrategy):
    """Strategy concrete class"""
    def print(self, text):
        return f"Color printing: {text}"

    def done(self):
        return "Color printing done"


class BWPrint(PrintStrategy):
    """Strategy concrete class"""
    def print(self, text):
        return f"Black & White printing: {text}"

    def done(self):
        return "BW printing done"


class FastPrint(PrintStrategy):
    """Strategy concrete class"""
    def print(self, text):
        return f"Fast printing: {text}"

    def done(self):
        return "Fast printing done"


class Printer:
    """Client class"""
    def __init__(self, strategy: PrintStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PrintStrategy):
        """Set strategy"""
        self.strategy = strategy

    def print(self, text):
        """Print text"""
        return self.strategy.print(text)


if __name__ == "__main__":
    printer = Printer(ColorPrint())

    print(printer.print("Hello World"))

    printer.set_strategy(BWPrint())
    print(printer.print("Hello World"))

    printer.set_strategy(FastPrint())
    print(printer.print("Hello World"))
