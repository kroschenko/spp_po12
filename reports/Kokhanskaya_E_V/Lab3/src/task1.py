"""Module implementing three design patterns for lab 3 variant 8.

This module contains:
1. Factory Method pattern - Vending machine for various products
2. Bridge pattern - TV remote control system
3. Command pattern - Text file operations library with undo support
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import os

# ============================================================================
# FIRST GROUP: CREATIONAL PATTERN - FACTORY METHOD
# Vending machine for snacks, chips, juices, etc.
# ============================================================================


class ProductCategory(Enum):
    """Product categories available in vending machine."""

    CHOCOLATE = "Chocolate bar"
    CHIPS = "Chips"
    JUICE = "Juice"
    SODA = "Soda"
    CANDY = "Candy"


@dataclass
class Product:
    """Product available in vending machine."""

    name: str
    price: float
    category: ProductCategory
    code: str
    calories: int


class ProductFactory(ABC):
    """Abstract factory for creating products."""

    @abstractmethod
    def create_product(self, code: str) -> Optional[Product]:
        """Create a product with given code."""
        # Abstract method - implementation in subclasses


class ChocolateFactory(ProductFactory):
    """Factory for creating chocolate products."""

    def create_product(self, code: str) -> Optional[Product]:
        """Create chocolate product based on code."""
        products = {
            "C01": Product("Milky Way", 1.50, ProductCategory.CHOCOLATE, "C01", 240),
            "C02": Product("Snickers", 1.50, ProductCategory.CHOCOLATE, "C02", 250),
            "C03": Product("Twix", 1.50, ProductCategory.CHOCOLATE, "C03", 245),
        }
        return products.get(code)


class ChipsFactory(ProductFactory):
    """Factory for creating chips products."""

    def create_product(self, code: str) -> Optional[Product]:
        """Create chips product based on code."""
        products = {
            "CH01": Product("Lays Classic", 2.00, ProductCategory.CHIPS, "CH01", 150),
            "CH02": Product("Pringles", 2.50, ProductCategory.CHIPS, "CH02", 160),
            "CH03": Product("Doritos", 2.00, ProductCategory.CHIPS, "CH03", 140),
        }
        return products.get(code)


class JuiceFactory(ProductFactory):
    """Factory for creating juice products."""

    def create_product(self, code: str) -> Optional[Product]:
        """Create juice product based on code."""
        products = {
            "J01": Product("Apple Juice", 1.80, ProductCategory.JUICE, "J01", 120),
            "J02": Product("Orange Juice", 1.80, ProductCategory.JUICE, "J02", 110),
            "J03": Product("Multivitamin", 2.00, ProductCategory.JUICE, "J03", 130),
        }
        return products.get(code)


class SodaFactory(ProductFactory):
    """Factory for creating soda products."""

    def create_product(self, code: str) -> Optional[Product]:
        """Create soda product based on code."""
        products = {
            "S01": Product("Coca-Cola", 1.50, ProductCategory.SODA, "S01", 140),
            "S02": Product("Pepsi", 1.50, ProductCategory.SODA, "S02", 140),
            "S03": Product("Fanta", 1.50, ProductCategory.SODA, "S03", 130),
        }
        return products.get(code)


class VendingMachine:
    """Vending machine that uses factory method pattern."""

    def __init__(self) -> None:
        """Initialize vending machine with all product factories."""
        self._factories = {
            ProductCategory.CHOCOLATE: ChocolateFactory(),
            ProductCategory.CHIPS: ChipsFactory(),
            ProductCategory.JUICE: JuiceFactory(),
            ProductCategory.SODA: SodaFactory(),
        }
        self._inventory = {}
        self._sales_total = 0.0
        self._initialize_inventory()

    def _initialize_inventory(self) -> None:
        """Initialize stock for all products."""
        product_codes = [
            "C01",
            "C02",
            "C03",
            "CH01",
            "CH02",
            "CH03",
            "J01",
            "J02",
            "J03",
            "S01",
            "S02",
            "S03",
        ]
        for code in product_codes:
            for factory in self._factories.values():
                product = factory.create_product(code)
                if product:
                    self._inventory[code] = {"product": product, "quantity": 10}
                    break

    def display_products(self) -> None:
        """Display all available products."""
        print("\n=== Available Products ===")
        for code, item in self._inventory.items():
            product = item["product"]
            quantity = item["quantity"]
            status = f" ({quantity} left)" if quantity > 0 else " (SOLD OUT)"
            print(f"{code}: {product.name} - ${product.price:.2f}{status}")

    def purchase(self, code: str, money: float) -> Optional[Product]:
        """Purchase a product with given code and money."""
        if code not in self._inventory:
            print(f"Invalid product code: {code}")
            return None

        item = self._inventory[code]
        if item["quantity"] <= 0:
            print(f"Product {code} is sold out")
            return None

        product = item["product"]
        if money < product.price:
            needed = product.price - money
            print(f"Insufficient funds. Need ${needed:.2f} more")
            return None

        item["quantity"] -= 1
        change = money - product.price
        self._sales_total += product.price

        print(f"Dispensing {product.name}")
        if change > 0:
            print(f"Change returned: ${change:.2f}")

        return product

    @property
    def sales_total(self) -> float:
        """Get total sales amount."""
        return self._sales_total


# ============================================================================
# SECOND GROUP: STRUCTURAL PATTERN - BRIDGE
# TV and remote control hierarchy
# ============================================================================


class TV(ABC):
    """Abstraction for TV device."""

    @abstractmethod
    def on(self) -> None:
        """Turn TV on."""

    @abstractmethod
    def off(self) -> None:
        """Turn TV off."""

    @abstractmethod
    def set_channel(self, channel: int) -> None:
        """Set TV channel."""

    @abstractmethod
    def set_volume(self, volume: int) -> None:
        """Set TV volume."""

    @abstractmethod
    def get_channel(self) -> int:
        """Get current channel."""

    @abstractmethod
    def get_volume(self) -> int:
        """Get current volume."""

    @abstractmethod
    def get_status(self) -> str:
        """Get TV status string."""


class SamsungTV(TV):
    """Samsung TV implementation."""

    def __init__(self) -> None:
        """Initialize Samsung TV."""
        self._is_on = False
        self._channel = 1
        self._volume = 10
        self._model = "Samsung QLED"

    def on(self) -> None:
        """Turn Samsung TV on."""
        self._is_on = True
        print(f"{self._model}: Power ON")

    def off(self) -> None:
        """Turn Samsung TV off."""
        self._is_on = False
        print(f"{self._model}: Power OFF")

    def set_channel(self, channel: int) -> None:
        """Set channel on Samsung TV."""
        if not self._is_on:
            print(f"{self._model}: TV is off, can't change channel")
            return
        if 1 <= channel <= 999:
            self._channel = channel
            print(f"{self._model}: Channel changed to {channel}")

    def set_volume(self, volume: int) -> None:
        """Set volume on Samsung TV."""
        if not self._is_on:
            print(f"{self._model}: TV is off, can't change volume")
            return
        if 0 <= volume <= 100:
            self._volume = volume
            print(f"{self._model}: Volume set to {volume}")

    def get_channel(self) -> int:
        """Get current channel."""
        return self._channel

    def get_volume(self) -> int:
        """Get current volume."""
        return self._volume

    def get_status(self) -> str:
        """Get Samsung TV status."""
        status = "ON" if self._is_on else "OFF"
        return f"{self._model}: {status}, Ch{self._channel}, Vol{self._volume}"


class LGTV(TV):
    """LG TV implementation."""

    def __init__(self) -> None:
        """Initialize LG TV."""
        self._is_on = False
        self._channel = 1
        self._volume = 15
        self._model = "LG OLED"

    def on(self) -> None:
        """Turn LG TV on."""
        self._is_on = True
        print(f"{self._model}: Power ON")

    def off(self) -> None:
        """Turn LG TV off."""
        self._is_on = False
        print(f"{self._model}: Power OFF")

    def set_channel(self, channel: int) -> None:
        """Set channel on LG TV."""
        if not self._is_on:
            print(f"{self._model}: TV is off, can't change channel")
            return
        if 1 <= channel <= 999:
            self._channel = channel
            print(f"{self._model}: Channel changed to {channel}")

    def set_volume(self, volume: int) -> None:
        """Set volume on LG TV."""
        if not self._is_on:
            print(f"{self._model}: TV is off, can't change volume")
            return
        if 0 <= volume <= 100:
            self._volume = volume
            print(f"{self._model}: Volume set to {volume}")

    def get_channel(self) -> int:
        """Get current channel."""
        return self._channel

    def get_volume(self) -> int:
        """Get current volume."""
        return self._volume

    def get_status(self) -> str:
        """Get LG TV status."""
        status = "ON" if self._is_on else "OFF"
        return f"{self._model}: {status}, Ch{self._channel}, Vol{self._volume}"


class RemoteControl(ABC):
    """Abstract remote control (bridge abstraction)."""

    def __init__(self, tv: TV) -> None:
        """Initialize remote with TV device."""
        self._tv = tv

    @abstractmethod
    def power(self) -> None:
        """Toggle power."""

    @abstractmethod
    def channel_up(self) -> None:
        """Go to next channel."""

    @abstractmethod
    def channel_down(self) -> None:
        """Go to previous channel."""

    @abstractmethod
    def volume_up(self) -> None:
        """Increase volume."""

    @abstractmethod
    def volume_down(self) -> None:
        """Decrease volume."""

    def get_status(self) -> str:
        """Get current TV status."""
        return self._tv.get_status()


class BasicRemote(RemoteControl):
    """Basic remote control with standard functions."""

    def power(self) -> None:
        """Toggle power."""
        print("Basic remote: Power button pressed")

    def channel_up(self) -> None:
        """Go to next channel."""
        new_channel = self._tv.get_channel() + 1
        self._tv.set_channel(new_channel)

    def channel_down(self) -> None:
        """Go to previous channel."""
        new_channel = self._tv.get_channel() - 1
        if new_channel >= 1:
            self._tv.set_channel(new_channel)

    def volume_up(self) -> None:
        """Increase volume."""
        new_volume = min(self._tv.get_volume() + 5, 100)
        self._tv.set_volume(new_volume)

    def volume_down(self) -> None:
        """Decrease volume."""
        new_volume = max(self._tv.get_volume() - 5, 0)
        self._tv.set_volume(new_volume)


class AdvancedRemote(RemoteControl):
    """Advanced remote with extra features."""

    def __init__(self, tv: TV) -> None:
        """Initialize advanced remote."""
        super().__init__(tv)
        self._muted = False
        self._last_volume = 15

    def power(self) -> None:
        """Toggle power."""
        print("Advanced remote: Power button pressed with animation")

    def channel_up(self) -> None:
        """Go to next channel."""
        new_channel = self._tv.get_channel() + 1
        self._tv.set_channel(new_channel)
        print(f"Channel: {new_channel}")

    def channel_down(self) -> None:
        """Go to previous channel."""
        new_channel = self._tv.get_channel() - 1
        if new_channel >= 1:
            self._tv.set_channel(new_channel)
            print(f"Channel: {new_channel}")

    def volume_up(self) -> None:
        """Increase volume with mute handling."""
        if self._muted:
            self._muted = False
            self._tv.set_volume(self._last_volume)
        else:
            new_volume = min(self._tv.get_volume() + 2, 100)
            self._tv.set_volume(new_volume)

    def volume_down(self) -> None:
        """Decrease volume with mute handling."""
        if self._muted:
            self._muted = False
            self._tv.set_volume(self._last_volume)
        else:
            new_volume = max(self._tv.get_volume() - 2, 0)
            self._tv.set_volume(new_volume)

    def mute(self) -> None:
        """Mute/unmute TV."""
        if self._muted:
            self._tv.set_volume(self._last_volume)
            self._muted = False
            print("Unmuted")
        else:
            self._last_volume = self._tv.get_volume()
            self._tv.set_volume(0)
            self._muted = True
            print("Muted")


# ============================================================================
# THIRD GROUP: BEHAVIORAL PATTERN - COMMAND
# Text file operations library with undo support
# ============================================================================


class TextFile:
    """Represents a text file with content."""

    def __init__(self, path: str) -> None:
        """Initialize text file."""
        self.path = path
        self.content = ""
        self._load_content()

    def _load_content(self) -> None:
        """Load content from file if exists."""
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as file:
                    self.content = file.read()
            except (IOError, OSError):
                self.content = ""

    def save(self) -> None:
        """Save content to file."""
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(self.content)

    def read(self) -> str:
        """Read file content."""
        return self.content

    def write(self, content: str) -> None:
        """Write new content."""
        self.content = content

    def append(self, text: str) -> None:
        """Append text to content."""
        self.content += text

    def replace(self, old: str, new: str) -> None:
        """Replace text in content."""
        self.content = self.content.replace(old, new)

    @property
    def size(self) -> int:
        """Get file size in bytes."""
        return len(self.content.encode("utf-8"))

    @property
    def modified_at(self) -> datetime:
        """Get last modification time."""
        if os.path.exists(self.path):
            timestamp = os.path.getmtime(self.path)
            return datetime.fromtimestamp(timestamp)
        return datetime.now()


class Command(ABC):
    """Abstract command for undoable operations."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""

    @abstractmethod
    def undo(self) -> None:
        """Undo the command."""


