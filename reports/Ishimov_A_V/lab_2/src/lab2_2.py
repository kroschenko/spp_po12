from abc import ABC, abstractmethod


# Обобщение
class Person(ABC):
    def __init__(self, name):
        self.name = name


# Интерфейс
class RepairRequester(ABC):
    @abstractmethod
    def request_repair(self, car):
        pass


# Класс водителя
class Driver(Person, RepairRequester):
    def __init__(self, name):
        super().__init__(name)
        self.suspended = False

    def request_repair(self, car):
        print(f"Водитель {self.name} подал заявку на ремонт автомобиля {car.number}")
        car.needs_repair = True

    def complete_route(self, route, car):
        if self.suspended:
            print(f"Водитель {self.name} отстранён и не может выполнить рейс")
            return

        print(f"Водитель {self.name} выполнил рейс {route.route_id}")
        route.completed = True
        print(f"Состояние автомобиля {car.number}: {'нужен ремонт' if car.needs_repair else 'исправен'}")


# Класс автомобиля
class Car:
    def __init__(self, number):
        self.number = number
        self.needs_repair = False

    def __str__(self):
        return f"Автомобиль {self.number}"


# Класс рейса
class Route:
    def __init__(self, route_id):
        self.route_id = route_id
        self.completed = False

    def __str__(self):
        return f"Рейс {self.route_id}"


# Класс диспетчера
class Dispatcher(Person):
    def __init__(self, name):
        super().__init__(name)
        self.drivers = []
        self.cars = []

    # Агрегация
    def add_driver(self, driver):
        self.drivers.append(driver)

    def add_car(self, car):
        self.cars.append(car)

    # Ассоциация
    def assign_route(self, driver, car, route):
        if driver.suspended:
            print(f"Диспетчер: водитель {driver.name} отстранён, рейс не назначен")
            return

        print(f"Диспетчер назначил водителю {driver.name} автомобиль {car.number} на рейс {route.route_id}")

    def suspend_driver(self, driver):
        driver.suspended = True
        print(f"Диспетчер отстранил водителя {driver.name} от работы")


dispatcher = Dispatcher("Иван Петров")
driver1 = Driver("Алексей")
driver2 = Driver("Сергей")

car1 = Car("A123BC")
car2 = Car("B777BB")

route1 = Route("R-01")

dispatcher.add_driver(driver1)
dispatcher.add_driver(driver2)
dispatcher.add_car(car1)
dispatcher.add_car(car2)

dispatcher.assign_route(driver1, car1, route1)

driver1.complete_route(route1, car1)

driver1.request_repair(car1)

dispatcher.suspend_driver(driver1)

driver1.complete_route(route1, car1)
