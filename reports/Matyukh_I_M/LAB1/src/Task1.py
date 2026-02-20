from typing import List, Union


def generate_sequence(
    start: Union[int, float], end: Union[int, float], step: Union[int, float]
) -> List[Union[int, float]]:

    if start >= end:
        raise ValueError(f"start ({start}) должно быть меньше end ({end})")

    if step <= 0:
        raise ValueError(f"step ({step}) должно быть положительным числом")

    result = []
    current = start

    while current <= end:
        result.append(current)
        current += step

    return result


def get_positive_number(prompt: str) -> float:

    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Ошибка: введите корректное число")


def main():
    print("Генератор последовательности чисел")
    print("-" * 35)

    while True:
        try:
            start = get_positive_number("Введите начало последовательности: ")
            end = get_positive_number("Введите конец последовательности: ")
            step = get_positive_number("Введите шаг: ")

            sequence = generate_sequence(start, end, step)

            print(f"\nРезультат: {sequence}")
            print(f"Количество элементов: {len(sequence)}")

            again = input(
                "\nХотите создать другую последовательность? (да/нет): "
            ).lower()
            if again != "да" and again != "yes" and again != "y":
                print("Программа завершена.")
                break

        except ValueError as e:
            print(f"Ошибка: {e}")
            print("Попробуйте снова.\n")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем.")
            break


if __name__ == "__main__":
    main()
