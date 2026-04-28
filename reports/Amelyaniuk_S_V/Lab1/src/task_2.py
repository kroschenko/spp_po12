def longest_common_prefix(strs):
    if not strs:
        return ""
    
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def main():
    print("=== Задание 2 ===")
    
    while True:
        try:
            n = int(input("Сколько строк вы хотите ввести? (минимум 2): "))
            if n < 2:
                print("Нужно минимум 2 строки. Попробуйте снова.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число.")
    
    strings = []
    for i in range(n):
        s = input(f"Введите строку {i+1}: ").strip()
        strings.append(s)
    
    result = longest_common_prefix(strings)
    print(f"\nВведенные строки: {strings}")
    
    if result:
        print(f"Самая длинная общая строка префикса: '{result}'")
        print(f"Длина общего префикса: {len(result)} символов")
    else:
        print("У введенных строк нет общего префикса")

if __name__ == "__main__":
    main()