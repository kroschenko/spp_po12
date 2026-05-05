from abc import ABC, abstractmethod


class Car(ABC):

    def __init__(self, brand):
        self.brand = brand
        self.engine_started = False
        self.doors_open = False
        self.alarm_on = False

    def start_engine(self):
        self.engine_started = True
        print(f"{self.brand}: Двигатель запущен")

    def stop_engine(self):
        self.engine_started = False
        print(f"{self.brand}: Двигатель остановлен")

    def open_doors(self):
        self.doors_open = True
        print(f"{self.brand}: Двери открыты")

    def close_doors(self):
        self.doors_open = False
        print(f"{self.brand}: Двери закрыты")

    def alarm_on_func(self):
        self.alarm_on = True
        print(f"{self.brand}: Сигнализация включена")

    def alarm_off_func(self):
        self.alarm_on = False
        print(f"{self.brand}: Сигнализация отключена")


class BMW(Car):
    def __init__(self):
        super().__init__("BMW")


class Toyota(Car):
    def __init__(self):
        super().__init__("Toyota")


class Audi(Car):
    def __init__(self):
        super().__init__("Audi")


class RemoteControl(ABC):

    def __init__(self, car):
        self.car = car

    @abstractmethod
    def alarm(self):
        pass

    @abstractmethod
    def doors(self):
        pass

    @abstractmethod
    def engine(self):
        pass


class StandardRemote(RemoteControl):

    def alarm(self):
        print("Стандартный пульт:")
        self.car.alarm_on_func()

    def doors(self):
        print("Стандартный пульт:")
        self.car.open_doors()

    def engine(self):
        print("Стандартный пульт: запуск двигателя запрещен")


class PremiumRemote(RemoteControl):

    def alarm(self):
        print("Премиум пульт:")
        self.car.alarm_on_func()

    def doors(self):
        print("Премиум пульт:")
        self.car.open_doors()

    def engine(self):
        print("Премиум пульт:")
        self.car.start_engine()


class SmartRemote(RemoteControl):

    def alarm(self):
        print("Смарт пульт:")
        self.car.alarm_on_func()
        print("Уведомление отправлено на телефон")

    def doors(self):
        print("Смарт пульт:")
        self.car.open_doors()

    def engine(self):
        print("Смарт пульт:")
        self.car.start_engine()
        print("Контроль температуры салона включен")


def choose_car():
    print("1. BMW")
    print("2. Toyota")
    print("3. Audi")

    car_choice = input("Выберите автомобиль: ")

    if car_choice == "1":
        return BMW()
    if car_choice == "2":
        return Toyota()
    if car_choice == "3":
        return Audi()

    return None


def choose_remote(car):
    if car is None:
        print("Сначала выберите автомобиль")
        return None

    print("1. Стандартный пульт")
    print("2. Премиум пульт")
    print("3. Смарт пульт")

    remote_choice = input("Выберите пульт: ")

    if remote_choice == "1":
        return StandardRemote(car)
    if remote_choice == "2":
        return PremiumRemote(car)
    if remote_choice == "3":
        return SmartRemote(car)

    return None


def remote_action(remote, action):
    if not remote:
        print("Сначала выберите пульт")
        return

    if action == "alarm":
        remote.alarm()
    elif action == "doors":
        remote.doors()
    elif action == "engine":
        remote.engine()


def main():

    car = None
    remote = None

    while True:
        print("\nМеню:")
        print("1. Выбрать автомобиль")
        print("2. Выбрать пульт")
        print("3. Включить сигнализацию")
        print("4. Открыть двери")
        print("5. Запустить двигатель")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            car = choose_car()

        elif choice == "2":
            remote = choose_remote(car)

        elif choice == "3":
            remote_action(remote, "alarm")

        elif choice == "4":
            remote_action(remote, "doors")

        elif choice == "5":
            remote_action(remote, "engine")

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
