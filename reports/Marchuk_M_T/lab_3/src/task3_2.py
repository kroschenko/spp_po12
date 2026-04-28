"""
Модуль для реализации паттерна 'Адаптер'.
Позволяет использовать аналоговые часы как цифровые.
"""


class AnalogClock:
    """Класс оригинальных аналоговых часов."""

    def __init__(self, hours_angle: float):
        """Инициализация угла стрелки."""
        self.angle = hours_angle


class DigitalClockAdapter:
    """Класс-адаптер для преобразования формата времени."""

    def __init__(self, analog_clock: AnalogClock):
        """Принимает объект аналоговых часов."""
        self.analog_clock = analog_clock

    def get_digital_time(self) -> str:
        """
        Преобразует градусы в часы.
        :return: Строка времени HH:MM
        """
        # 30 градусов = 1 час
        hours = int(self.analog_clock.angle // 30)
        return f"{hours:02d}:00"


def main():
    """Точка входа в программу."""
    print("--- Адаптер часов ---")
    # 90 градусов соответствуют 3 часам
    analog = AnalogClock(90.0)
    adapter = DigitalClockAdapter(analog)
    print(f"Цифровое время на дисплее: {adapter.get_digital_time()}")


if __name__ == "__main__":
    main()
