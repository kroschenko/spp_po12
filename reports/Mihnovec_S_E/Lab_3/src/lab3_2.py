"""
Модуль реализует паттерн проектирования 'Адаптер'.
Позволяет использовать данные аналогового градусника (высота ртутного столба)
в интерфейсе электронного градусника (градусы Цельсия).
"""

from abc import ABC, abstractmethod


class AnalogThermometer:
    """
    Класс, представляющий аналоговый ртутный градусник.
    Хранит высоту ртутного столба и границы шкалы.
    """

    def __init__(self, mercury_height: float, min_bound: float = 0.0, max_bound: float = 100.0):
        self.mercury_height = mercury_height
        self.min_bound = min_bound
        self.max_bound = max_bound

    def get_mercury_level(self):
        """Возвращает текущий уровень ртути."""
        return self.mercury_height

    def get_limits(self):
        """Возвращает границы измерений прибора."""
        return self.min_bound, self.max_bound


class ElectronicThermometer(ABC):
    """
    Абстрактный интерфейс электронного градусника.
    Определяет методы для получения температуры и единиц измерения.
    """

    @abstractmethod
    def get_temperature_celsius(self) -> float:
        """Возвращает температуру в градусах Цельсия."""

    @abstractmethod
    def get_display_units(self) -> str:
        """Возвращает строку с единицей измерения."""


class AnalogToElectronicAdapter(ElectronicThermometer):
    """
    Адаптер, преобразующий данные аналогового градусника
    в формат электронного прибора.
    """

    def __init__(self, analog_thermometer: AnalogThermometer):
        self.analog = analog_thermometer
        # Заданные константы для перевода высоты в температуру
        self.min_temp_c = -30.0
        self.max_temp_c = 50.0

    def get_temperature_celsius(self) -> float:
        """
        Выполняет расчет температуры на основе высоты ртутного столба.
        Формула разбита на части для соблюдения длины строки (Pylint C0301).
        """
        span_analog = self.analog.max_bound - self.analog.min_bound
        relative_height = self.analog.mercury_height - self.analog.min_bound

        ratio = relative_height / span_analog
        temp_range = self.max_temp_c - self.min_temp_c
        temp_celsius = self.min_temp_c + (ratio * temp_range)

        return round(temp_celsius, 1)

    def get_display_units(self) -> str:
        """Реализация получения единиц измерения."""
        return "°C"


def main():
    """
    Основная функция для демонстрации работы адаптера.
    """
    print("--- Задача 2: Адаптер ---")
    analog_device = AnalogThermometer(mercury_height=65.0)
    adapter = AnalogToElectronicAdapter(analog_device)

    temp = adapter.get_temperature_celsius()
    unit = adapter.get_display_units()

    print(f"Высота ртутного столба: {analog_device.get_mercury_level()} мм.")
    print(f"Данные на электронном табло: {temp} {unit}")


if __name__ == "__main__":
    main()
