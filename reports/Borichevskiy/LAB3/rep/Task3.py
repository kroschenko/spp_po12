#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Проект «Принтеры»
Демонстрация поведенческого паттерна «Стратегия» (Strategy Pattern)

Разные модели принтеров используют разные стратегии печати,
которые можно менять во время выполнения программы.
"""

from abc import ABC, abstractmethod


# ==========================
#   ПОВЕДЕНЧЕСКИЙ ПАТТЕРН: СТРАТЕГИЯ
# ==========================

class PrintStrategy(ABC):
    """Абстрактная стратегия печати"""

    @abstractmethod
    def print(self, text: str) -> None:
        pass


class LaserPrintStrategy(PrintStrategy):
    """Лазерная печать"""

    def print(self, text: str) -> None:
        print(f"[LASER] Чёткая лазерная печать: {text}")


class InkjetPrintStrategy(PrintStrategy):
    """Струйная печать"""

    def print(self, text: str) -> None:
        print(f"[INKJET] Струйная печать с насыщенными цветами: {text}")


class MatrixPrintStrategy(PrintStrategy):
    """Матричная печать"""

    def print(self, text: str) -> None:
        print(f"[MATRIX] Матричная точечная печать: {text}")


class PhotoPrintStrategy(PrintStrategy):
    """Фотопечать"""

    def print(self, text: str) -> None:
        print(f"[PHOTO] Фотопечать высокого качества: {text}")


# ==========================
#   КЛАССЫ ПРИНТЕРОВ
# ==========================

class Printer:
    """Базовый принтер, использующий стратегию печати"""

    def __init__(self, model: str, strategy: PrintStrategy):
        self.model = model
        self._strategy = strategy

    def set_strategy(self, strategy: PrintStrategy) -> None:
        """Смена стратегии печати"""
        print(f"\n[{self.model}] Меняем стратегию на {strategy.__class__.__name__}")
        self._strategy = strategy

    def print_document(self, text: str) -> None:
        """Печать документа"""
        print(f"\n[{self.model}] Печать документа...")
        self._strategy.print(text)


# Конкретные модели принтеров

class LaserPrinter(Printer):
    def __init__(self, model: str):
        super().__init__(model, LaserPrintStrategy())


class InkjetPrinter(Printer):
    def __init__(self, model: str):
        super().__init__(model, InkjetPrintStrategy())


class MatrixPrinter(Printer):
    def __init__(self, model: str):
        super().__init__(model, MatrixPrintStrategy())


class PhotoPrinter(Printer):
    def __init__(self, model: str):
        super().__init__(model, PhotoPrintStrategy())


# ==========================
#   ДЕМОНСТРАЦИЯ
# ==========================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMO: ПАТТЕРН 'СТРАТЕГИЯ' ДЛЯ ПРОЕКТА 'ПРИНТЕРЫ'")
    print("=" * 60)

    # Создаём разные принтеры
    laser = LaserPrinter("HP LaserJet 5000")
    inkjet = InkjetPrinter("Canon InkMaster 200")
    matrix = MatrixPrinter("Epson DotMatrix 90")
    photo = PhotoPrinter("Sony PhotoPro X")

    # Печать по умолчанию
    laser.print_document("Отчёт по лабораторной работе")
    inkjet.print_document("Цветная диаграмма")
    matrix.print_document("Накладная №12345")
    photo.print_document("Фотография 10x15")

    # Меняем стратегию печати у лазерного принтера
    laser.set_strategy(PhotoPrintStrategy())
    laser.print_document("Фото высокого качества")

    # Меняем стратегию у струйного принтера
    inkjet.set_strategy(MatrixPrintStrategy())
    inkjet.print_document("Тест матричной печати")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