class WriteCommand(Command):
    """Command to write entire content to file."""

    def __init__(self, file: TextFile, new_content: str) -> None:
        """Initialize write command."""
        self._file = file
        self._new_content = new_content
        self._old_content = ""

    def execute(self) -> None:
        """Execute write operation."""
        self._old_content = self._file.read()
        self._file.write(self._new_content)
        self._file.save()

    def undo(self) -> None:
        """Undo write operation."""
        self._file.write(self._old_content)
        self._file.save()


class AppendCommand(Command):
    """Command to append text to file."""

    def __init__(self, file: TextFile, text: str) -> None:
        """Initialize append command."""
        self._file = file
        self._text = text

    def execute(self) -> None:
        """Execute append operation."""
        self._file.append(self._text)
        self._file.save()

    def undo(self) -> None:
        """Undo append operation."""
        content = self._file.read()
        if content.endswith(self._text):
            self._file.write(content[: -len(self._text)])
            self._file.save()


class ReplaceCommand(Command):
    """Command to replace text in file."""

    def __init__(self, file: TextFile, old: str, new: str) -> None:
        """Initialize replace command."""
        self._file = file
        self._old = old
        self._new = new
        self._occurrences = 0

    def execute(self) -> None:
        """Execute replace operation."""
        content = self._file.read()
        self._occurrences = content.count(self._old)
        self._file.replace(self._old, self._new)
        self._file.save()

    def undo(self) -> None:
        """Undo replace operation."""
        content = self._file.read()
        self._file.write(content.replace(self._new, self._old))
        self._file.save()


