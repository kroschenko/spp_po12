from collections import Counter


def find_mode(sequence):
    counts = Counter(sequence)
    max_count = max(counts.values())

    if list(counts.values()).count(max_count) == len(counts):
        return None

    modes = [num for num, freq in counts.items() if freq == max_count]
    return modes


seq = [1, 2, 2, 3, 3, 5, 3]
print(find_mode(seq))
