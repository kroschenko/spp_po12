"""Модуль для работы с файловой системой."""

from abc import ABC, abstractmethod
from datetime import datetime


class FileSystemComponent(ABC):
    """Абстрактный компонент файловой системы."""

    def __init__(self, name):
        self.name = name
        self.date_created = datetime.now()

    @abstractmethod
    def get_size(self):
        """Получить размер элемента."""

    @abstractmethod
    def display(self, indent=0):
        """Отобразить элемент."""


class File(FileSystemComponent):
    """Класс файла."""

    def __init__(self, name, size, extension):
        super().__init__(name)
        self.size = size
        self.extension = extension

    def get_size(self):
        """Получить размер файла."""
        return self.size

    def display(self, indent=0):
        """Отобразить файл."""
        print(" " * indent + f"Файл: {self.name}.{self.extension} ({self.size} байт)")


class Directory(FileSystemComponent):
    """Класс директории."""

    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, component):
        """Добавить элемент в директорию."""
        self.children.append(component)

    def remove(self, component):
        """Удалить элемент из директории."""
        self.children.remove(component)

    def get_size(self):
        """Получить общий размер директории."""
        total = 0
        for child in self.children:
            total += child.get_size()
        return total

    def display(self, indent=0):
        """Отобразить директорию."""
        print(" " * indent + f"Директория: {self.name}/")
        for child in self.children:
            child.display(indent + 2)


def create_file(root):
    """Создать файл."""
    name = input("Введите имя файла: ")
    size = int(input("Введите размер файла (байт): "))
    ext = input("Введите расширение: ")
    new_file = File(name, size, ext)
    print(f"Файл {name}.{ext} создан")

    dest = input("Добавить в корень? (да/нет): ")
    if dest.lower() == "да":
        root.add(new_file)
    else:
        dir_name = input("Введите имя директории: ")
        for child in root.children:
            if isinstance(child, Directory) and child.name == dir_name:
                child.add(new_file)
                return
        print("Директория не найдена, файл добавлен в корень")
        root.add(new_file)


def create_directory(root):
    """Создать директорию."""
    name = input("Введите имя директории: ")
    new_dir = Directory(name)
    root.add(new_dir)
    print(f"Директория {name} создана")


def add_to_directory(root):
    """Добавить элемент в директорию."""
    dir_name = input("Введите имя директории, куда добавить элемент: ")
    for child in root.children:
        if isinstance(child, Directory) and child.name == dir_name:
            print("1. Добавить существующий файл")
            print("2. Создать новый файл")
            sub_choice = input("Выберите (1-2): ")

            if sub_choice == "1":
                file_name = input("Введите имя файла: ")
                file_size = int(input("Введите размер: "))
                file_ext = input("Введите расширение: ")
                new_file = File(file_name, file_size, file_ext)
                child.add(new_file)
                print(f"Файл добавлен в {dir_name}")
            elif sub_choice == "2":
                name = input("Введите имя файла: ")
                file_size = int(input("Введите размер (байт): "))
                file_ext = input("Введите расширение: ")
                new_file = File(name, file_size, file_ext)
                child.add(new_file)
                print(f"Файл {name}.{file_ext} добавлен в {dir_name}")
            return
    print("Директория не найдена")


def delete_element(root):
    """Удалить элемент."""
    name = input("Введите имя элемента для удаления: ")
    for child in root.children[:]:
        if child.name == name:
            root.remove(child)
            print(f"{name} удален")
            return
    print("Элемент не найден")


def show_structure(root):
    """Показать структуру."""
    print("\n" + "=" * 50)
    print("СТРУКТУРА ФАЙЛОВОЙ СИСТЕМЫ")
    print("=" * 50)
    root.display()


def main():
    """Основная функция программы."""
    root = Directory("root")

    while True:
        print("\n" + "=" * 50)
        print("ФАЙЛОВАЯ СИСТЕМА")
        print("=" * 50)
        print("1. Создать файл")
        print("2. Создать директорию")
        print("3. Добавить элемент в директорию")
        print("4. Удалить элемент")
        print("5. Показать всю структуру")
        print("6. Выход")

        choice = input("\nВыберите действие (1-6): ")

        if choice == "1":
            create_file(root)
        elif choice == "2":
            create_directory(root)
        elif choice == "3":
            add_to_directory(root)
        elif choice == "4":
            delete_element(root)
        elif choice == "5":
            show_structure(root)
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()
