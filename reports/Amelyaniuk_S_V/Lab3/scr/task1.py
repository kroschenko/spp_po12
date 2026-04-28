from abc import ABC, abstractmethod

# --- Абстрактный продукт ---
class Smartphone(ABC):
    def __init__(self, model_name: str, cpu: str, ram: int, screen: str, price: int):
        self.model_name = model_name
        self.cpu = cpu
        self.ram = ram
        self.screen = screen
        self.price = price

    @abstractmethod
    def get_info(self):
        pass

# --- Конкретные продукты (Модели смартфонов с характеристиками) ---

class BudgetModel(Smartphone):
    def __init__(self):
        super().__init__(
            model_name="Lite-2025",
            cpu="MediaTek Helio G99",
            ram=4,
            screen="6.5' IPS",
            price=15000
        )

    def get_info(self):
        return f"Бюджетная модель: {self.model_name} | Процессор: {self.cpu} | ОЗУ: {self.ram}ГБ | Экран: {self.screen} | Цена: {self.price} руб."

class FlagshipModel(Smartphone):
    def __init__(self):
        super().__init__(
            model_name="Ultra-Pro Max",
            cpu="Snapdragon 8 Gen 3",
            ram=16,
            screen="6.8' AMOLED 120Hz",
            price=120000
        )

    def get_info(self):
        return f"Флагманская модель: {self.model_name} | Процессор: {self.cpu} | ОЗУ: {self.ram}ГБ | Экран: {self.screen} | Цена: {self.price} руб."

class WorkstationModel(Smartphone):
    def __init__(self):
        super().__init__(
            model_name="Business Tab-Phone",
            cpu="Apple A18 Pro",
            ram=8,
            screen="7.0' Foldable OLED",
            price=150000
        )

    def get_info(self):
        return f"Бизнес-модель: {self.model_name} | Процессор: {self.cpu} | ОЗУ: {self.ram}ГБ | Экран: {self.screen} | Цена: {self.price} руб."


# --- Фабрика (Завод) ---
class SmartphoneFactory:
    @staticmethod
    def produce_smartphone(type_name: str) -> Smartphone:
        """Метод для создания моделей по заранее выбранным типам"""
        types = {
            "budget": BudgetModel,
            "flagship": FlagshipModel,
            "business": WorkstationModel
        }
        
        smartphone_class = types.get(type_name.lower())
        if smartphone_class:
            return smartphone_class()
        else:
            raise ValueError(f"Модель типа '{type_name}' не выпускается на нашем заводе.")


# --- Клиентский код ---
if __name__ == "__main__":
    factory = SmartphoneFactory()

    print("=== Запуск производственной линии смартфона ===")
    
    # Создаем разные модели по их типам (характеристики уже внутри)
    phone1 = factory.produce_smartphone("budget")
    phone2 = factory.produce_smartphone("flagship")
    phone3 = factory.produce_smartphone("business")

    print(phone1.get_info())
    print(phone2.get_info())
    print(phone3.get_info())

    # Попытка создать неизвестную модель
    try:
        phone4 = factory.produce_smartphone("gaming")
    except ValueError as e:
        print(f"\n[Ошибка производства] {e}")