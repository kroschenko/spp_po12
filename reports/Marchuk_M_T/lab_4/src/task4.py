"""
Модуль для автоматического анализа трендов популярных репозиториев GitHub.
Использует GitHub Search API для поиска самых быстрорастущих проектов.
"""

from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt


def get_trending_repositories(language, days, min_stars=0):
    """
    Получает список популярных репозиториев через GitHub API.

    :param language: Язык программирования (Python, JavaScript и др.)
    :param days: Период анализа в днях (7 или 30)
    :param min_stars: Минимальное количество звезд для фильтрации
    :return: Список словарей с данными репозиториев
    """
    date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    query = f"language:{language} created:>{date_threshold} stars:>={min_stars}"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }
    url = "https://api.github.com/search/repositories"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при запросе к API: {error}")
        return []


def visualize_trends(repos, language, days):
    """
    Строит столбчатую диаграмму популярности репозиториев.

    :param repos: Список репозиториев
    :param language: Язык программирования
    :param days: Период в днях
    """
    if not repos:
        print("Нет данных для визуализации.")
        return

    names = [repo['name'] for repo in repos]
    stars = [repo['stargazers_count'] for repo in repos]

    plt.figure(figsize=(10, 6))
    plt.bar(names, stars, color='skyblue')
    plt.xlabel('Репозиторий')
    plt.ylabel('Количество звезд (всего)')
    plt.title(f'ТОП-5 быстрорастущих проектов на {language} за {days} дней')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    filename = f"trending_{language.lower()}.png"
    plt.savefig(filename)
    print(f"\nГрафик роста сохранен в файл: {filename}")
    plt.show()


def main():
    """
    Основная функция для взаимодействия с пользователем.
    """
    print("--- Анализ трендов GitHub ---")
    lang = input("Введите язык программирования: ").strip()
    try:
        period = int(input("Выберите период (7 / 30 дней): ").strip())
        min_s = input("Минимальное количество звезд (по желанию): ").strip()
        min_s = int(min_s) if min_s else 0
    except ValueError:
        print("Ошибка: введено нечисловое значение.")
        return

    print(f"\nАнализируем популярные репозитории на {lang} за последние {period} дней...")
    repositories = get_trending_repositories(lang, period, min_s)

    if not repositories:
        print("По вашему запросу ничего не найдено.")
        return

    print("\nТОП-5 самых быстрорастущих проектов:")
    for i, repo in enumerate(repositories, 1):
        print(f"{i}. **{repo['name']}** (+{repo['stargazers_count']} ⭐)")
        print(f"   Автор: {repo['owner']['login']}")
        print(f"   Форков: {repo['forks_count']} | Язык: {repo['language']}")
        desc = repo['description'] if repo['description'] else "Нет описания"
        print(f"   Описание: {desc}")
        print(f"   Ссылка: {repo['html_url']}\n")

    visualize_trends(repositories, lang, period)


if __name__ == "__main__":
    main()
