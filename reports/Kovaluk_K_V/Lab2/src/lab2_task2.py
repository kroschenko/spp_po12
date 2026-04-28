from enum import Enum


class CarStatus(Enum):
    OK = "Исправен"
    BROKEN = "Требует ремонта"
    IN_REPAIR = "В ремонте"


class TripStatus(Enum):
    PENDING = "Ожидает назначения"
    ASSIGNED = "Назначен"
    COMPLETED = "Выполнен"
    CANCELLED = "Отменен"


class Person:
    def __init__(self, name, person_id):
        self.name = name
        self.person_id = person_id

    def __str__(self):
        return f"{self.name} (ID: {self.person_id})"


class Driver(Person):
    def __init__(self, name, person_id, experience_years):
        super().__init__(name, person_id)
        self.experience_years = experience_years
        self.is_active = True
        self.assigned_car = None
        self.trip_history = []

    def request_repair(self):
        if self.assigned_car and self.assigned_car.status == CarStatus.BROKEN:
            print(f"Водитель {self.name} заявляет о поломке автомобиля {self.assigned_car.model}.")
            return True
        if self.assigned_car:
            print(f"Водитель {self.name}: автомобиль {self.assigned_car.model} исправен, ремонт не требуется.")
            return False
        print(f"Водитель {self.name}: за мной не закреплен автомобиль.")
        return False

    def complete_trip(self, trip, car_condition_ok=True):
        if trip.assigned_driver == self and trip.status == TripStatus.ASSIGNED:
            trip.status = TripStatus.COMPLETED
            self.trip_history.append(trip)
            print(f"Водитель {self.name} выполнил рейс {trip.trip_id}.")

            if not car_condition_ok and self.assigned_car:
                self.assigned_car.status = CarStatus.BROKEN
                print(f"Водитель {self.name} отметил, что автомобиль {self.assigned_car.model} неисправен.")
            return True
        print(f"Ошибка: Рейс {trip.trip_id} не может быть завершен водителем {self.name}.")
        return False

    def __str__(self):
        status = "активен" if self.is_active else "отстранен"
        car = self.assigned_car.model if self.assigned_car else "нет авто"
        return f"Водитель {self.name}, стаж: {self.experience_years}, {status}, авто: {car}"


class Car:
    def __init__(self, model, license_plate):
        self.model = model
        self.license_plate = license_plate
        self.status = CarStatus.OK

    def __str__(self):
        return f"Авто {self.model} ({self.license_plate}), статус: {self.status.value}"


class Trip:
    def __init__(self, trip_id, destination, distance_km):
        self.trip_id = trip_id
        self.destination = destination
        self.distance_km = distance_km
        self.status = TripStatus.PENDING
        self.assigned_driver = None
        self.assigned_car = None

    def __str__(self):
        driver_name = self.assigned_driver.name if self.assigned_driver else "не назначен"
        return f"Рейс {self.trip_id} до {self.destination}, статус: {self.status.value}, водитель: {driver_name}"


