from abc import ABC, abstractmethod


class EncryptionStrategy(ABC):
    """Абстрактная стратегия шифрования."""

    @abstractmethod
    def encrypt(self, text: str) -> str:
        """Зашифровать текст."""
        raise NotImplementedError


class RemoveVowelsStrategy(EncryptionStrategy):
    """Стратегия удаления всех гласных букв из текста."""

    def encrypt(self, text: str) -> str:
        vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouAEIOU"
        return "".join(char for char in text if char not in vowels)


class ShiftCipherStrategy(EncryptionStrategy):

    def __init__(self, shift: int) -> None:
        self.shift = shift
        self.ru_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self.ru_upper = self.ru_lower.upper()
        self.en_lower = "abcdefghijklmnopqrstuvwxyz"
        self.en_upper = self.en_lower.upper()

    def _shift_char(self, char: str, alphabet: str) -> str:
        index = alphabet.index(char)
        new_index = (index + self.shift) % len(alphabet)
        return alphabet[new_index]

    def encrypt(self, text: str) -> str:
        result = []

        for char in text:
            if char in self.ru_lower:
                result.append(self._shift_char(char, self.ru_lower))
            elif char in self.ru_upper:
                result.append(self._shift_char(char, self.ru_upper))
            elif char in self.en_lower:
                result.append(self._shift_char(char, self.en_lower))
            elif char in self.en_upper:
                result.append(self._shift_char(char, self.en_upper))
            else:
                result.append(char)

        return "".join(result)


class XorCipherStrategy(EncryptionStrategy):

    def __init__(self, key: int) -> None:
        self.key = key

    def encrypt(self, text: str) -> str:
        encrypted_chars = [chr(ord(char) ^ self.key) for char in text]
        return "".join(encrypted_chars)


class TextFileEncryptor:
    """Класс-шифровщик текстовых файлов."""

    def __init__(self, strategy: EncryptionStrategy) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: EncryptionStrategy) -> None:
        """Сменить алгоритм шифрования."""
        self.strategy = strategy

    def encrypt_file(self, input_file: str, output_file: str) -> None:
        """Считать текст из файла, зашифровать и записать в другой файл."""
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()

        encrypted_text = self.strategy.encrypt(text)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(encrypted_text)


if __name__ == "__main__":
    input_filename = "input.txt"

    # 1. Удаление гласных
    encryptor = TextFileEncryptor(RemoveVowelsStrategy())
    encryptor.encrypt_file(input_filename, "output_no_vowels.txt")

    # 2. Сдвиг на 4 символа
    encryptor.set_strategy(ShiftCipherStrategy(4))
    encryptor.encrypt_file(input_filename, "output_shift.txt")

    # 3. XOR с ключом 5
    encryptor.set_strategy(XorCipherStrategy(5))
    encryptor.encrypt_file(input_filename, "output_xor.txt")

    print("Шифрование завершено.")