class CompositeCommand(Command):
    """Command that groups multiple commands."""

    def __init__(self) -> None:
        """Initialize composite command."""
        self._commands: List[Command] = []

    def add(self, command: Command) -> None:
        """Add command to composite."""
        self._commands.append(command)

    def execute(self) -> None:
        """Execute all commands in sequence."""
        for command in self._commands:
            command.execute()

    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for command in reversed(self._commands):
            command.undo()


class TextFileProcessor:
    """Text file processor with command pattern and undo support."""

    def __init__(self) -> None:
        """Initialize processor."""
        self._history: List[Command] = []
        self._redo_stack: List[Command] = []

    def execute_command(self, command: Command) -> None:
        """Execute command and add to history."""
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self) -> bool:
        """Undo last command."""
        if not self._history:
            return False
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        return True

    def redo(self) -> bool:
        """Redo last undone command."""
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        return True

    def get_history_size(self) -> int:
        """Get number of commands in history."""
        return len(self._history)


# ============================================================================
# DEMONSTRATION
# ============================================================================


def demonstrate_vending_machine() -> None:
    """Demonstrate vending machine functionality."""
    print("\n" + "=" * 60)
    print("DEMONSTRATION 1: VENDING MACHINE (Factory Method Pattern)")
    print("=" * 60)

    vending = VendingMachine()
    vending.display_products()

    print("\n--- Purchasing products ---")
    vending.purchase("C01", 2.00)
    vending.purchase("CH02", 3.00)
    vending.purchase("J01", 2.00)
    vending.purchase("INVALID", 1.00)

    print(f"\nTotal sales: ${vending.sales_total:.2f}")


