"""Модуль с реализацией паттерна Адаптер для термометра."""
from abc import ABC, abstractmethod


class ElectronicThermometer(ABC):  # pylint: disable=R0903
    """Абстрактный класс для электронного термометра."""

    @abstractmethod
    def get_temperature(self) -> float:
        """Возвращает температуру в градусах Цельсия."""


class AnalogThermometer:  # pylint: disable=R0903
    """Аналоговый термометр со своей логикой измерения."""

    def __init__(self, min_temp: float, max_temp: float, max_height_mm: float):
        """Инициализирует аналоговый термометр."""
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.max_height_mm = max_height_mm
        self._current_mercury_height = 0.0

    def set_mercury_level(self, height_mm: float):
        """Устанавливает текущий уровень ртути."""
        if height_mm > self.max_height_mm:
            self._current_mercury_height = self.max_height_mm
        elif height_mm < 0:
            self._current_mercury_height = 0
        else:
            self._current_mercury_height = height_mm

    def get_mercury_height(self) -> float:
        """Возвращает высоту ртутного столба в мм."""
        return self._current_mercury_height


class ThermometerAdapter(ElectronicThermometer):  # pylint: disable=R0903
    """Адаптер для преобразования показаний аналогового термометра."""

    def __init__(self, analog_thermometer: AnalogThermometer):
        """Инициализирует адаптер с аналоговым термометром."""
        self.analog_thermometer = analog_thermometer

    def get_temperature(self) -> float:
        """Возвращает температуру в градусах Цельсия."""
        height = self.analog_thermometer.get_mercury_height()
        max_h = self.analog_thermometer.max_height_mm
        min_t = self.analog_thermometer.min_temp
        max_t = self.analog_thermometer.max_temp

        percentage = height / max_h
        temperature = min_t + (max_t - min_t) * percentage

        return round(temperature, 1)


if __name__ == "__main__":
    old_thermometer = AnalogThermometer(
        min_temp=-30, max_temp=50, max_height_mm=200
    )

    old_thermometer.set_mercury_level(150)

    adapter = ThermometerAdapter(old_thermometer)

    print(
        f"Показания аналогового прибора (высота): "
        f"{old_thermometer.get_mercury_height()} мм"
    )
    print(
        f"Показания через адаптер (электронный вид): "
        f"{adapter.get_temperature()} °C"
    )

    old_thermometer.set_mercury_level(75)
    print(f"\nНовые показания через адаптер: {adapter.get_temperature()} °C")
