if __name__ == "__main__":
    n = int(input("Введите количество элементов: "))
    nums = list(map(int, input("Введите числа через пробел: ").split()))

    nums.sort(reverse=True)

    print(*nums)
