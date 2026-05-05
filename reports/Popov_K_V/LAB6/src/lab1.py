"""
Модуль для поиска наибольшего общего префикса (Лабораторная работа №1).
"""

def find_prefix(words):
    """
    Находит самый длинный общий префикс для списка слов.
    Выбрасывает ValueError, если список пуст.
    """
    if not words:
        raise ValueError("Список слов пуст")

    first_word = words[0]
    first_len = len(first_word)
    words_len = len(words)

    for j in range(first_len):
        char = first_word[j]
        for i in range(1, words_len):
            # Если достигли конца одного из слов или символы не совпадают
            if j == len(words[i]) or words[i][j] != char:
                return first_word[:j]
    return first_word

if __name__ == "__main__":
    user_words =[]
    try:
        const = int(input("Введите сколько будет кол-во строк: "))
        for idx in range(const):
            user_word = str(input(f"Введите слово № {idx+1} "))
            user_words.append(user_word)

        result = find_prefix(user_words)
        print("Самый длинный префикс:", result)
    except ValueError as e:
        print("Ошибка:", e)
