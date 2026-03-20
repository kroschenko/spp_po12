"""
Шифрование текстового файла.
Поведенческий паттерн: Strategy (Стратегия).
"""

from abc import ABC, abstractmethod


class EncryptionStrategy(ABC):
    """Абстрактный класс стратегии шифрования."""

    @abstractmethod
    def encrypt(self, text: str) -> str:
        """Зашифровать текст."""

    @abstractmethod
    def decrypt(self, text: str) -> str:
        """Расшифровать текст."""

    @abstractmethod
    def get_name(self) -> str:
        """Получить название алгоритма."""


class VowelRemovalStrategy(EncryptionStrategy):
    """Стратегия: удаление всех гласных букв."""

    def __init__(self):
        self.vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouAEIOU"

    def encrypt(self, text: str) -> str:
        """Удалить гласные."""
        result = ""
        for char in text:
            if char not in self.vowels:
                result += char
        return result

    def decrypt(self, text: str) -> str:
        """Расшифровать невозможно (потеря данных)."""
        return f"[Невозможно восстановить] {text}"

    def get_name(self) -> str:
        return "Удаление гласных"


class CaesarCipherStrategy(EncryptionStrategy):
    """Стратегия: шифр Цезаря (сдвиг)."""

    def __init__(self, shift: int = 4):
        self.shift = shift % 26
        self.alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
        self.alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.russian_lower = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        self.russian_upper = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    def _shift_char(self, char: str, alphabet: str, shift: int) -> str:
        """Сдвинуть символ в алфавите."""
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index + shift) % len(alphabet)
            return alphabet[new_index]
        return char

    def encrypt(self, text: str) -> str:
        """Зашифровать сдвигом."""
        result = ""
        for char in text:
            if char in self.russian_lower:
                result += self._shift_char(char, self.russian_lower, self.shift)
            elif char in self.russian_upper:
                result += self._shift_char(char, self.russian_upper, self.shift)
            elif char in self.alphabet_lower:
                result += self._shift_char(char, self.alphabet_lower, self.shift)
            elif char in self.alphabet_upper:
                result += self._shift_char(char, self.alphabet_upper, self.shift)
            else:
                result += char
        return result

    def decrypt(self, text: str) -> str:
        """Расшифровать сдвигом."""
        result = ""
        for char in text:
            if char in self.russian_lower:
                result += self._shift_char(char, self.russian_lower, -self.shift)
            elif char in self.russian_upper:
                result += self._shift_char(char, self.russian_upper, -self.shift)
            elif char in self.alphabet_lower:
                result += self._shift_char(char, self.alphabet_lower, -self.shift)
            elif char in self.alphabet_upper:
                result += self._shift_char(char, self.alphabet_upper, -self.shift)
            else:
                result += char
        return result

    def get_name(self) -> str:
        return f"Цезарь (сдвиг {self.shift})"


class XorStrategy(EncryptionStrategy):
    """Стратегия: XOR с ключом."""

    def __init__(self, key: str = "secret"):
        self.key = key

    def encrypt(self, text: str) -> str:
        """Зашифровать XOR."""
        result = []
        key_length = len(self.key)
        for i, char in enumerate(text):
            key_char = self.key[i % key_length]
            xor_val = ord(char) ^ ord(key_char)
            result.append(chr(xor_val))
        return "".join(result)

    def decrypt(self, text: str) -> str:
        """Расшифровать XOR (то же самое)."""
        return self.encrypt(text)

    def get_name(self) -> str:
        return f"XOR (ключ: {self.key})"


class FileEncryptor:
    """Класс-шифровщик текстового файла."""

    def __init__(self, strategy: EncryptionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: EncryptionStrategy):
        """Сменить стратегию шифрования."""
        self.strategy = strategy

    def encrypt_file(self, input_path: str, output_path: str) -> bool:
        """Зашифровать файл."""
        try:
            with open(input_path, "r", encoding="utf-8") as file_in:
                text = file_in.read()

            encrypted = self.strategy.encrypt(text)

            with open(output_path, "w", encoding="utf-8") as file_out:
                file_out.write(encrypted)

            print(f"Файл зашифрован. Сохранен в: {output_path}")
            return True
        except FileNotFoundError:
            print(f"Ошибка: файл {input_path} не найден")
            return False
        except (IOError, OSError) as error:
            print(f"Ошибка ввода-вывода: {error}")
            return False

    def decrypt_file(self, input_path: str, output_path: str) -> bool:
        """Расшифровать файл."""
        try:
            with open(input_path, "r", encoding="utf-8") as file_in:
                text = file_in.read()

            decrypted = self.strategy.decrypt(text)

            with open(output_path, "w", encoding="utf-8") as file_out:
                file_out.write(decrypted)

            print(f"Файл расшифрован. Сохранен в: {output_path}")
            return True
        except FileNotFoundError:
            print(f"Ошибка: файл {input_path} не найден")
            return False
        except (IOError, OSError) as error:
            print(f"Ошибка ввода-вывода: {error}")
            return False

    def get_strategy_name(self) -> str:
        """Получить название текущей стратегии."""
        return self.strategy.get_name()


def create_sample_file():
    """Создать пример файла для демонстрации."""
    content = """Привет, мир! Это тестовый файл для шифрования.
Hello, world! This is a test file for encryption.
Цифры: 12345, спецсимволы: !@#$%^&*()"""
    with open("sample.txt", "w", encoding="utf-8") as file_out:
        file_out.write(content)
    print("Создан файл sample.txt")


def main():
    """Основная функция."""
    print("=" * 60)
    print("ШИФРОВАНИЕ ТЕКСТОВОГО ФАЙЛА")
    print("=" * 60)

    create_sample_file()

    print("\nДоступные алгоритмы шифрования:")
    print("1. Удаление гласных")
    print("2. Шифр Цезаря (сдвиг 4)")
    print("3. Шифр Цезаря (свой сдвиг)")
    print("4. XOR с ключом")
    print("5. XOR (свой ключ)")

    choice = input("\nВыберите алгоритм (1-5): ")

    if choice == "1":
        strategy = VowelRemovalStrategy()
    elif choice == "2":
        strategy = CaesarCipherStrategy(4)
    elif choice == "3":
        shift = int(input("Введите сдвиг (1-25): "))
        strategy = CaesarCipherStrategy(shift)
    elif choice == "4":
        strategy = XorStrategy("secret")
    elif choice == "5":
        key = input("Введите ключ: ")
        strategy = XorStrategy(key)
    else:
        print("Неверный выбор")
        return

    encryptor = FileEncryptor(strategy)
    print(f"\nВыбран алгоритм: {encryptor.get_strategy_name()}")

    print("\n1. Зашифровать sample.txt")
    print("2. Расшифровать")
    action = input("Выберите действие (1-2): ")

    if action == "1":
        encryptor.encrypt_file("sample.txt", "encrypted.txt")
        print("\nРезультат шифрования:")
        with open("encrypted.txt", "r", encoding="utf-8") as file_in:
            print(file_in.read()[:200])
    elif action == "2":
        encryptor.decrypt_file("encrypted.txt", "decrypted.txt")
        print("\nРезультат расшифровки:")
        with open("decrypted.txt", "r", encoding="utf-8") as file_in:
            print(file_in.read()[:200])
    else:
        print("Неверный выбор")


if __name__ == "__main__":
    main()
