def merge(nums1, m, nums2, n):

    # Указатели на текущие позиции (с конца)
    i = m - 1  # последний значимый элемент в nums1
    j = n - 1  # последний элемент в nums2
    k = m + n - 1  # позиция для вставки в nums1

    # Пока есть элементы в обоих списках
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1

    # Если остались элементы в nums2 (в nums1 они уже на месте)
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1

    return nums1


def input_sorted_list(name, count, allow_zeros=False):
    """Ввод отсортированного списка с проверкой"""
    print(f"\nВвод списка {name} ({count} элементов):")
    result = []
    for i in range(count):
        while True:
            try:
                num = int(input(f"  Элемент {i + 1}: "))
                # Проверка на неубывающий порядок
                if i > 0 and num < result[-1]:
                    print("  Ошибка: список должен быть отсортирован по неубыванию!")
                    continue
                result.append(num)
                break
            except ValueError:
                print("  Ошибка: введите целое число!")

    # Если нужно добавить нули (для nums1)
    if allow_zeros:
        result.extend([0] * allow_zeros)
        print(f"  (добавлено {allow_zeros} нулей в конец для слияния)")

    return result


def main():
    print("=" * 50)
    print("СЛИЯНИЕ ДВУХ ОТСОРТИРОВАННЫХ СПИСКОВ")
    print("=" * 50)

    # Ввод параметров
    print("\n--- Ввод параметров ---")

    # Ввод m и n
    while True:
        try:
            m = int(input("Введите m (количество элементов в nums1): "))
            n = int(input("Введите n (количество элементов в nums2): "))
            if m < 0 or n < 0:
                print("Числа должны быть неотрицательными!")
                continue
            break
        except ValueError:
            print("Введите целые числа!")

    # Ввод nums1 (только m значимых элементов)
    nums1 = input_sorted_list("nums1", m, allow_zeros=n)

    # Ввод nums2 (n элементов)
    nums2 = input_sorted_list("nums2", n)

    # Вывод исходных данных
    print("\n" + "=" * 50)
    print("ИСХОДНЫЕ ДАННЫЕ:")
    print(f"  nums1 = {nums1}")
    print(f"  m = {m}")
    print(f"  nums2 = {nums2}")
    print(f"  n = {n}")

    # Выполнение слияния
    merge(nums1, m, nums2, n)

    # Вывод результата
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТ:")
    print(f"  nums1 = {nums1}")
    print("=" * 50)


# Запуск программы
if __name__ == "__main__":
    main()
