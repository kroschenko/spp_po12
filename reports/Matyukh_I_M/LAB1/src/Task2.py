def is_palindrome(s: str) -> bool:

    cleaned = "".join(char.lower() for char in s if char.isalnum())

    return cleaned == cleaned[::-1]


def main():
    print("🔍 ПРОВЕРКА ПАЛИНДРОМА")
    print("-" * 30)

    while True:
        s = input("\nВведите строку (или 'exit' для выхода): ").strip()

        if s.lower() in ["exit", "quit", "выход"]:
            print("До свидания!")
            break

        if not s:
            print("Строка не может быть пустой!")
            continue

        result = is_palindrome(s)

        if result:
            print(f"✅ '{s}' - ЭТО ПАЛИНДРОМ!")

            cleaned = "".join(char.lower() for char in s if char.isalnum())
            print(f"   Очищенная версия: {cleaned}")
            print(f"   Перевернутая: {cleaned[::-1]}")
        else:
            print(f"❌ '{s}' - НЕ ПАЛИНДРОМ")


if __name__ == "__main__":
    main()