class Dispatcher(Person):
    def __init__(self, name, person_id):
        super().__init__(name, person_id)
        self._drivers = []
        self._cars = []
        self._trips = []

    def add_driver(self, driver):
        self._drivers.append(driver)
        print(f"Диспетчер {self.name}: Водитель {driver.name} добавлен в систему.")
        return True

    def add_car(self, car):
        self._cars.append(car)
        print(f"Диспетчер {self.name}: Автомобиль {car.model} добавлен в автопарк.")
        return True

    def add_trip_request(self, trip):
        self._trips.append(trip)
        print(f"Диспетчер {self.name}: Поступила заявка на рейс {trip.trip_id} до {trip.destination}.")
        return True

    def assign_trip(self, trip_id, driver_id, car_license):
        trip = next((t for t in self._trips if t.trip_id == trip_id), None)
        driver = next((d for d in self._drivers if d.person_id == driver_id and d.is_active), None)
        car = next(
            (c for c in self._cars if c.license_plate == car_license and c.status == CarStatus.OK),
            None,
        )

        if not trip or trip.status != TripStatus.PENDING:
            print(f"Ошибка: Рейс {trip_id} не найден или не ожидает назначения.")
            return False
        if not driver:
            print(f"Ошибка: Водитель с ID {driver_id} не найден, неактивен или отстранен.")
            return False
        if not car:
            print(f"Ошибка: Автомобиль {car_license} не найден или неисправен.")
            return False

        trip.status = TripStatus.ASSIGNED
        trip.assigned_driver = driver
        trip.assigned_car = car
        driver.assigned_car = car
        print(f"Диспетчер {self.name}: Рейс {trip_id} назначен водителю {driver.name} на автомобиле {car.model}.")
        return True

    def suspend_driver(self, driver_id):
        driver = next((d for d in self._drivers if d.person_id == driver_id), None)
        if driver:
            driver.is_active = False
            print(f"Диспетчер {self.name}: Водитель {driver.name} отстранен от работы.")
            return True
        print(f"Ошибка: Водитель с ID {driver_id} не найден.")
        return False

    def process_repair_request(self, driver_id):
        driver = next((d for d in self._drivers if d.person_id == driver_id), None)
        if driver and driver.assigned_car and driver.assigned_car.status == CarStatus.BROKEN:
            car = driver.assigned_car
            car.status = CarStatus.IN_REPAIR
            print(f"Диспетчер {self.name}: Принята заявка от {driver.name}. Автомобиль {car.model} отправлен в ремонт.")
            car.status = CarStatus.OK
            print(f"Диспетчер {self.name}: Автомобиль {car.model} отремонтирован и снова готов к работе.")
            return True
        print(f"Диспетчер {self.name}: Заявка на ремонт от {driver.name} не может быть обработана.")
        return False

    def show_system_state(self):
        print("\n" + "=" * 50)
        print(f"СОСТОЯНИЕ СИСТЕМЫ (Диспетчер {self.name})")
        print("-" * 50)
        print("Водители:")
        for d in self._drivers:
            print(f"  {d}")
        print("Автомобили:")
        for c in self._cars:
            print(f"  {c}")
        print("Рейсы:")
        for t in self._trips:
            print(f"  {t}")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    print("--- Демонстрация работы системы 'Автобаза' ---")

    disp = Dispatcher("Анна Петровна", "D001")

    d1 = Driver("Иван Сидоров", "DR001", 5)
    d2 = Driver("Петр Иванов", "DR002", 2)
    d3 = Driver("Сергей Смирнов", "DR003", 10)

    c1 = Car("ГАЗель Next", "А123ВВ")
    c2 = Car("Ford Transit", "В456АК")
    c3 = Car("Volvo FH", "Е789КМ")

    print("\n--- Инициализация системы ---")
    disp.add_driver(d1)
    disp.add_driver(d2)
    disp.add_driver(d3)
    disp.add_car(c1)
    disp.add_car(c2)
    disp.add_car(c3)

    print("\n--- Поступление заявок ---")
    t1 = Trip("T101", "Минск", 120)
    t2 = Trip("T102", "Брест", 350)
    t3 = Trip("T103", "Гродно", 280)
    disp.add_trip_request(t1)
    disp.add_trip_request(t2)
    disp.add_trip_request(t3)

    disp.show_system_state()

    print("\n--- Распределение рейсов ---")
    disp.assign_trip("T101", "DR001", "А123ВВ")
    disp.assign_trip("T102", "DR002", "В456АК")
    disp.assign_trip("T103", "DR003", "НЕТНОМЕР")

    disp.show_system_state()

    print("\n--- Выполнение рейсов и события ---")
    d1.complete_trip(t1, car_condition_ok=False)

    d1.request_repair()

    disp.process_repair_request("DR001")

    disp.suspend_driver("DR002")

    d2.complete_trip(t2)

    disp.show_system_state()
