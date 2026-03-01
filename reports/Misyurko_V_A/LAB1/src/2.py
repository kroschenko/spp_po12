if __name__ == "__main__":
    n = int(input("Введите n: "))

    if n == 0:
        print(1)
    elif n == 1:
        print(1)
    else:
        a = 1  # ways to reach step 0
        b = 1  # ways to reach step 1

        for _ in range(2, n + 1):
            a, b = b, a + b

        print(b)
