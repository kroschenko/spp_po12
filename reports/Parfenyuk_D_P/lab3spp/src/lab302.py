"""
Модуль для лабораторной работы №3.
Задание 2 (Структурный паттерн: Мост).
Вариант 7: Дистанционное управление автомобилем.
"""

# pylint: disable=too-few-public-methods


class Car:
    """Базовый класс реализации автомобиля."""

    def activate_alarm(self):
        """Метод для включения сигнализации."""

    def toggle_doors(self):
        """Метод для управления дверями."""

    def start_engine(self):
        """Метод для запуска двигателя."""


class BMW(Car):
    """Реализация функций для автомобиля марки BMW."""

    def activate_alarm(self):
        """Включение сигнализации BMW."""
        print("[BMW] Сигнализация включена: звучит громкий сигнал.")

    def toggle_doors(self):
        """Управление дверями BMW."""
        print("[BMW] Двери заблокированы/разблокированы (плавный доводчик).")

    def start_engine(self):
        """Запуск двигателя BMW."""
        print("[BMW] Двигатель запущен: V8 готов к работе.")


class Audi(Car):
    """Реализация функций для автомобиля марки Audi."""

    def activate_alarm(self):
        """Включение сигнализации Audi."""
        print("[Audi] Сигнализация активна: мигают фары.")

    def toggle_doors(self):
        """Управление дверями Audi."""
        print("[Audi] Центральный замок сработал.")

    def start_engine(self):
        """Запуск двигателя Audi."""
        print("[Audi] Двигатель запущен кнопкой Start/Stop.")


class RemoteControl:
    """Абстракция пульта дистанционного управления."""

    def __init__(self, car):
        """Инициализация пульта конкретным автомобилем."""
        self.car = car

    def press_alarm_button(self):
        """Нажатие кнопки сигнализации."""
        self.car.activate_alarm()

    def press_door_button(self):
        """Нажатие кнопки дверей."""
        self.car.toggle_doors()

    def press_start_button(self):
        """Нажатие кнопки запуска двигателя."""
        self.car.start_engine()


def main():
    """Основная функция с интерактивным меню."""
    print("--- ВЫБОР АВТОМОБИЛЯ ---")
    print("1. Управлять BMW")
    print("2. Управлять Audi")
    brand_choice = input("Выберите марку: ")

    if brand_choice == "1":
        current_car = BMW()
    else:
        current_car = Audi()

    remote = RemoteControl(current_car)

    while True:
        print("\n--- КНОПКИ ПУЛЬТА ДУ ---")
        print("1. Сигнализация")
        print("2. Двери")
        print("3. Запуск двигателя")
        print("0. Выход")

        button = input("Нажмите кнопку на пульте: ")

        if button == "1":
            remote.press_alarm_button()
        elif button == "2":
            remote.press_door_button()
        elif button == "3":
            remote.press_start_button()
        elif button == "0":
            break
        else:
            print("Ошибка: на пульте нет такой кнопки.")


if __name__ == "__main__":
    main()
