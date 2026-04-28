"""
Проект Часы.
Структурный паттерн: Adapter (Адаптер).
"""


class AnalogClock:
    """Часы со стрелками. Хранит повороты стрелок в градусах."""

    def __init__(self, hours_angle: float = 0, minutes_angle: float = 0):
        self.hours_angle = hours_angle % 360
        self.minutes_angle = minutes_angle % 360
        self._sync_time()

    def _sync_time(self):
        """Синхронизирует время на основе углов стрелок."""
        self.hours = (self.hours_angle / 30) % 12
        self.minutes = (self.minutes_angle / 6) % 60
        self.seconds = 0

    def set_time_by_angles(self, hours_angle: float, minutes_angle: float):
        """Установить время по углам стрелок."""
        self.hours_angle = hours_angle % 360
        self.minutes_angle = minutes_angle % 360
        self._sync_time()

    def set_hours_angle(self, angle: float):
        """Установить угол часовой стрелки."""
        self.hours_angle = angle % 360
        self._sync_time()

    def set_minutes_angle(self, angle: float):
        """Установить угол минутной стрелки."""
        self.minutes_angle = angle % 360
        self._sync_time()

    def get_hours_angle(self) -> float:
        """Получить угол часовой стрелки."""
        return self.hours_angle

    def get_minutes_angle(self) -> float:
        """Получить угол минутной стрелки."""
        return self.minutes_angle

    def get_time(self):
        """Получить время в формате (часы, минуты)."""
        return int(self.hours), int(self.minutes)

    def __str__(self):
        hours_int = int(self.hours)
        minutes_int = int(self.minutes)
        return (
            f"Аналоговые часы: {hours_int:02d}:{minutes_int:02d} "
            f"(часы: {self.hours_angle:.1f}°, минуты: {self.minutes_angle:.1f}°)"
        )


class DigitalClockInterface:
    """Интерфейс цифровых часов."""

    def display_time(self) -> str:
        """Отобразить время в цифровом формате."""
        raise NotImplementedError

    def set_time(self, hours: int, minutes: int):
        """Установить время."""
        raise NotImplementedError


class DigitalClock(DigitalClockInterface):
    """Цифровые часы."""

    def __init__(self, hours: int = 0, minutes: int = 0):
        self.hours = hours % 24
        self.minutes = minutes % 60

    def display_time(self) -> str:
        """Отобразить время."""
        return f"{self.hours:02d}:{self.minutes:02d}"

    def set_time(self, hours: int, minutes: int):
        """Установить время."""
        self.hours = hours % 24
        self.minutes = minutes % 60

    def __str__(self):
        return f"Цифровые часы: {self.display_time()}"


class AnalogToDigitalAdapter(DigitalClockInterface):
    """Адаптер, позволяющий использовать аналоговые часы как цифровые."""

    def __init__(self, analog_clock: AnalogClock):
        self.analog_clock = analog_clock

    def display_time(self) -> str:
        """Отобразить время из аналоговых часов в цифровом формате."""
        hours, minutes = self.analog_clock.get_time()
        return f"{hours:02d}:{minutes:02d}"

    def set_time(self, hours: int, minutes: int):
        """Установить время на аналоговых часах через цифровой интерфейс."""
        hours_angle = (hours % 12) * 30
        minutes_angle = minutes * 6
        self.analog_clock.set_time_by_angles(hours_angle, minutes_angle)

    def get_analog_clock(self) -> AnalogClock:
        """Получить оригинальные аналоговые часы."""
        return self.analog_clock


def main():
    """Основная функция."""
    print("=" * 60)
    print("ПРОЕКТ ЧАСЫ - АДАПТЕР")
    print("=" * 60)

    print("\n1. СОЗДАНИЕ АНАЛОГОВЫХ ЧАСОВ")
    analog = AnalogClock()
    print(analog)

    print("\n2. УСТАНОВКА ВРЕМЕНИ НА АНАЛОГОВЫХ ЧАСАХ")
    hours = int(input("Введите часы (0-12): "))
    minutes = int(input("Введите минуты (0-60): "))
    analog.set_time_by_angles(hours * 30, minutes * 6)
    print(analog)

    print("\n3. СОЗДАНИЕ АДАПТЕРА")
    adapter = AnalogToDigitalAdapter(analog)
    print(f"Адаптер показывает время: {adapter.display_time()}")

    print("\n4. УСТАНОВКА ВРЕМЕНИ ЧЕРЕЗ АДАПТЕР")
    new_hours = int(input("Введите новые часы (0-23): "))
    new_minutes = int(input("Введите новые минуты (0-60): "))
    adapter.set_time(new_hours, new_minutes)

    print("\n5. ПРОВЕРКА РЕЗУЛЬТАТА")
    print(f"Адаптер показывает: {adapter.display_time()}")
    print(f"Оригинальные аналоговые часы: {adapter.get_analog_clock()}")

    print("\n6. ДЕМОНСТРАЦИЯ РАБОТЫ С ЦИФРОВЫМИ ЧАСАМИ")
    digital = DigitalClock()
    digital.set_time(new_hours, new_minutes)
    print(f"Цифровые часы: {digital}")

    print("\nАдаптер позволяет использовать аналоговые часы")
    print("там же, где ожидаются цифровые часы.")


if __name__ == "__main__":
    main()
