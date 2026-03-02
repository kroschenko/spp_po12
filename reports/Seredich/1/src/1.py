def median(numbers):
    """Возвращает медиану списка чисел."""
    numbers.sort()
    n = len(numbers)
    mid = n // 2

    if n % 2 == 1:
        return numbers[mid]
    return (numbers[mid - 1] + numbers[mid]) / 2


def main():
    n = int(input("Введите количество чисел: "))
    nums = list(map(int, input("Введите числа через пробел: ").split()))
    print(median(nums))


if __name__ == "__main__":
    main()
