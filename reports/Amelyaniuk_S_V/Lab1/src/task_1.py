"""Модуль для вычисления размаха последовательности чисел."""


def range_of_sequence(numbers):
    """Вычисляет размах последовательности (разница между max и min)."""
    if not numbers:
        return 0
    return max(numbers) - min(numbers)


def main():
    """Основная функция для ввода данных и вывода результата."""
    print("=== Задание 1 ===")

    while True:
        try:
            nums_input = input("Введите целые числа через пробел: ").strip()
            if not nums_input:
                print("Ошибка: пустой ввод. Попробуйте снова.")
                continue

            numbers = list(map(int, nums_input.split()))
            break

        except ValueError:
            print("Ошибка: введите только целые числа, разделенные пробелами.")

    result = range_of_sequence(numbers)
    print(f"Введенная последовательность: {numbers}")
    print(f"Максимальное значение: {max(numbers)}")
    print(f"Минимальное значение: {min(numbers)}")
    print(f"Размах последовательности (разница между max и min): {result}")


if __name__ == "__main__":
    main()
