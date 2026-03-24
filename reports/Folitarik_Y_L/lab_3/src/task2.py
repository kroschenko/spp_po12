"""
Модуль реализует модель файловой системы с использованием паттерна 'Компоновщик'.
Поддерживает файлы и директории с расчетом размера и иерархическим выводом.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class FileSystemItem(ABC):
    """
    Общий интерфейс для компонентов файловой системы (файлов и папок).
    """

    def __init__(self, name):
        """Инициализация базовых атрибутов элемента."""
        self.name = name
        self.created_at = datetime.now()

    @abstractmethod
    def get_size(self):
        """Возвращает размер элемента в байтах."""

    @abstractmethod
    def display(self, indent=0):
        """Выводит структуру элемента с отступом."""


class File(FileSystemItem):
    """
    Класс 'Лист' (Leaf) - представляет отдельный файл.
    """

    def __init__(self, name, extension, size):
        """
        Инициализация файла.
        :param name: Имя файла без расширения.
        :param extension: Расширение файла (например, '.txt').
        :param size: Размер в байтах.
        """
        super().__init__(name)
        self.extension = extension
        self.size = size

    def get_size(self):
        """Возвращает фиксированный размер файла."""
        return self.size

    def display(self, indent=0):
        """Отображает информацию о файле."""
        prefix = "    " * indent
        date_str = self.created_at.strftime("%Y-%m-%d %H:%M")
        print(
            f"{prefix}📄 {self.name}{self.extension} "
            f"({self.size} B) | Создан: {date_str}"
        )


class Directory(FileSystemItem):
    """
    Класс 'Компоновщик' (Composite) - представляет директорию.
    Может содержать как файлы, так и другие директории.
    """

    def __init__(self, name):
        """Инициализация пустого списка содержимого."""
        super().__init__(name)
        self.children = []

    def add(self, item: FileSystemItem):
        """Добавляет элемент в директорию."""
        self.children.append(item)

    def remove(self, item: FileSystemItem):
        """Удаляет элемент из директории."""
        self.children.remove(item)

    def get_size(self):
        """Рекурсивно вычисляет общий размер всех вложенных элементов."""
        return sum(child.get_size() for child in self.children)

    def display(self, indent=0):
        """Рекурсивно отображает дерево каталогов и файлов."""
        prefix = "    " * indent
        print(f"{prefix}📁 [{self.name}] | Общий размер: {self.get_size()} B")
        for child in self.children:
            child.display(indent + 1)


def main():
    """Точка входа для демонстрации работы файловой системы."""
    # Создаем файлы
    file1 = File("config", ".yaml", 500)
    file2 = File("script", ".py", 1200)
    file3 = File("presentation", ".pptx", 5000)
    file4 = File("notes", ".txt", 100)

    # Создаем структуру директорий
    root = Directory("C:")
    users = Directory("Users")
    admin = Directory("Admin")
    projects = Directory("Projects")

    # Собираем иерархию
    root.add(users)
    users.add(admin)
    admin.add(projects)
    admin.add(file4)  # notes.txt в папке Admin

    projects.add(file1)
    projects.add(file2)
    root.add(file3)  # презентация в корне диска

    # Вывод всей структуры
    print("Структура файловой системы:")
    root.display()

    # Демонстрация работы get_size()
    print("\nСтатистика:")
    print(f"Размер папки 'Projects': {projects.get_size()} байт")
    print(f"Общий размер диска '{root.name}': {root.get_size()} байт")


if __name__ == "__main__":
    main()
