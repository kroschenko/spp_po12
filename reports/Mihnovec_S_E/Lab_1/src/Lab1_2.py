"""Модуль для решения задачи Two Sum."""


def twosum(target: int, nums: list[int]) -> list[int]:
    """
    Ищет два числа в списке, сумма которых равна target.

    :param target: Искомая сумма
    :param nums: Список чисел
    :return: Индексы двух чисел
    """
    pmap = {}
    for index, num in enumerate(nums):
        diff = target - num
        if diff in pmap:
            return [pmap[diff], index]
        pmap[num] = index
    return []


def setlist() -> list[int]:
    """Создает список чисел через ввод пользователя."""
    objects = []
    try:
        n = int(input("Число объектов в списке: "))
        for i in range(n):
            element = int(input(f"Введите элемент {i+1}: "))
            objects.append(element)
            print(f"Элемент {element} был добавлен в список.")
            print(f"Итоговый список: {objects}")
    except ValueError:
        print("Ошибка: нужно вводить только целые числа!")
    return objects


def settarget() -> int:
    """Запрашивает целевое число."""
    try:
        return int(input("Целевое число: "))
    except ValueError:
        print("Ошибка: нужно вводить только целые числа!")
        return 0


def main():
    """Запуск алгоритма Two Sum."""
    nums = setlist()
    target = settarget()
    result = twosum(target, nums)
    print(f"Результат: {result}")


if __name__ == "__main__":
    main()
