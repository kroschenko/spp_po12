class AnalogThermometer:
    def __init__(self, min_temp, max_temp):
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.height = 0

    def set_height(self, height):
        if 0 <= height <= 100:
            self.height = height

    def get_height(self):
        return self.height

    def get_range(self):
        return self.min_temp, self.max_temp


class ElectronicThermometer:
    def get_temperature(self):
        pass


class ThermometerAdapter(ElectronicThermometer):
    def __init__(self, analog_thermometer):
        self.analog = analog_thermometer

    def get_temperature(self):
        min_temp, max_temp = self.analog.get_range()
        height = self.analog.get_height()
        temperature = min_temp + (height / 100) * (max_temp - min_temp)
        return round(temperature, 1)


class DigitalThermometer(ElectronicThermometer):
    def __init__(self):
        self.temperature = 22.5

    def get_temperature(self):
        return self.temperature

    def set_temperature(self, temp):
        self.temperature = temp


if __name__ == "__main__":
    analog = AnalogThermometer(-20, 40)
    analog.set_height(75)

    adapter = ThermometerAdapter(analog)
    print(f"Аналоговый как электронный: {adapter.get_temperature()}°C")

    digital = DigitalThermometer()
    print(f"Цифровой: {digital.get_temperature()}°C")
