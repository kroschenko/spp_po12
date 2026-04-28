from abc import ABC, abstractmethod


class DigitalClockInterface(ABC):
    @abstractmethod
    def set_time(self, hours: int, minutes: int, seconds: int) -> None:
        """Установить время."""
        raise NotImplementedError

    @abstractmethod
    def get_time(self) -> str:
        """Получить время в цифровом формате."""
        raise NotImplementedError


class AnalogClock:

    def __init__(self) -> None:
        self.hour_angle = 0.0
        self.minute_angle = 0.0
        self.second_angle = 0.0

    def set_angles(
        self,
        hour_angle: float,
        minute_angle: float,
        second_angle: float,
    ) -> None:
        """Установить углы стрелок."""
        self.hour_angle = hour_angle % 360
        self.minute_angle = minute_angle % 360
        self.second_angle = second_angle % 360

    def get_angles(self) -> tuple[float, float, float]:
        """Получить углы стрелок."""
        return self.hour_angle, self.minute_angle, self.second_angle


class ClockAdapter(DigitalClockInterface):
    """Адаптер, позволяющий работать с аналоговыми часами как с цифровыми."""

    def __init__(self, source_clock: AnalogClock) -> None:
        self.source_clock = source_clock

    def set_time(self, hours: int, minutes: int, seconds: int) -> None:
        """Установить время в формате часы:минуты:секунды."""
        if not 0 <= hours <= 23:
            raise ValueError("Часы должны быть в диапазоне 0..23")
        if not 0 <= minutes <= 59:
            raise ValueError("Минуты должны быть в диапазоне 0..59")
        if not 0 <= seconds <= 59:
            raise ValueError("Секунды должны быть в диапазоне 0..59")

        normalized_hours = hours % 12

        second_angle = seconds * 6
        minute_angle = minutes * 6 + seconds * 0.1
        hour_angle = normalized_hours * 30 + minutes * 0.5 + seconds * (0.5 / 60)

        self.source_clock.set_angles(hour_angle, minute_angle, second_angle)

    def get_time(self) -> str:
        """Получить время в цифровом виде."""
        hour_angle, minute_angle, second_angle = self.source_clock.get_angles()

        seconds = round(second_angle / 6) % 60
        minutes = int(minute_angle / 6) % 60
        hours = int(hour_angle / 30) % 12

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_full_info(self) -> str:
        """Получить время и углы стрелок."""
        hour_angle, minute_angle, second_angle = self.source_clock.get_angles()
        return (
            f"Текущее цифровое время: {self.get_time()}\n"
            f"Углы стрелок:\n"
            f"  Часовая стрелка: {hour_angle:.2f}°\n"
            f"  Минутная стрелка: {minute_angle:.2f}°\n"
            f"  Секундная стрелка: {second_angle:.2f}°"
        )


if __name__ == "__main__":
    clock_model = AnalogClock()
    clock_adapter = ClockAdapter(clock_model)

    clock_adapter.set_time(10, 25, 30)
    print(clock_adapter.get_full_info())

    print("\nИзменим время:")
    clock_adapter.set_time(3, 45, 0)
    print(clock_adapter.get_full_info())
