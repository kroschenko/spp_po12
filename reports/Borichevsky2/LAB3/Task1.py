from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional


class CarType(Enum):
    """Типы автомобилей."""
    SEDAN = auto()
    SUV = auto()
    TRUCK = auto()
    ELECTRIC = auto()


class Car(ABC):
    """Абстрактный базовый класс для всех автомобилей."""

    def __init__(self, model: str, color: str, engine_power: int):
        self.model = model
        self.color = color
        self.engine_power = engine_power
        self._is_engine_running = False

    @abstractmethod
    def get_car_type(self) -> CarType:
        """Возвращает тип автомобиля."""
        pass

    @abstractmethod
    def get_features(self) -> list[str]:
        """Возвращает список особенностей автомобиля."""
        pass

    def start_engine(self) -> str:
        """Запускает двигатель."""
        self._is_engine_running = True
        return f"Двигатель {self.model} запущен"

    def stop_engine(self) -> str:
        """Останавливает двигатель."""
        self._is_engine_running = False
        return f"Двигатель {self.model} остановлен"

    def __str__(self) -> str:
        return (f"{self.get_car_type().name}: {self.model}, "
                f"цвет: {self.color}, мощность: {self.engine_power} л.с.")


class Sedan(Car):
    """Класс седана."""

    def get_car_type(self) -> CarType:
        return CarType.SEDAN

    def get_features(self) -> list[str]:
        return ["Комфорт", "Экономичность", "Просторный салон"]


class SUV(Car):
    """Класс внедорожника."""

    def get_car_type(self) -> CarType:
        return CarType.SUV

    def get_features(self) -> list[str]:
        return ["Полный привод", "Высокий клиренс", "Вместительность"]


class Truck(Car):
    """Класс грузовика."""

    def get_car_type(self) -> CarType:
        return CarType.TRUCK

    def get_features(self) -> list[str]:
        return ["Большая грузоподъемность", "Мощный двигатель", "Прочная рама"]


class ElectricCar(Car):
    """Класс электромобиля."""

    def __init__(self, model: str, color: str, engine_power: int,
                 battery_capacity: float):
        super().__init__(model, color, engine_power)
        self.battery_capacity = battery_capacity

    def get_car_type(self) -> CarType:
        return CarType.ELECTRIC

    def get_features(self) -> list[str]:
        return ["Экологичность", "Низкая стоимость эксплуатации",
                f"Батарея: {self.battery_capacity} кВт·ч"]

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base}, батарея: {self.battery_capacity} кВт·ч"


class CarFactory(ABC):
    """
    Абстрактный класс фабрики (Factory Method).
    Определяет интерфейс для создания автомобилей.
    """

    @abstractmethod
    def create_car(self, model: str, color: str,
                   engine_power: int) -> Car:
        """
        Фабричный метод для создания автомобиля.

        Args:
            model: Модель автомобиля
            color: Цвет автомобиля
            engine_power: Мощность двигателя в л.с.

        Returns:
            Созданный экземпляр автомобиля
        """
        pass

    def produce_car(self, model: str, color: str,
                    engine_power: int) -> Car:
        """
        Шаблонный метод производства автомобиля.

        Выполняет стандартные операции при производстве:
        1. Создание автомобиля
        2. Проверка качества
        3. Подготовка к выдаче

        Args:
            model: Модель автомобиля
            color: Цвет автомобиля
            engine_power: Мощность двигателя

        Returns:
            Готовый к эксплуатации автомобиль
        """
        car = self.create_car(model, color, engine_power)
        self._quality_check(car)
        self._prepare_for_delivery(car)
        return car

    def _quality_check(self, car: Car) -> None:
        """Проверка качества автомобиля."""
        print(f"Проверка качества {car.model}... OK")

    def _prepare_for_delivery(self, car: Car) -> None:
        """Подготовка автомобиля к выдаче."""
        print(f"Подготовка {car.model} к выдаче... Готово")


class SedanFactory(CarFactory):
    """Фабрика производства седанов."""

    def create_car(self, model: str, color: str,
                   engine_power: int) -> Car:
        return Sedan(model, color, engine_power)


class SUVFactory(CarFactory):
    """Фабрика производства внедорожников."""

    def create_car(self, model: str, color: str,
                   engine_power: int) -> Car:
        return SUV(model, color, engine_power)


