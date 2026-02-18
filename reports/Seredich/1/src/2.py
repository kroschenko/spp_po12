def increment_digits(digits):
    """Прибавляет 1 к числу, представленному списком цифр."""
    i = len(digits) - 1
    while i >= 0 and digits[i] == 9:
        digits[i] = 0
        i -= 1

    if i < 0:
        digits.insert(0, 1)
    else:
        digits[i] += 1

    return digits


def main():
    digits = list(map(int, input("Введите цифры через пробел: ").split()))
    print(*increment_digits(digits))


if __name__ == "__main__":
    main()
