def find_mode(sequence):
    if not sequence:
        return None

    # Считаем частоту каждого уникального элемента
    counts = {x: sequence.count(x) for x in set(sequence)}
    max_freq = max(counts.values())

    # Проверка на отсутствие моды (если все элементы встречаются одинаково часто)
    if all(count == max_freq for count in counts.values()):
        return None

    return [item for item, freq in counts.items() if freq == max_freq]


seq = [1, 2, 2, 3, 3, 5]
print(find_mode(seq))
