def all_elements_equal(data: list) -> bool:
    return bool(data) and len(set(data)) == 1


def find_two_sum(arr: list[int], target: int) -> list[int] | None:
    for i, first in enumerate(arr):
        for j, second in enumerate(arr[i + 1:], start=i + 1):
            if first + second == target:
                return [i, j]
    return None
