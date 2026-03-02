def process_sequence():
    # Ввод последовательности
    n = int(input("Введите количество элементов N: "))
    sequence = []

    print(f"Введите {n} целых чисел:")
    for i in range(n):
        num = int(input(f"Элемент {i + 1}: "))
        sequence.append(num)

    # Вычисления
    max_val = max(sequence)
    min_val = min(sequence)
    sum_val = sum(sequence)

    # Произведение (с защитой от переполнения для больших чисел)
    prod_val = 1
    for num in sequence:
        prod_val *= num

    # Вывод результатов
    print(f"\nРезультаты обработки последовательности {sequence}:")
    print(f"Максимальное значение: {max_val}")
    print(f"Минимальное значение: {min_val}")
    print(f"Сумма элементов: {sum_val}")
    print(f"Произведение элементов: {prod_val}")


# Запуск
process_sequence()
