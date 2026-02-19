class Transport:
    def __init__(self, number, typ):
        self.number = number
        self.typ = typ
        self.works = True
        self.route = None

    def __str__(self):
        return f"{self.typ} {self.number}"


class Route:
    def __init__(self, num, name, interval):
        self.num = num
        self.name = name
        self.interval = interval
        self.vehicles = []
        self.reserve = []

    def add_vehicle(self, vehicle):
        vehicle.route = self
        self.vehicles.append(vehicle)
        print(f"{vehicle} назначен на маршрут {self.num}")

    def add_reserve(self, vehicle):
        self.reserve.append(vehicle)
        print(f"{vehicle} в резерве маршрута {self.num}")

    def breakdown(self, vehicle):
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
            print(f"{vehicle} сломался!")

            if self.reserve:
                new = self.reserve.pop(0)
                self.add_vehicle(new)
                print(f"Резервный {new} вышел на линию")
            else:
                self.interval = self.interval * 2
                print(f"Резерва нет! Интервал увеличен до {self.interval} мин")

    def info(self):
        print(f"\nМаршрут {self.num}: {self.name}")
        print(f"Интервал: {self.interval} мин")
        print(f"На линии: {[str(v) for v in self.vehicles]}")
        print(f"В резерве: {[str(v) for v in self.reserve]}")


if __name__ == "__main__":
    route_5 = Route(5, "Центр - Северный", 10)

    bus1 = Transport("А001АА", "автобус")
    bus2 = Transport("А002АА", "автобус")
    trolley = Transport("Т001ТТ", "троллейбус")
    reserve = Transport("А003АА", "автобус")

    route_5.add_vehicle(bus1)
    route_5.add_vehicle(bus2)
    route_5.add_vehicle(trolley)
    route_5.add_reserve(reserve)

    route_5.info()

    print("\nАвария")
    route_5.breakdown(bus1)

    route_5.info()
