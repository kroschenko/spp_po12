"""Модуль с реализацией паттерна Фабрика для создания смартфонов."""
from abc import ABC, abstractmethod


class Smartphone(ABC):  # pylint: disable=R0903,R0913,R0917
    """Абстрактный класс для представления смартфона."""

    def __init__(self, model_name: str, cpu: str, ram: int, screen: str, price: int):  # pylint: disable=R0913,R0917
        """Инициализирует смартфон с заданными характеристиками.

        Args:
            model_name: Название модели.
            cpu: Процессор.
            ram: Объём оперативной памяти (ГБ).
            screen: Характеристики экрана.
            price: Цена в рублях.
        """
        self.model_name = model_name
        self.cpu = cpu
        self.ram = ram
        self.screen = screen
        self.price = price

    @abstractmethod
    def get_info(self):
        """Возвращает информацию о смартфоне."""


class BudgetModel(Smartphone):  # pylint: disable=R0903
    """Бюджетная модель смартфона."""

    def __init__(self):
        """Инициализирует бюджетную модель смартфона."""
        super().__init__(
            model_name="Lite-2025",
            cpu="MediaTek Helio G99",
            ram=4,
            screen="6.5' IPS",
            price=15000,
        )

    def get_info(self):
        """Возвращает информацию о бюджетной модели."""
        return (
            f"Бюджетная модель: {self.model_name} | "
            f"Процессор: {self.cpu} | ОЗУ: {self.ram}ГБ | "
            f"Экран: {self.screen} | Цена: {self.price} руб."
        )


class FlagshipModel(Smartphone):  # pylint: disable=R0903
    """Флагманская модель смартфона."""

    def __init__(self):
        """Инициализирует флагманскую модель смартфона."""
        super().__init__(
            model_name="Ultra-Pro Max",
            cpu="Snapdragon 8 Gen 3",
            ram=16,
            screen="6.8' AMOLED 120Hz",
            price=120000,
        )

    def get_info(self):
        """Возвращает информацию о флагманской модели."""
        return (
            f"Флагманская модель: {self.model_name} | "
            f"Процессор: {self.cpu} | ОЗУ: {self.ram}ГБ | "
            f"Экран: {self.screen} | Цена: {self.price} руб."
        )


class WorkstationModel(Smartphone):  # pylint: disable=R0903
    """Бизнес-модель смартфона."""

    def __init__(self):
        """Инициализирует бизнес-модель смартфона."""
        super().__init__(
            model_name="Business Tab-Phone",
            cpu="Apple A18 Pro",
            ram=8,
            screen="7.0' Foldable OLED",
            price=150000,
        )

    def get_info(self):
        """Возвращает информацию о бизнес-модели."""
        return (
            f"Бизнес-модель: {self.model_name} | "
            f"Процессор: {self.cpu} | ОЗУ: {self.ram}ГБ | "
            f"Экран: {self.screen} | Цена: {self.price} руб."
        )


class SmartphoneFactory:  # pylint: disable=R0903
    """Фабрика для создания смартфонов различных типов."""

    @staticmethod
    def produce_smartphone(type_name: str) -> Smartphone:
        """Создает смартфон заданного типа."""
        types = {
            "budget": BudgetModel,
            "flagship": FlagshipModel,
            "business": WorkstationModel,
        }

        smartphone_class = types.get(type_name.lower())
        if smartphone_class:
            return smartphone_class()
        raise ValueError(
            f"Модель типа '{type_name}' не выпускается на нашем заводе."
        )


if __name__ == "__main__":
    factory = SmartphoneFactory()

    print("=== Запуск производственной линии смартфона ===")

    phone1 = factory.produce_smartphone("budget")
    phone2 = factory.produce_smartphone("flagship")
    phone3 = factory.produce_smartphone("business")

    print(phone1.get_info())
    print(phone2.get_info())
    print(phone3.get_info())

    try:
        factory.produce_smartphone("gaming")
    except ValueError as e:
        print(f"Ошибка: {e}")
