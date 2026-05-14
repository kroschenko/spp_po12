"""Lab1 module"""


def generate_sequence(start: int, end: int, step: int) -> list[int]:
    """
    Возвращает список чисел от start до end (не включая) с шагом step.

    Raises:
        ValueError: если step == 0 (бесконечный цикл).
        ValueError: если step имеет «неправильный» знак и диапазон никогда
                    не будет пройден (например, start < end, но step < 0).
    """
    if step == 0:
        raise ValueError("step не может быть равен нулю.")
    if start < end and step < 0:
        raise ValueError(
            f"Недостижимый диапазон: start={start} < end={end}, но step={step} < 0."
        )
    if start > end and step > 0:
        raise ValueError(
            f"Недостижимый диапазон: start={start} > end={end}, но step={step} > 0."
        )
    return list(range(start, end, step))


def rep():
    """Консольная обёртка для generate_sequence."""
    start = int(input("Enter a starting number: "))
    end = int(input("Enter an ending number: "))
    step = int(input("Enter a step: "))
    for i in generate_sequence(start, end, step):
        print(i)


def is_palindrome(phrase: str) -> bool:
    """
    Возвращает True, если фраза является палиндромом
    (без учёта регистра и не-буквенно-цифровых символов).

    Raises:
        TypeError: если передан не строковый аргумент.
    """
    if not isinstance(phrase, str):
        raise TypeError(f"Ожидается str, получен {type(phrase).__name__}.")
    cleaned = "".join(c for c in phrase.lower() if c.isalnum())
    return cleaned == cleaned[::-1]


def check_palindrome():
    """Консольная обёртка для is_palindrome."""
    phrase = input("Enter a phrase: ")
    print(is_palindrome(phrase))
