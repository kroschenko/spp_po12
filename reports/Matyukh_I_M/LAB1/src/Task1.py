def generate_sequence(start, end, step):
    if start >= end:
        raise ValueError("Начало должно быть меньше конца")
    if step <= 0:
        raise ValueError("Шаг должен быть положительным")

    result = []
    current = start
    while current <= end:
        result.append(current)
        current += step
    return result


def main():
    print("Генератор последовательности чисел")
    print("-" * 30)

    while True:
        try:

            start = float(input("Начало: "))
            end = float(input("Конец: "))
            step = float(input("Шаг: "))

            sequence = generate_sequence(start, end, step)

            print(f"\nРезультат: {sequence}")
            print(f"Количество: {len(sequence)}")

            if input("\nЕщё? (д/н): ").lower() not in ["д", "да", "y", "yes"]:
                print("Пока!")
                break

        except ValueError as e:
            print(f"Ошибка: {e}")
        except KeyboardInterrupt:
            print("\nДо свидания!")
            break


if __name__ == "__main__":
    main()
