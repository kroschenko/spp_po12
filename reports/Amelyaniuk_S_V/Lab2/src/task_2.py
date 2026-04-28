class Book:
    def __init__(self, title, is_rare=False):
        self.title = title
        self.is_rare = is_rare 

    def __repr__(self):
        type_str = "(Редкая)" if self.is_rare else ""
        return f"Книга '{self.title}' {type_str}"

class Order:
    def __init__(self, reader, book_title):
        self.reader = reader
        self.book_title = book_title


class Catalog:
    def __init__(self):
        self.books = {} 

    def add_book(self, book):
        self.books[book.title] = book

    def find(self, title):
        return self.books.get(title)

class Reader:
    def __init__(self, name):
        self.name = name
        self.books_on_hands = []
        self.in_blacklist = False

    def create_order(self, book_title):
        return Order(self, book_title)

    def receive_book(self, book):
        self.books_on_hands.append(book)

    def return_book(self, title):
        for b in self.books_on_hands:
            if b.title == title:
                self.books_on_hands.remove(b)
                return True
        return False

    def __str__(self):
        status = "[В ЧЕРНОМ СПИСКЕ]" if self.in_blacklist else "[OK]"
        return f"Читатель: {self.name} {status}. Книг на руках: {len(self.books_on_hands)}"

class Librarian:
    def process_order(self, order, catalog):
        reader = order.reader
        
        if reader.in_blacklist:
            print(f"Библиотекарь: отказ. {reader.name} в черном списке.")
            return

        book = catalog.find(order.book_title)
        if not book:
            print(f"Библиотекарь: Книги '{order.book_title}' нет в каталоге.")
            return

        place = "в Читальный зал" if book.is_rare else "на Абонемент"
        print(f"Библиотекарь: Выдаю '{book.title}' {place} читателю {reader.name}.")
        reader.receive_book(book)

class Administrator:
    def check_debts(self, readers):
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

    ivan.return_book("Python для профи")

    admin.check_debts([ivan, petr])

    order3 = petr.create_order("Python для профи")
    lib.process_order(order3, catalog)