"""Модуль для анализа последовательности чисел."""


def analyze_numbers(numbers):
    """Анализирует последовательность чисел и распределяет их по количеству цифр."""

    distribution = {}

    for num in numbers:
        num_digits = len(str(abs(num)))

        if num_digits == 1:
            key = "1-циферные"
        elif num_digits == 2:
            key = "2-циферные"
        elif num_digits == 3:
            key = "3-циферные"
        else:
            key = f"{num_digits}-циферные"

        distribution[key] = distribution.get(key, 0) + 1

    return distribution


def print_distribution(distribution):
    """Выводит распределение чисел в удобном формате."""

    print("\nРаспределение чисел по количеству цифр:")

    for category, count in sorted(distribution.items()):
        print(f"{category}: {count} шт.")


def main():
    """Основная функция программы, обрабатывающая ввод пользователя."""
    try:
        n = int(input("Введите количество чисел N: "))

        if n <= 0:
            print("Ошибка: N должно быть положительным числом")
            return

        numbers = []
        print(f"\nВведите {n} целых чисел (каждое с новой строки):")

        for i in range(n):
            while True:
                try:
                    num = int(input(f"Число {i + 1}: "))
                    numbers.append(num)
                    break
                except ValueError:
                    print("Ошибка: введите целое число")

        distribution = analyze_numbers(numbers)

        print(f"\nИсходная последовательность из {n} чисел:")
        print(numbers)

        print_distribution(distribution)

    except ValueError:
        print("Ошибка: введите корректное целое число для N")


if __name__ == "__main__":

    main()