def demonstrate_tv_remote() -> None:
    """Demonstrate TV and remote control functionality."""
    print("\n" + "=" * 60)
    print("DEMONSTRATION 2: TV REMOTE CONTROL (Bridge Pattern)")
    print("=" * 60)

    samsung = SamsungTV()
    lg = LGTV()

    basic_remote = BasicRemote(samsung)
    advanced_remote = AdvancedRemote(lg)

    print("\n--- Controlling Samsung TV with Basic Remote ---")
    basic_remote.power()
    basic_remote.volume_up()
    basic_remote.channel_up()
    print(samsung.get_status())

    print("\n--- Controlling LG TV with Advanced Remote ---")
    advanced_remote.power()
    advanced_remote.volume_up()
    advanced_remote.channel_up()
    advanced_remote.mute()
    print(lg.get_status())


def demonstrate_text_processor() -> None:
    """Demonstrate text file processor functionality."""
    print("\n" + "=" * 60)
    print("DEMONSTRATION 3: TEXT FILE PROCESSOR (Command Pattern)")
    print("=" * 60)

    test_file_path = "test_demo.txt"
    with open(test_file_path, "w", encoding="utf-8") as file:
        file.write("Hello World\nThis is a test file.\n")

    file = TextFile(test_file_path)
    processor = TextFileProcessor()

    print(f"\nOriginal content:\n{file.read()}")

    print("\n--- Executing commands ---")
    write_cmd = WriteCommand(file, "New content here!")
    processor.execute_command(write_cmd)
    print(f"After write: {file.read()}")

    append_cmd = AppendCommand(file, "\nAppended text.")
    processor.execute_command(append_cmd)
    print(f"After append: {file.read()}")

    print("\n--- Undo operations ---")
    processor.undo()
    print(f"After undo: {file.read()}")
    processor.undo()
    print(f"After second undo: {file.read()}")

    print("\n--- Redo operations ---")
    processor.redo()
    print(f"After redo: {file.read()}")

    if os.path.exists(test_file_path):
        os.remove(test_file_path)


def main() -> None:
    """Main demonstration function."""
    print("\n" + "=" * 60)
    print("LABORATORY WORK #3 - DESIGN PATTERNS (VARIANT 8)")
    print("=" * 60)

    demonstrate_vending_machine()
    demonstrate_tv_remote()
    demonstrate_text_processor()

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
