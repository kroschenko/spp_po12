def median(sequence):
    seq = sorted(sequence)
    n = len(seq)

    if n % 2 == 1:
        return seq[n // 2]

    mid1 = seq[n // 2 - 1]
    mid2 = seq[n // 2]
    return (mid1 + mid2) / 2


N = int(input("Введите количество элементов: "))
numbers = []

for _ in range(N):
    numbers.append(int(input()))

print("Медиана:", median(numbers))
