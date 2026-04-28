"""
Task3 — реализация поведенческого паттерна «Стратегия»
на примере разных моделей принтеров.
"""

from abc import ABC, abstractmethod


# ==========================
#       СТРАТЕГИИ ПЕЧАТИ
# ==========================

class PrintStrategy(ABC):
    """Абстрактная стратегия печати."""

    @abstractmethod
    def print_document(self, text: str) -> str:
        """Возвращает строку, описывающую процесс печати."""


class LaserPrintStrategy(PrintStrategy):
    """Лазерная печать."""

    def print_document(self, text: str) -> str:
        return f"[LASER] Чёткая лазерная печать: {text}"


class InkjetPrintStrategy(PrintStrategy):
    """Струйная печать."""

    def print_document(self, text: str) -> str:
        return f"[INKJET] Цветная струйная печать: {text}"


class MatrixPrintStrategy(PrintStrategy):
    """Матричная печать."""

    def print_document(self, text: str) -> str:
        return f"[MATRIX] Матричная печать: {text}"


# ==========================
#         ПРИНТЕР
# ==========================

class Printer:
    """Контекст, использующий стратегию печати."""

    def __init__(self, strategy: PrintStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PrintStrategy) -> None:
        """Позволяет менять стратегию во время выполнения."""
        self._strategy = strategy

    def print(self, text: str) -> str:
        """Возвращает результат печати."""
        return self._strategy.print_document(text)


# ==========================
#       МИНИ-ДЕМОНСТРАЦИЯ
# ==========================

if __name__ == "__main__":
    printer = Printer(LaserPrintStrategy())
    print(printer.print("Документ 1"))

    printer.set_strategy(InkjetPrintStrategy())
    print(printer.print("Документ 2"))
