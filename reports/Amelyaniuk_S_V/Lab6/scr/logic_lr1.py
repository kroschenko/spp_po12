def check_age(age):
    if not isinstance(age, (int, float)):
        raise TypeError("Возраст должен быть числом")
    if age < 0:
        raise ValueError("Возраст не может быть меньше 0")
    return age >= 18