class TruckFactory(CarFactory):
    """Фабрика производства грузовиков."""

    def create_car(self, model: str, color: str,
                   engine_power: int) -> Car:
        return Truck(model, color, engine_power)


class ElectricCarFactory(CarFactory):
    """
    Фабрика производства электромобилей.
    Расширяет базовый интерфейс для работы с батареями.
    """

    def __init__(self, default_battery_capacity: float = 75.0):
        self._default_battery_capacity = default_battery_capacity

    def create_car(self, model: str, color: str,
                   engine_power: int) -> Car:
        return ElectricCar(
            model, color, engine_power,
            self._default_battery_capacity
        )

    def create_car_with_battery(self, model: str, color: str,
                                engine_power: int,
                                battery_capacity: float) -> ElectricCar:
        """Создание электромобиля с указанной емкостью батареи."""
        return ElectricCar(model, color, engine_power, battery_capacity)


class UniversalCarFactory:
    """
    Универсальная фабрика, способная производить разные типы автомобилей.
    Демонстрирует расширяемость паттерна Factory Method.
    """

    _factories: dict[CarType, type[CarFactory]] = {
        CarType.SEDAN: SedanFactory,
        CarType.SUV: SUVFactory,
        CarType.TRUCK: TruckFactory,
        CarType.ELECTRIC: ElectricCarFactory,
    }

    @classmethod
    def register_factory(cls, car_type: CarType,
                         factory_class: type[CarFactory]) -> None:
        """Регистрация новой фабрики."""
        cls._factories[car_type] = factory_class

    @classmethod
    def create_car(cls, car_type: CarType, model: str, color: str,
                   engine_power: int, **kwargs) -> Car:
        """
        Создание автомобиля указанного типа.

        Args:
            car_type: Тип автомобиля
            model: Модель автомобиля
            color: Цвет автомобиля
            engine_power: Мощность двигателя
            **kwargs: Дополнительные параметры (например, battery_capacity)

        Returns:
            Созданный автомобиль

        Raises:
            ValueError: Если тип автомобиля не поддерживается
        """
        if car_type not in cls._factories:
            raise ValueError(f"Неизвестный тип автомобиля: {car_type}")

        factory_class = cls._factories[car_type]
        factory = factory_class()

        # Особая обработка для электромобилей
        if car_type == CarType.ELECTRIC and "battery_capacity" in kwargs:
            if isinstance(factory, ElectricCarFactory):
                return factory.create_car_with_battery(
                    model, color, engine_power,
                    kwargs["battery_capacity"]
                )

        return factory.produce_car(model, color, engine_power)


# ============== Демонстрация работы ==============

def main():
    """Демонстрация работы фабричного метода."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА FACTORY METHOD")
    print("=" * 60)

    # 1. Использование конкретных фабрик
    print("\n1. Производство на специализированных фабриках:")
    print("-" * 50)

    sedan_factory = SedanFactory()
    sedan = sedan_factory.produce_car("Toyota Camry", "Серебристый", 200)
    print(f"Произведен: {sedan}")
    print(f"Особенности: {', '.join(sedan.get_features())}")

    print()

    suv_factory = SUVFactory()
    suv = suv_factory.produce_car("BMW X5", "Черный", 300)
    print(f"Произведен: {suv}")
    print(f"Особенности: {', '.join(suv.get_features())}")

    # 2. Использование универсальной фабрики
    print("\n2. Производство на универсальной фабрике:")
    print("-" * 50)

    truck = UniversalCarFactory.create_car(
        CarType.TRUCK, "Volvo FH", "Синий", 500
    )
    print(f"Произведен: {truck}")
    print(f"Особенности: {', '.join(truck.get_features())}")

    electric = UniversalCarFactory.create_car(
        CarType.ELECTRIC, "Tesla Model S", "Красный", 670,
        battery_capacity=100.0
    )
    print(f"Произведен: {electric}")
    print(f"Особенности: {', '.join(electric.get_features())}")

    # 3. Демонстрация работы с автомобилями
    print("\n3. Использование автомобилей:")
    print("-" * 50)

    cars = [sedan, suv, truck, electric]
    for car in cars:
        print(f"\n{car}")
        print(f"  {car.start_engine()}")
        print(f"  {car.stop_engine()}")

    print("\n" + "=" * 60)
    print("Готово!")
    print("=" * 60)


if __name__ == "__main__":
    main()