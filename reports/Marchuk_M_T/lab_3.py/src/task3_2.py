"""
Задание 2: Проект 'Часы' (Паттерн: Адаптер).
Адаптирует аналоговые часы (градусы) под цифровой формат (HH:MM).
"""
class AnalogClock:
    def __init__(self, hours_angle):
        self.angle = hours_angle # Угол часовой стрелки

class DigitalClockAdapter:
    def __init__(self, analog_clock):
        self.analog_clock = analog_clock

    def get_time(self):
        # 30 градусов = 1 час
        hours = int(self.analog_clock.angle // 30)
        return f"{hours:02d}:00"

if __name__ == "__main__":
    analog = AnalogClock(90) # 90 градусов = 3 часа
    adapter = DigitalClockAdapter(analog)
    print(f"Цифровое время: {adapter.get_time()}")
