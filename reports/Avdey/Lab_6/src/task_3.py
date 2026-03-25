def repeat(pattern, count):
    if pattern is None:
        raise TypeError("Шаблон должен быть строкой.")
    if count < 0:
        raise ValueError("Число должно быть неотрицательным.")
    return pattern * count
