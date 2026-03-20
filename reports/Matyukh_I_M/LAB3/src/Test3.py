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

        print(f"\n🖨️ Идет струйная печать...")
        print(f"📊 Расход чернил: {pages * 0.5:.1f}% на копию")

        for copy in range(1, copies + 1):
            result.append(f"\n📄 Копия {copy}:")
            result.append("═" * 50)
            result.append(f"🖨️ Тип печати: {self.get_printer_type()}")
            result.append(f"⚙️ Качество: 1200 dpi (высокое)")
            result.append(f"📝 Текст документа:")
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

        print(f"\n🖨️ Идет лазерная печать...")
        print(f"📊 Расход тонера: {pages * 0.3:.1f}% на копию")

        for copy in range(1, copies + 1):
            result.append(f"\n📄 Копия {copy}:")
            result.append("═" * 50)
            result.append(f"🖨️ Тип печати: {self.get_printer_type()}")
            result.append(f"⚙️ Качество: 600 dpi (быстрая)")
            result.append(f"📝 Текст документа:")
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

        print(f"\n🖨️ Идет матричная печать (очень шумно)...")
        print(f"📊 Износ ленты: {pages * 0.8:.1f}% на копию")

        for copy in range(1, copies + 1):
            result.append(f"\n📄 Копия {copy}:")
            result.append("═" * 50)
            result.append(f"🖨️ Тип печати: {self.get_printer_type()}")
            result.append(f"⚙️ Режим: Черновик")
            result.append(f"📝 Текст документа:")
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
        print(f"\n🔄 Смена режима печати:")
        print(f"   Было: {old}")
        print(f"   Стало: {self._strategy.get_printer_type()}")

    def print_document(self, document_text, copies=1):
        self.print_count += copies

        print(f"\n{'=' * 60}")
        print(f"🖨️ ПРИНТЕР {self.model}")
        print(f"📊 Напечатано всего: {self.print_count} копий")
        print(f"{'=' * 60}")

        result = self._strategy.print_document(document_text, copies)
        print(f"\n✅ Печать завершена!")
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
            elif choice == 2:
                return LaserPrintStrategy()
            elif choice == 3:
                return DotMatrixPrintStrategy()
            else:
                print("Ошибка: введите число от 1 до 3")
        except ValueError:
            print("Ошибка: введите число")


def main():

    print("=" * 80)
    print("ПРОГРАММА: РАЗНЫЕ МОДЕЛИ ПРИНТЕРОВ")
    print("=" * 80)

    print("\n🔧 СОЗДАНИЕ ПРИНТЕРА")
    model = input("Введите модель принтера: ")
    strategy = get_printer_strategy()

    printer = Printer(model, strategy)
    print(f"\n✅ Принтер {model} создан!")
    print(printer.get_info())

    while True:
        print("\n" + "=" * 50)
        print("ДОСТУПНЫЕ ОПЕРАЦИИ:")
        print("1. Напечатать документ")
        print("2. Сменить тип принтера")
        print("3. Показать информацию о принтере")
        print("0. Выход")

        choice = input("\nВыберите операцию (0-3): ")

        if choice == "1":

            doc_text = input_document()

            try:
                copies = int(input("Введите количество копий: "))
                if copies < 1:
                    copies = 1
            except ValueError:
                print("Использовано значение по умолчанию: 1")
                copies = 1

            result = printer.print_document(doc_text, copies)
            print(result)

        elif choice == "2":

            new_strategy = get_printer_strategy()
            printer.set_strategy(new_strategy)

        elif choice == "3":
            print(printer.get_info())

        elif choice == "0":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

    print("\n" + "=" * 80)
    print(f"СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ ПРИНТЕРА {model}!")
    print("=" * 80)


if __name__ == "__main__":
    main()
