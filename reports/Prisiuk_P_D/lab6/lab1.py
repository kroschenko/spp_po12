"""Модуль для работы с числами: перемешивание и поиск мажоритарного элемента."""

import random


def task_1_shuffle_numbers(n):
    """Возвращает перемешанный список чисел от 1 до n."""
    if not isinstance(n, int):
        raise TypeError("n должно быть целым числом")
    if n < 0:
        raise ValueError("n не может быть отрицательным")

    numbers = list(range(1, n + 1))
    random.shuffle(numbers)
    return numbers


def task_2_majority_element(nums):
    """Находит элемент большинства (алгоритм Бойера-Мура)."""
    if not nums:
        raise ValueError("Список не может быть пустым")

    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num

        if num == candidate:
            count += 1
        else:
            count -= 1

    return candidate


if __name__ == "__main__":
    print(f"task 1\n{task_1_shuffle_numbers(10)}\n{'-' * 30}")

    test_nums_1 = [3, 2, 3]
    test_nums_2 = [1, 2, 1, 1, 1, 2, 2]

    print("task 2")
    print(f"Input: {test_nums_1} -> Output: {task_2_majority_element(test_nums_1)}")
    print(f"Input: {test_nums_2} -> Output: {task_2_majority_element(test_nums_2)}")
