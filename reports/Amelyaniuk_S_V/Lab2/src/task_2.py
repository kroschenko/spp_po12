"""Модуль для симуляции работы библиотеки."""


class Book:  # pylint: disable=R0903
    """Класс для представления книги."""

    def __init__(self, title, is_rare=False):
        """Инициализирует книгу с названием и флагом редкости."""
        self.title = title
        self.is_rare = is_rare

    def __repr__(self):
        """Возвращает строковое представление книги."""
        type_str = "(Редкая)" if self.is_rare else ""
        return f"Книга '{self.title}' {type_str}"


class Order:  # pylint: disable=R0903
    """Класс для представления заказа книги."""

    def __init__(self, reader, book_title):
        """Инициализирует заказ с читателем и названием книги."""
        self.reader = reader
        self.book_title = book_title


class Catalog:
    """Класс для каталога книг в библиотеке."""

    def __init__(self):
        """Инициализирует пустой каталог."""
        self.books = {}

    def add_book(self, book):
        """Добавляет книгу в каталог."""
        self.books[book.title] = book

    def find(self, title):
        """Находит книгу по названию в каталоге."""
        return self.books.get(title)


class Reader:
    """Класс для представления читателя библиотеки."""

    def __init__(self, name):
        """Инициализирует читателя с именем."""
        self.name = name
        self.books_on_hands = []
        self.in_blacklist = False

    def create_order(self, book_title):
        """Создает заказ на книгу."""
        return Order(self, book_title)

    def receive_book(self, book):
        """Получает книгу на руки."""
        self.books_on_hands.append(book)

    def return_book(self, title):
        """Возвращает книгу в библиотеку."""
        for b in self.books_on_hands:
            if b.title == title:
                self.books_on_hands.remove(b)
                return True
        return False

    def __str__(self):
        """Возвращает строковое представление читателя."""
        status = "[В ЧЕРНОМ СПИСКЕ]" if self.in_blacklist else "[OK]"
        return (
            f"Читатель: {self.name} {status}. Книг на руках: {len(self.books_on_hands)}"
        )


class Librarian:  # pylint: disable=R0903
    """Класс для библиотекаря, обрабатывающего заказы."""

    def process_order(self, order, library_catalog):
        """Обрабатывает заказ читателя."""
        reader = order.reader

        if reader.in_blacklist:
            print(f"Библиотекарь: отказ. {reader.name} в черном списке.")
            return

        book = library_catalog.find(order.book_title)
        if not book:
            print(f"Библиотекарь: Книги '{order.book_title}' нет в каталоге.")
            return

        place = "в Читальный зал" if book.is_rare else "на Абонемент"
        print(f"Библиотекарь: Выдаю '{book.title}' {place} читателю {reader.name}.")
        reader.receive_book(book)


class Administrator:  # pylint: disable=R0903
    """Класс для администратора, проверяющего должников."""

    def check_debts(self, readers):
        """Проверяет читателей на наличие невозвращенных книг."""
        print("\n[Админ проверяет должников]")
        for r in readers:
            if r.books_on_hands:
                print(f"!!! {r.name} не вернул книгу! Вносим в черный список.")
                r.in_blacklist = True
            else:
                print(f"Чек: {r.name} — всё чисто.")


if __name__ == "__main__":
    print("\n--- ТЕСТ ---")
    catalog = Catalog()
    catalog.add_book(Book("Python для профи"))
    catalog.add_book(Book("Золотой Кодекс", is_rare=True))

    lib = Librarian()
    admin = Administrator()

    ivan = Reader("Иван")
    petr = Reader("Петр")

    order1 = ivan.create_order("Python для профи")
    lib.process_order(order1, catalog)

    order2 = petr.create_order("Золотой Кодекс")
    lib.process_order(order2, catalog)

    print("\n--- Проверка должников ---")
    admin.check_debts([ivan, petr])
