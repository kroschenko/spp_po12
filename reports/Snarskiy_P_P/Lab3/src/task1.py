"""Abstract car factory"""

from abc import ABC, abstractmethod


class Sedan(ABC):
    """Abstract sedan class"""

    @abstractmethod
    def drive(self):
        """Drive the car"""

    @abstractmethod
    def honk(self):
        """Honk func"""


class MercedesSedan(Sedan):
    """Concrete sedan class"""

    def drive(self):
        print("Driving Mercedes Sedan")

    def honk(self):
        print("Honking Mercedes Sedan")


class AudiSedan(Sedan):
    """Concrete sedan class"""

    def drive(self):
        print("Driving Audi Sedan")

    def honk(self):
        print("Honking Mercedes Sedan")


class Coupe(ABC):
    """Abstract coupe class"""

    @abstractmethod
    def drive(self):
        """Drive func"""

    @abstractmethod
    def honk(self):
        """Honk func"""


class MercedesCoupe(Coupe):
    """Concrete coupe class"""

    def drive(self):
        print("Driving Mercedes Coupe")

    def honk(self):
        print("Honking Mercedes Sedan")


class AudiCoupe(Coupe):
    """Concrete coupe class"""

    def drive(self):
        print("Driving Audi Coupe")

    def honk(self):
        print("Honking Mercedes Sedan")


class Factory(ABC):
    """Abstract factory class"""

    @abstractmethod
    def create_sedan(self) -> Sedan:
        """Create sedan func"""

    @abstractmethod
    def create_coupe(self) -> Coupe:
        """Create coupe func"""


class MercedesFactory(Factory):
    """Concrete factory class"""

    def create_sedan(self) -> Sedan:
        return MercedesSedan()

    def create_coupe(self) -> Coupe:
        return MercedesCoupe()


class AudiFactory(Factory):
    """Concrete factory class"""

    def create_sedan(self) -> Sedan:
        return AudiSedan()

    def create_coupe(self) -> Coupe:
        return AudiCoupe()


def test_drive(factory: Factory):
    """Client func"""
    sedan = factory.create_sedan()
    coupe = factory.create_coupe()

    sedan.drive()
    coupe.drive()


if __name__ == "__main__":

    print("Client test driving Mercedes:")
    test_drive(MercedesFactory())

    print("\n")

    print("Client test driving Audi:")
    test_drive(AudiFactory())
