"""
Модуль реализует модель файловой системы с использованием паттерна 'Посетитель'.
Логика обхода и операций вынесена из классов данных в отдельные классы-посетители.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class FileSystemVisitor(ABC):
    """Абстрактный интерфейс посетителя для операций над файловой системой."""

    @abstractmethod
    def visit_file(self, file):
        """Действие при посещении файла."""

    @abstractmethod
    def visit_directory(self, directory):
        """Действие при посещении директории."""


class FileSystemItem(ABC):
    """Базовый элемент файловой системы."""

    def __init__(self, name):
        """Инициализация базовых атрибутов."""
        self.name = name
        self.created_at = datetime.now()

    @abstractmethod
    def accept(self, visitor: FileSystemVisitor):
        """Метод для принятия посетителя (двойная диспетчеризация)."""


class File(FileSystemItem):
    """Класс, представляющий файл (данные)."""

    def __init__(self, name, extension, size):
        """Инициализация атрибутов файла."""
        super().__init__(name)
        self.extension = extension
        self.size = size

    def accept(self, visitor: FileSystemVisitor):
        """Файл сообщает посетителю, что он — файл."""
        visitor.visit_file(self)


class Directory(FileSystemItem):
    """Класс, представляющий директорию (структуру)."""

    def __init__(self, name):
        """Инициализация списка дочерних элементов."""
        super().__init__(name)
        self.children = []

    def add(self, item: FileSystemItem):
        """Добавление элемента в папку."""
        self.children.append(item)

    def accept(self, visitor: FileSystemVisitor):
        """Директория сообщает посетителю о себе и инициирует обход детей."""
        visitor.visit_directory(self)
        for child in self.children:
            child.accept(visitor)


class SizeCalculatorVisitor(FileSystemVisitor):
    """Посетитель для подсчета суммарного размера всей структуры."""

    def __init__(self):
        """Инициализация счетчика."""
        self.total_size = 0

    def visit_file(self, file: File):
        """Прибавляет размер файла к общему итогу."""
        self.total_size += file.size

    def visit_directory(self, directory: Directory):
        """При посещении директории ничего не делает (размер вычислят файлы)."""


class PrintStructureVisitor(FileSystemVisitor):
    """Посетитель для красивой печати дерева файловой системы."""

    def __init__(self):
        """Инициализация уровня отступа."""
        self.indent = 0

    def visit_file(self, file: File):
        """Печать информации о файле."""
        prefix = "    " * (self.indent + 1)
        print(f"{prefix}📄 {file.name}{file.extension} ({file.size} B)")

    def visit_directory(self, directory: Directory):
        """Печать информации о директории и управление отступами."""
        prefix = "    " * self.indent
        print(f"{prefix}📁 [{directory.name}]")
        self.indent += 1

    def decrease_indent(self):
        """Вспомогательный метод для уменьшения отступа (если нужно)."""
        self.indent -= 1


def main():
    """Точка входа: создание структуры и применение посетителей."""
    root = Directory("Root")
    bin_dir = Directory("bin")
    etc_dir = Directory("etc")

    file_sh = File("bash", ".sh", 2500)
    file_conf = File("hosts", ".conf", 400)
    file_log = File("sys", ".log", 10000)

    root.add(bin_dir)
    root.add(etc_dir)
    bin_dir.add(file_sh)
    etc_dir.add(file_conf)
    root.add(file_log)

    print("--- Структура ФС ---")
    printer = PrintStructureVisitor()
    root.accept(printer)

    print("\n--- Расчет размера ---")
    size_calc = SizeCalculatorVisitor()
    root.accept(size_calc)
    print(f"Общий размер системы: {size_calc.total_size} байт")


if __name__ == "__main__":
    main()
