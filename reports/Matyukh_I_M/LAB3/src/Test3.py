from abc import ABC, abstractmethod
from datetime import datetime


class PrintStrategy(ABC):
    @abstractmethod
    def print_document(self, document_text, copies=1):
        pass

    @abstractmethod
    def get_printer_type(self):
        pass

    @abstractmethod
    def get_cost_per_page(self):
        pass


class InkjetPrintStrategy(PrintStrategy):
    def __init__(self):
        self.ink_level = 100
        self.name = "Струйный принтер"

    def print_document(self, document_text, copies=1):
        result = []
        pages = max(1, len(document_text) // 1000 + 1)

        print("\n🖨️ Идет струйная печать...")
        print(f"📊 Расход чернил: {pages * 0.5:.1f}% на копию")

        for copy in range(1, copies + 1):
            result.append(f"\n📄 Копия {copy}:")
            result.append("═" * 50)
            result.append(f"🖨️ Тип печати: {self.get_printer_type()}")
            result.append("⚙️ Качество: 1200 dpi (высокое)")
            result.append("📝 Текст документа:")
            result.append(f"   {document_text}")
            result.append(
                f"💰 Стоимость копии: {pages * self.get_cost_per_page():.2f} руб."
            )

            self.ink_level -= pages * 0.5

        return "\n".join(result)

    def get_printer_type(self):
        return f"{self.name} (чернила: {max(0, self.ink_level):.1f}%)"

    def get_cost_per_page(self):
        return 2.5


class LaserPrintStrategy(PrintStrategy):
    def __init__(self):
        self.toner_level = 100
        self.name = "Лазерный принтер"

    def print_document(self, document_text, copies=1):
        result = []
        pages = max(1, len(document_text) // 1500 + 1)

        print("\n🖨️ Идет лазерная печать...")
        print(f"📊 Расход тонера: {pages * 0.3:.1f}% на копию")

        for copy in range(1, copies + 1):
            result.append(f"\n📄 Копия {copy}:")
            result.append("═" * 50)
            result.append(f"🖨️ Тип печати: {self.get_printer_type()}")
            result.append("⚙️ Качество: 600 dpi (быстрая)")
            result.append("📝 Текст документа:")
            result.append(f"   {document_text}")
            result.append(
                f"💰 Стоимость копии: {pages * self.get_cost_per_page():.2f} руб."
            )

            self.toner_level -= pages * 0.3

        return "\n".join(result)

    def get_printer_type(self):
        return f"{self.name} (тонер: {max(0, self.toner_level):.1f}%)"

    def get_cost_per_page(self):
        return 1.8


class DotMatrixPrintStrategy(PrintStrategy):
    def __init__(self):
        self.ribbon_level = 100
        self.name = "Матричный принтер"

    def print_document(self, document_text, copies=1):
        result = []
        pages = max(1, len(document_text) // 800 + 1)

        print("\n🖨️ Идет матричная печать (очень шумно)...")
        print(f"📊 Износ ленты: {pages * 0.8:.1f}% на копию")

        for copy in range(1, copies + 1):
            result.append(f"\n📄 Копия {copy}:")
            result.append("═" * 50)
            result.append(f"🖨️ Тип печати: {self.get_printer_type()}")
            result.append("⚙️ Режим: Черновик")
            result.append("📝 Текст документа:")
            result.append(f"   {document_text}")
            result.append(
                f"💰 Стоимость копии: {pages * self.get_cost_per_page():.2f} руб."
            )

            self.ribbon_level -= pages * 0.8

        return "\n".join(result)

    def get_printer_type(self):
        return f"{self.name} (лента: {max(0, self.ribbon_level):.1f}%)"

    def get_cost_per_page(self):
        return 0.9


class Printer:
    def __init__(self, model, strategy: PrintStrategy):
        self.model = model
        self._strategy = strategy
        self.print_count = 0
        self.last_maintenance = datetime.now()

    def set_strategy(self, strategy: PrintStrategy):
        old = self._strategy.get_printer_type()
        self._strategy = strategy
        print("\n🔄 Смена режима печати:")
        print(f"   Было: {old}")
        print(f"   Стало: {self._strategy.get_printer_type()}")

    def print_document(self, document_text, copies=1):
        copies = max(copies, 1)
        self.print_count += copies

        print(f"\n{'=' * 60}")
        print(f"🖨️ ПРИНТЕР {self.model}")
        print(f"📊 Напечатано всего: {self.print_count} копий")
        print(f"{'=' * 60}")

        result = self._strategy.print_document(document_text, copies)
        print("\n✅ Печать завершена!")
        return result

    def get_info(self):
        return f"""
╔══════════════════════════════════════════════╗
║   ИНФОРМАЦИЯ О ПРИНТЕРЕ
╠══════════════════════════════════════════════╣
║ Модель: {self.model}
║ Тип: {self._strategy.get_printer_type()}
║ Напечатано: {self.print_count} копий
║ Последнее обслуживание: {self.last_maintenance.strftime('%d.%m.%Y')}
╚══════════════════════════════════════════════╝
        """


def input_document():
    print("\n📝 ВВОД ДОКУМЕНТА:")
    print("(введите текст документа, для завершения введите 'end' на отдельной строке)")

    lines = []
    while True:
        line = input()
        if line == "end":
            break
        lines.append(line)

    return "\n".join(lines) if lines else input("Введите текст документа: ")


def get_printer_strategy():
    print("\n🖨️ ДОСТУПНЫЕ ТИПЫ ПРИНТЕРОВ:")
    print("1. Струйный принтер (для фотографий и цветной печати)")
    print("2. Лазерный принтер (для документов, быстро и дешево)")
    print("3. Матричный принтер (для накладных, шумно но надежно)")

    while True:
        try:
            choice = int(input("\nВыберите тип принтера (1-3): "))
            if choice == 1:
                return InkjetPrintStrategy()
            if choice == 2:
                return LaserPrintStrategy()
            if choice == 3:
                return DotMatrixPrintStrategy()
            print("Ошибка: введите число от 1 до 3")
        except ValueError:
            print("Ошибка: введите число")


def create_printer():
    print("\n🔧 СОЗДАНИЕ ПРИНТЕРА")
    model = input("Введите модель принтера: ")
    strategy = get_printer_strategy()

    printer = Printer(model, strategy)
    print(f"\n✅ Принтер {model} создан!")
    print(printer.get_info())
    return printer


def get_copies_count():
    try:
        copies = int(input("Введите количество копий: "))
        return max(copies, 1)
    except ValueError:
        print("Использовано значение по умолчанию: 1")
        return 1


def show_menu():
    print("\n" + "=" * 50)
    print("ДОСТУПНЫЕ ОПЕРАЦИИ:")
    print("1. Напечатать документ")
    print("2. Сменить тип принтера")
    print("3. Показать информацию о принтере")
    print("0. Выход")


def process_menu_choice(printer, choice):
    if choice == "1":
        doc_text = input_document()
        copies = get_copies_count()
        result = printer.print_document(doc_text, copies)
        print(result)
    elif choice == "2":
        new_strategy = get_printer_strategy()
        printer.set_strategy(new_strategy)
    elif choice == "3":
        print(printer.get_info())
    elif choice == "0":
        return False
    else:
        print("Неверный выбор. Попробуйте снова.")
    return True


def run_printer_menu(printer):
    while True:
        show_menu()
        choice = input("\nВыберите операцию (0-3): ")
        if not process_menu_choice(printer, choice):
            break


def main():
    print("=" * 80)
    print("ПРОГРАММА: РАЗНЫЕ МОДЕЛИ ПРИНТЕРОВ")
    print("=" * 80)

    printer = create_printer()
    run_printer_menu(printer)

    print("\n" + "=" * 80)
    print(f"СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ ПРИНТЕРА {printer.model}!")
    print("=" * 80)


if __name__ == "__main__":
    main()
