"""
Модуль для анализа трендовых репозиториев GitHub.
Использует GitHub REST API для поиска популярных проектов и визуализации роста.
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests


def get_trending_repositories(language, days, min_stars=0):
    """
    Получает список популярных репозиториев через GitHub Search API.
    """
    date_threshold = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    query = f"language:{language} created:>{date_threshold} stars:>={min_stars}"
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 10}

    print(f"\nАнализ репозиториев {language} за последние {days} дней...")

    try:
        # Добавлен timeout для предотвращения зависания
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])

        results = []
        for item in items:
            results.append(
                {
                    "name": item["name"],
                    "author": item["owner"]["login"],
                    "stars_period": item["stargazers_count"],
                    "description": item["description"] or "Нет описания",
                    "url": item["html_url"],
                }
            )
        return results
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при запросе к API: {error}")
        return []


def visualize_trends(repos, language):
    """
    Создает горизонтальную диаграмму топ-5 репозиториев.
    """
    if not repos:
        return

    top_repos = repos[:5]
    names = [r["name"] for r in top_repos]
    stars = [r["stars_period"] for r in top_repos]

    plt.figure(figsize=(10, 6))
    # Переименовано 'bar' в 'rects' для pylint
    rects = plt.barh(names[::-1], stars[::-1], color="skyblue")

    plt.xlabel("Количество новых звезд (⭐)")
    plt.title(f"ТОП-5 быстрорастущих проектов на {language}")

    for rect in rects:
        width = rect.get_width()
        plt.text(
            width, rect.get_y() + rect.get_height() / 2, f" +{int(width)}", va="center"
        )

    plt.tight_layout()
    filename = f"trending_{language.lower()}.png"
    plt.savefig(filename)
    print(f"\nГрафик сохранен в файл: {filename}")
    plt.show()


def main():
    """
    Основная точка входа: ввод данных пользователем и запуск анализа.
    """
    lang = input("Введите язык (например, Python): ") or "Python"
    try:
        period = int(input("Период в днях (7): ") or 7)
        min_stars = int(input("Мин. звезд (0): ") or 0)
    except ValueError:
        print("Ошибка: введите числовые значения для периода и звезд.")
        return

    trending_repos = get_trending_repositories(lang, period, min_stars)

    if trending_repos:
        print("\nТОП-5 самых быстрорастущих проектов:")
        for i, repo in enumerate(trending_repos[:5], 1):
            name = repo["name"]
            stars = repo["stars_period"]
            print(f"{i}. {name} (+{stars:,} ⭐) - {repo['url']}")

        visualize_trends(trending_repos, lang)
    else:
        print("Репозитории не найдены.")


if __name__ == "__main__":
    main()
