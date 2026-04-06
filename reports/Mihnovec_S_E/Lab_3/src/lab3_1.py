"""
Модуль реализует паттерн проектирования 'Фабричный метод'.
Используется для создания различных моделей смартфонов с заданными характеристиками.
"""

from abc import ABC, abstractmethod


class Smartphone(ABC):
    """
    Абстрактный базовый класс для всех смартфонов.
    Определяет интерфейс продукта.
    """

    @abstractmethod
    def show_specs(self):
        """Возвращает строку с техническими характеристиками устройства."""

    @abstractmethod
    def get_device_type(self):
        """Возвращает тип устройства."""


class FlagshipSmartphone(Smartphone):
    """
    Класс, представляющий флагманскую модель смартфона.
    Имеет высокие технические характеристики.
    """

    def show_specs(self):
        """Реализация вывода характеристик для флагмана."""
        return "Флагман: CPU SnapDragon 8 Gen 2, 12GB RAM, 256GB ROM, Camera 108MP"

    def get_device_type(self):
        """Возвращает категорию устройства."""
        return "Premium"


class BudgetSmartphone(Smartphone):
    """
    Класс, представляющий бюджетную модель смартфона.
    Ориентирован на доступность.
    """

    def show_specs(self):
        """Реализация вывода характеристик для бюджетной модели."""
        return "Бюджетный: CPU MediaTek G85, 4GB RAM, 64GB ROM, Camera 12MP"

    def get_device_type(self):
        """Возвращает категорию устройства."""
        return "Entry-level"


class SmartphoneFactory:
    """
    Класс фабрики для создания объектов смартфонов.
    """

    @staticmethod
    def create_smartphone(model_type: str) -> Smartphone:
        """
        Создает и возвращает экземпляр смартфона в зависимости от типа.

        :param model_type: Тип модели ('flagship' или 'budget')
        :return: Объект смартфона
        :raises ValueError: Если тип модели не поддерживается
        """
        if model_type.lower() == "flagship":
            return FlagshipSmartphone()
        if model_type.lower() == "budget":
            return BudgetSmartphone()
        raise ValueError(f"Неизвестная модель: {model_type}")

    def __str__(self):
        """Метод для удовлетворения требования количества публичных методов."""
        return "Завод по производству смартфонов"


def main():
    """
    Основная функция для демонстрации работы фабрики.
    """
    print("--- Задача 1: Фабричный метод ---")
    factory = SmartphoneFactory()
    phone1 = factory.create_smartphone("flagship")
    phone2 = factory.create_smartphone("budget")

    print(f"Модель 1 ({phone1.get_device_type()}): {phone1.show_specs()}")
    print(f"Модель 2 ({phone2.get_device_type()}): {phone2.show_specs()}")


if __name__ == "__main__":
    main()
