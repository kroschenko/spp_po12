from abc import ABC, abstractmethod

class Car(ABC):

    def __init__(self, model, engine, price):
        self.model = model
        self.engine = engine
        self.price = price

    @abstractmethod
    def get_description(self):
        pass

    def __str__(self):
        return f"{self.model} ({self.engine}) - {self.price} руб."


class Sedan(Car):

    def get_description(self):
        return f"Седан {self.model}: комфортный городской автомобиль с двигателем {self.engine}"

    def drive_city(self):
        return f"Едем по городу на {self.model}. Плавно и экономично."


class SUV(Car):
    def get_description(self):
        return f"Внедорожник {self.model}: мощный автомобиль с двигателем {self.engine} для бездорожья"

    def drive_offroad(self):
        return f"Едем по бездорожью на {self.model}. Полный привод включен!"


class Hatchback(Car):

    def get_description(self):
        return f"Хэтчбек {self.model}: компактный и маневренный автомобиль с двигателем {self.engine}"

    def park_easily(self):
        return f"Паркуемся на {self.model}. Компактные размеры - легко!"


class CarFactory(ABC):

    @abstractmethod
    def create_sedan(self) -> Sedan:
        pass

    @abstractmethod
    def create_suv(self) -> SUV:
        pass

    @abstractmethod
    def create_hatchback(self) -> Hatchback:
        pass

    @abstractmethod
    def get_factory_name(self) -> str:
        pass


class VolkswagenFactory(CarFactory):

    def get_factory_name(self) -> str:
        return "Завод Volkswagen (Германия)"

    def create_sedan(self) -> Sedan:
        return Sedan("Volkswagen Jetta", "1.4 TSI (бензин)", 1800000)

    def create_suv(self) -> SUV:
        return SUV("Volkswagen Tiguan", "2.0 TDI (дизель)", 2800000)

    def create_hatchback(self) -> Hatchback:
        return Hatchback("Volkswagen Golf", "1.6 MPI (бензин)", 1600000)


class ToyotaFactory(CarFactory):

    def get_factory_name(self) -> str:
        return "Завод Toyota (Япония)"

    def create_sedan(self) -> Sedan:
        return Sedan("Toyota Camry", "3.5 V6 (бензин)", 2500000)

    def create_suv(self) -> SUV:
        return SUV("Toyota Land Cruiser Prado", "2.8 TD (дизель)", 4500000)

    def create_hatchback(self) -> Hatchback:
        return Hatchback("Toyota Corolla", "1.8 Hybrid", 2000000)


class TeslaFactory(CarFactory):

    def get_factory_name(self) -> str:
        return "Завод Tesla (США)"

    def create_sedan(self) -> Sedan:
        return Sedan("Tesla Model S", "электрический (1020 л.с.)", 8500000)

    def create_suv(self) -> SUV:
        return SUV("Tesla Model X", "электрический (1020 л.с.)", 9500000)

    def create_hatchback(self) -> Hatchback:
        return Hatchback("Tesla Model 3", "электрический (450 л.с.)", 5000000)


def get_factory_choice():
    print("\nДоступные заводы:")
    print("1. Volkswagen (Германия)")
    print("2. Toyota (Япония)")
    print("3. Tesla (США)")

    while True:
        try:
            choice = int(input("\nВыберите завод (1-3): "))
            if choice == 1:
                return VolkswagenFactory()
            elif choice == 2:
                return ToyotaFactory()
            elif choice == 3:
                return TeslaFactory()
            else:
                print("Ошибка: введите число от 1 до 3")
        except ValueError:
            print("Ошибка: введите число")


def get_car_type_choice():
    print("\nДоступные типы автомобилей:")
    print("1. Седан")
    print("2. Внедорожник (SUV)")
    print("3. Хэтчбек")

    while True:
        try:
            choice = int(input("\nВыберите тип автомобиля (1-3): "))
            if choice == 1:
                return "sedan"
            elif choice == 2:
                return "suv"
            elif choice == 3:
                return "hatchback"
            else:
                print("Ошибка: введите число от 1 до 3")
        except ValueError:
            print("Ошибка: введите число")


def order_car(factory: CarFactory, car_type: str):

    print(f"\n{'=' * 50}")
    print(f"ОФОРМЛЕНИЕ ЗАКАЗА НА {factory.get_factory_name()}")
    print("=" * 50)

    if car_type == "sedan":
        car = factory.create_sedan()
        print(f"\n✅ Вы выбрали: {car}")
        print(car.get_description())
        print(car.drive_city())
    elif car_type == "suv":
        car = factory.create_suv()
        print(f"\n✅ Вы выбрали: {car}")
        print(car.get_description())
        print(car.drive_offroad())
    elif car_type == "hatchback":
        car = factory.create_hatchback()
        print(f"\n✅ Вы выбрали: {car}")
        print(car.get_description())
        print(car.park_easily())

    print(f"\n💰 Итоговая стоимость: {car.price} руб.")

    buy = input("\nХотите купить этот автомобиль? (да/нет): ").lower()
    if buy in ["да", "yes", "y", "д"]:
        print("\n🎉 ПОЗДРАВЛЯЕМ С ПОКУПКОЙ!")
        print(f"Вы стали владельцем {car.model}!")
    else:
        print("\nЗаказ отменен.")

    return car


def main():

    print("=" * 70)
    print("ПРОГРАММА: ЗАВОДЫ ПО ПРОИЗВОДСТВУ АВТОМОБИЛЕЙ")
    print("=" * 70)
    print("\nДобро пожаловать в систему заказа автомобилей!")

    while True:

        factory = get_factory_choice()

        car_type = get_car_type_choice()

        order_car(factory, car_type)

        again = input("\nХотите сделать еще один заказ? (да/нет): ").lower()
        if again not in ["да", "yes", "y", "д"]:
            break

    print("\n" + "=" * 70)
    print("СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ ПРОГРАММЫ!")
    print("=" * 70)


if __name__ == "__main__":
    main()
