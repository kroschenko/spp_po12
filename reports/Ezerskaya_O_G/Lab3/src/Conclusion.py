"""Модуль для вывода файловой системы в случайном порядке."""

from abc import ABC, abstractmethod
from datetime import datetime
import random


class Iterator(ABC):
    """Абстрактный итератор."""

    @abstractmethod
    def has_next(self):
        """Проверить наличие следующего элемента."""

    @abstractmethod
    def next(self):
        """Получить следующий элемент."""


class FileSystemComponent(ABC):
    """Абстрактный компонент файловой системы."""

    def __init__(self, name):
        self.name = name
        self.date_created = datetime.now()

    @abstractmethod
    def get_size(self):
        """Получить размер элемента."""

    @abstractmethod
    def get_attributes(self):
        """Получить атрибуты элемента."""


class File(FileSystemComponent):
    """Класс файла."""

    def __init__(self, name, size, extension):
        super().__init__(name)
        self.size = size
        self.extension = extension

    def get_size(self):
        """Получить размер файла."""
        return self.size

    def get_attributes(self):
        """Получить атрибуты файла."""
        return {
            "тип": "файл",
            "имя": self.name,
            "расширение": self.extension,
            "размер": f"{self.size} байт",
            "дата создания": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Directory(FileSystemComponent):
    """Класс директории."""

    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, component):
        """Добавить элемент в директорию."""
        self.children.append(component)

    def get_size(self):
        """Получить общий размер директории."""
        total = 0
        for child in self.children:
            total += child.get_size()
        return total

    def get_attributes(self):
        """Получить атрибуты директории."""
        return {
            "тип": "директория",
            "имя": self.name,
            "размер": f"{self.get_size()} байт",
            "количество элементов": len(self.children),
            "дата создания": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }


class RandomIterator(Iterator):
    """Итератор для случайного обхода файловой системы."""

    def __init__(self, root):
        self.items = []
        self._collect_all(root)
        random.shuffle(self.items)
        self.index = 0

    def _collect_all(self, component):
        """Собрать все элементы ФС."""
        self.items.append(component)
        if isinstance(component, Directory):
            for child in component.children:
                self._collect_all(child)

    def has_next(self):
        """Проверить наличие следующего элемента."""
        return self.index < len(self.items)

    def next(self):
        """Получить следующий элемент."""
        if self.has_next():
            item = self.items[self.index]
            self.index += 1
            return item
        return None


def create_filesystem():
    """Создать файловую систему для демонстрации."""
    root = Directory("root")

    documents = Directory("documents")
    documents.add(File("resume", 1024, "pdf"))
    documents.add(File("notes", 512, "txt"))
    documents.add(File("presentation", 2048, "pptx"))
    root.add(documents)

    photos = Directory("photos")
    photos.add(File("vacation", 3072, "jpg"))
    photos.add(File("family", 4096, "png"))
    root.add(photos)

    music = Directory("music")
    music.add(File("song1", 5120, "mp3"))
    music.add(File("song2", 6144, "mp3"))
    root.add(music)

    projects = Directory("projects")
    projects.add(File("main", 2048, "py"))
    projects.add(File("utils", 1024, "py"))
    documents.add(projects)

    return root


def print_element(element):
    """Вывести информацию об элементе."""
    attrs = element.get_attributes()

    print(f"\n{'-' * 40}")
    if attrs["тип"] == "файл":
        print(f"Файл: {attrs['имя']}.{attrs['расширение']}")
    else:
        print(f"Директория: {attrs['имя']}/")

    for key, value in attrs.items():
        if key not in ("тип", "имя"):
            print(f"   {key}: {value}")


def print_structure_info():
    """Вывести информацию о структуре ФС."""
    print("СОЗДАНА СЛЕДУЮЩАЯ СТРУКТУРА ФС:")
    print("root/")
    print("  ├── documents/")
    print("  │   ├── resume.pdf")
    print("  │   ├── notes.txt")
    print("  │   ├── presentation.pptx")
    print("  │   └── projects/")
    print("  │       ├── main.py")
    print("  │       └── utils.py")
    print("  ├── photos/")
    print("  │   ├── vacation.jpg")
    print("  │   └── family.png")
    print("  └── music/")
    print("      ├── song1.mp3")
    print("      └── song2.mp3")


def main():
    """Основная функция программы."""
    print("=" * 60)
    print("ВЫВОД ФАЙЛОВОЙ СИСТЕМЫ В СЛУЧАЙНОМ ПОРЯДКЕ")
    print("(Паттерн Итератор)")
    print("=" * 60)

    root = create_filesystem()
    print_structure_info()

    print("\n" + "=" * 60)
    print("ВЫВОД ЭЛЕМЕНТОВ В СЛУЧАЙНОМ ПОРЯДКЕ:")
    print("=" * 60)

    iterator = RandomIterator(root)

    while iterator.has_next():
        element = iterator.next()
        print_element(element)

    print(f"\n{'-' * 40}")
    print(f"\nВсего выведено элементов: {len(iterator.items)}")


if __name__ == "__main__":
    main()
