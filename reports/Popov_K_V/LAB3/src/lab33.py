"""
Модуль реализует поведенческий паттерн проектирования Стратегия (Strategy).
Позволяет динамически менять алгоритмы шифрования текстовых файлов.
"""
# pylint: disable=too-few-public-methods

import os
from abc import ABC, abstractmethod


class EncryptionStrategy(ABC):
    """Абстрактный класс для алгоритмов шифрования."""

    @abstractmethod
    def encrypt(self, text: str) -> str:
        """Метод для выполнения шифрования текста."""


class RemoveVowelsStrategy(EncryptionStrategy):
    """Стратегия, удаляющая все гласные буквы из текста."""

    def encrypt(self, text: str) -> str:
        """Удаляет гласные (русские и английские)."""
        vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouyAEIOUY"
        return "".join(ch for ch in text if ch not in vowels)


class CaesarCipherStrategy(EncryptionStrategy):
    """Стратегия, реализующая шифр Цезаря со сдвигом."""

    def __init__(self, shift: int = 4):
        self.shift = shift
        self.alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    def encrypt(self, text: str) -> str:
        """Сдвигает буквы алфавита на заданное число позиций."""
        result = []
        for ch in text:
            if ch.lower() in self.alphabet:
                is_upper = ch.isupper()
                idx = self.alphabet.index(ch.lower())
                new_idx = (idx + self.shift) % len(self.alphabet)
                new_ch = self.alphabet[new_idx]
                result.append(new_ch.upper() if is_upper else new_ch)
            else:
                result.append(ch)
        return "".join(result)


class XorStrategy(EncryptionStrategy):
    """Стратегия шифрования через операцию XOR с ключом."""

    def __init__(self, key: str):
        self.key = key

    def encrypt(self, text: str) -> str:
        """Применяет XOR к каждому символу текста, используя ключ."""
        if not self.key:
            return text
        return "".join(
            chr(ord(text[i]) ^ ord(self.key[i % len(self.key)]))
            for i in range(len(text))
        )


class TextFileEncryptor:
    """Класс-контекст для работы с файлами через выбранную стратегию."""

    def __init__(self, strategy: EncryptionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: EncryptionStrategy):
        """Позволяет сменить стратегию шифрования во время выполнения."""
        self.strategy = strategy

    def process_file(self, input_path: str, output_path: str) -> str:
        """Считывает файл, шифрует его и сохраняет результат."""
        try:
            with open(input_path, 'r', encoding='utf-16') as input_file:
                text = input_file.read()

            encrypted = self.strategy.encrypt(text)

            with open(output_path, 'w', encoding='utf-16') as output_file:
                output_file.write(encrypted)

            print(f"[Успех] Сохранен: {output_path}")
            return encrypted
        except FileNotFoundError:
            print("Ошибка: Файл не найден.")
            return ""


if __name__ == "__main__":
    TEST_FILE = "source.txt"
    with open(TEST_FILE, 'w', encoding='utf-16') as f:
        f.write("Привет")

    encryptor_inst = TextFileEncryptor(RemoveVowelsStrategy())

    print("Удаление гласных")
    encryptor_inst.process_file(TEST_FILE, "resultNoW.txt")

    print("\nШифр Цезаря")
    encryptor_inst.set_strategy(CaesarCipherStrategy(4))
    encryptor_inst.process_file(TEST_FILE, "resultCaesr.txt")

    print("\nXOR (ключ 'secret')")
    encryptor_inst.set_strategy(XorStrategy("secret"))
    encryptor_inst.process_file(TEST_FILE, "resultXor.txt")

    os.remove(TEST_FILE)
