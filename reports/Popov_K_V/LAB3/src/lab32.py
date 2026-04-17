"""
Модуль реализует структурный паттерн проектирования Адаптер (Adapter).
Позволяет использовать интерфейс аналоговых часов (градусы) в системе,
ожидающей цифровой формат времени.
"""
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod


class DigitalClock(ABC):
    """Абстрактный класс цифровых часов."""

    @abstractmethod
    def get_digital_time(self) -> str:
        """Возвращает время в формате HH:MM."""


# === 2. Цифровые часы ===
class SimpleDigitalClock(DigitalClock):
    """Класс стандартных цифровых часов."""

    def __init__(self, hours: int, minutes: int):
        self.hours = hours % 24
        self.minutes = minutes % 60

    def get_digital_time(self) -> str:
        """Возвращает время в строковом представлении."""
        return f"{self.hours:02d}:{self.minutes:02d}"


class AnalogClock:
    """Класс аналоговых часов, работающий с углами поворота стрелок."""

    def __init__(self, hour_angle: float, minute_angle: float):
        self.hour_angle = hour_angle % 360
        self.minute_angle = minute_angle % 360

    def get_angles(self) -> tuple:
        """Возвращает текущие углы поворота часовой и минутной стрелок."""
        return self.hour_angle, self.minute_angle


class AnalogToDigitalAdapter(DigitalClock):
    """Адаптер, преобразующий данные аналоговых часов в цифровой формат."""

    def __init__(self, analog_clock: AnalogClock):
        self.analog = analog_clock

    def get_digital_time(self) -> str:
        """Математически переводит градусы в часы/минуты и возвращает строку."""
        hour_angle, minute_angle = self.analog.get_angles()

        minutes = int(minute_angle // 6)

        hours = int(hour_angle // 30)
        hours = 12 if hours == 0 else hours

        return f"{hours:02d}:{minutes:02d}"


def display_time(clock: DigitalClock):
    """Функция для демонстрации времени, принимающая объект DigitalClock."""
    print(f"Время: {clock.get_digital_time()}")


if __name__ == "__main__":
    display_time(SimpleDigitalClock(14, 30))

    analog_inst = AnalogClock(187.5, 90.0)
    display_time(AnalogToDigitalAdapter(analog_inst))
