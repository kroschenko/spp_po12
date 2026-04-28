from abc import ABC, abstractmethod


class RemoteControl(ABC):
    @abstractmethod
    def activate_alarm(self, car_model):
        pass

    @abstractmethod
    def remote_lock_doors(self, car_model):
        pass

    @abstractmethod
    def remote_start_engine(self, car_model):
        pass


class PremiumRemote(RemoteControl):
    def activate_alarm(self, car_model):
        return f"{car_model}: Сигнализация активирована (дальность 500м, датчик удара, GPS-трекинг)"

    def remote_lock_doors(self, car_model):
        return f"{car_model}: Двери заблокированы + автоматическое закрытие окон и складывание зеркал"

    def remote_start_engine(self, car_model):
        return f"{car_model}: Двигатель запущен (автозапуск, климат-контроль, подогрев сидений)"


class StandardRemote(RemoteControl):
    def activate_alarm(self, car_model):
        return f"{car_model}: Сигнализация активирована (дальность 100м, звуковой сигнал)"

    def remote_lock_doors(self, car_model):
        return f"{car_model}: Двери заблокированы"

    def remote_start_engine(self, car_model):
        return f"{car_model}: Двигатель запущен (требуется нажатие кнопки в зоне видимости)"


class BasicRemote(RemoteControl):
    def activate_alarm(self, car_model):
        return f"{car_model}: Сигнализация активирована (дальность 30м)"

    def remote_lock_doors(self, car_model):
        return f"{car_model}: Двери заблокированы (только центральный замок)"

    def remote_start_engine(self, car_model):
        return f"{car_model}: Запуск двигателя не поддерживается данным пультом"


class Car:
    def __init__(self, model, remote):
        self.model = model
        self._remote = remote
        self.engine_running = False
        self.doors_locked = False
        self.alarm_active = False

    def activate_alarm(self):
        result = self._remote.activate_alarm(self.model)
        self.alarm_active = True
        return result

    def lock_doors(self):
        result = self._remote.remote_lock_doors(self.model)
        self.doors_locked = True
        return result

    def unlock_doors(self):
        self.doors_locked = False
        return f"{self.model}: Двери разблокированы"

    def start_engine(self):
        result = self._remote.remote_start_engine(self.model)
        if "запущен" in result or "Запущен" in result:
            self.engine_running = True
        return result

    def stop_engine(self):
        self.engine_running = False
        return f"{self.model}: Двигатель остановлен"

    def get_status(self):
        return {
            "model": self.model,
            "engine": "работает" if self.engine_running else "выключен",
            "doors": "закрыты" if self.doors_locked else "открыты",
            "alarm": "активна" if self.alarm_active else "выключена"
        }


class BMW(Car):
    def __init__(self, model, remote):
        super().__init__(f"BMW {model}", remote)
        self.manufacturer = "BMW"
        self.has_comfort_access = True


class Tesla(Car):
    def __init__(self, model, remote):
        super().__init__(f"Tesla {model}", remote)
        self.manufacturer = "Tesla"
        self.has_electric_mode = True


class Toyota(Car):
    def __init__(self, model, remote):
        super().__init__(f"Toyota {model}", remote)
        self.manufacturer = "Toyota"
        self.has_economy_mode = True


if __name__ == "__main__":
    print("--- Комбинация 1: BMW X5 + Премиум пульт ---")
    bmw = BMW("X5", PremiumRemote())
    print(bmw.activate_alarm())
    print(bmw.lock_doors())
    print(bmw.start_engine())
    print(bmw.get_status())

    print("\n--- Комбинация 2: Tesla Model 3 + Стандартный пульт ---")
    tesla = Tesla("Model 3", StandardRemote())
    print(tesla.activate_alarm())
    print(tesla.lock_doors())
    print(tesla.start_engine())
    print(tesla.get_status())

    print("\n--- Комбинация 3: Toyota Camry + Базовый пульт ---")
    toyota = Toyota("Camry", BasicRemote())
    print(toyota.activate_alarm())
    print(toyota.lock_doors())
    print(toyota.start_engine())
    print(toyota.get_status())

    print("\n--- Смена пульта на лету ---")
    print("Toyota теперь получает премиум пульт:")
    toyota._remote = PremiumRemote()
    print(toyota.start_engine())
    print(toyota.get_status())
