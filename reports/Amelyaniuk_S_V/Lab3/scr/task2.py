from abc import ABC, abstractmethod

# --- Целевой интерфейс (Target) ---
class ElectronicThermometer(ABC):
    @abstractmethod
    def get_temperature(self) -> float:
        pass


# --- Адаптируемый класс (Adaptee) ---
# Аналоговый градусник со своей логикой
class AnalogThermometer:
    def __init__(self, min_temp: float, max_temp: float, max_height_mm: float):
        self.min_temp = min_temp      # Нижняя граница (например, -10)
        self.max_temp = max_temp      # Верхняя граница (например, +50)
        self.max_height_mm = max_height_mm  # Максимально возможная высота столба
        self._current_mercury_height = 0.0

    def set_mercury_level(self, height_mm: float):
        """Установка текущего уровня ртути (физический процесс)"""
        if height_mm > self.max_height_mm:
            self._current_mercury_height = self.max_height_mm
        elif height_mm < 0:
            self._current_mercury_height = 0
        else:
            self._current_mercury_height = height_mm

    def get_mercury_height(self) -> float:
        """Возвращает только высоту, но не температуру"""
        return self._current_mercury_height


# --- Адаптер (Adapter) ---
class ThermometerAdapter(ElectronicThermometer):
    def __init__(self, analog_thermometer: AnalogThermometer):
        self.analog_thermometer = analog_thermometer

    def get_temperature(self) -> float:
        
        height = self.analog_thermometer.get_mercury_height()
        max_h = self.analog_thermometer.max_height_mm
        min_t = self.analog_thermometer.min_temp
        max_t = self.analog_thermometer.max_temp

        # Формула: Т_мин + (Т_диапазон * (Тек_высота / Макс_высота))
        percentage = height / max_h
        temperature = min_t + (max_t - min_t) * percentage
        
        return round(temperature, 1)


# --- Клиентский код ---
if __name__ == "__main__":
    old_thermometer = AnalogThermometer(min_temp=-30, max_temp=50, max_height_mm=200)
    
    old_thermometer.set_mercury_level(150)

    adapter = ThermometerAdapter(old_thermometer)

    print(f"Показания аналогового прибора (высота): {old_thermometer.get_mercury_height()} мм")
    print(f"Показания через адаптер (электронный вид): {adapter.get_temperature()} °C")

    # 4. Изменим уровень ртути
    old_thermometer.set_mercury_level(75)
    print(f"\nНовые показания через адаптер: {adapter.get_temperature()} °C")
