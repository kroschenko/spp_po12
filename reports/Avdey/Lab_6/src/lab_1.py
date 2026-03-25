def all_elements_equal(data: list) -> bool:
    return bool(data) and len(set(data)) == 1


def find_two_sum(arr: list[int], target: int) -> list[int] | None:
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                return [i, j]
    return None
