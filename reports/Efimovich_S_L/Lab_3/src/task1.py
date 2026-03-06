from abc import ABC, abstractmethod


class Smartphone:

    def __init__(self, *, model, processor, display, camera, body):
        self.model = model
        self.processor = processor
        self.display = display
        self.camera = camera
        self.body = body

    def show_info(self):
        print(f"\n--- {self.model} ---")
        print(f"Процессор: {self.processor}")
        print(f"Дисплей: {self.display}")
        print(f"Камера: {self.camera}")
        print(f"Корпус: {self.body}")


class PhoneFactory(ABC):

    @abstractmethod
    def create_processor(self):
        pass

    @abstractmethod
    def create_display(self):
        pass

    @abstractmethod
    def create_camera(self):
        pass

    @abstractmethod
    def create_body(self):
        pass

    @abstractmethod
    def get_model_name(self):
        pass


# ========== Конкретные фабрики ==========


class BudgetFactory(PhoneFactory):

    def create_processor(self):
        return "MediaTek Helio G25, 2.0 ГГц"

    def create_display(self):
        return "6.1 дюймов, IPS, 1560x720"

    def create_camera(self):
        return "13 МП, вспышка, автофокус"

    def create_body(self):
        return "Пластик, черный, 185 г"

    def get_model_name(self):
        return "Galaxy A04"


class MidRangeFactory(PhoneFactory):

    def create_processor(self):
        return "Snapdragon 778G, 2.4 ГГц"

    def create_display(self):
        return "6.5 дюймов, AMOLED, 2400x1080"

    def create_camera(self):
        return "64 МП, стабилизация, 4K видео"

    def create_body(self):
        return "Стекло, синий, 175 г"

    def get_model_name(self):
        return "Galaxy A54"


class FlagshipFactory(PhoneFactory):

    def create_processor(self):
        return "Snapdragon 8 Gen 2, 3.2 ГГц"

    def create_display(self):
        return "6.8 дюймов, Dynamic AMOLED, 3200x1440, 120Гц"

    def create_camera(self):
        return "200 МП, лазерный фокус, 8K видео"

    def create_body(self):
        return "Титан, серебристый, 195 г"

    def get_model_name(self):
        return "Galaxy S23 Ultra"


class PhoneFactoryPlant:

    @staticmethod
    def create_phone(factory):
        return Smartphone(
            model=factory.get_model_name(),
            processor=factory.create_processor(),
            display=factory.create_display(),
            camera=factory.create_camera(),
            body=factory.create_body(),
        )


if __name__ == "__main__":
    print("ЗАВОД ПО ПРОИЗВОДСТВУ СМАРТФОНОВ")
    print("=" * 40)

    budget_phone = PhoneFactoryPlant.create_phone(BudgetFactory())
    mid_phone = PhoneFactoryPlant.create_phone(MidRangeFactory())
    flagship_phone = PhoneFactoryPlant.create_phone(FlagshipFactory())

    budget_phone.show_info()
    mid_phone.show_info()
    flagship_phone.show_info()

    print("\n" + "=" * 40)
    print("Производство завершено!")
