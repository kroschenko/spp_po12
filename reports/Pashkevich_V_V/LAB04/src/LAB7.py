import json
from datetime import datetime
import requests


def monitor_popular_repos():
    """Функция для мониторинга популярных репозиториев GitHub."""
    keyword = input("Введите ключевое слово для поиска репозиториев: ")

    url = "https://api.github.com/search/repositories"
    params = {
        'q': keyword,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 10
    }

    print(f"Поиск топ-10 репозиториев по запросу '{keyword}'...")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = data.get('items', [])
        results_to_save = []

        print(f"\nТоп-10 репозиториев по запросу \"{keyword}\":")

        for i, repo in enumerate(items, 1):
            name = repo.get('full_name')
            description = repo.get('description') or "Нет описания"
            stars = repo.get('stargazers_count')
            forks = repo.get('forks_count')
            last_push = repo.get('pushed_at')
            formatted_date = datetime.strptime(last_push, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

            repo_info = {
                "rank": i,
                "name": name,
                "description": description,
                "stars": stars,
                "forks": forks,
                "last_commit": formatted_date
            }
            results_to_save.append(repo_info)

            print(f"{i}. {name} - ⭐{stars:,}, {forks:,} (Last commit: {formatted_date})")

        with open('github_top_repos.json', 'w', encoding='utf-8') as f:
            json.dump(results_to_save, f, ensure_ascii=False, indent=4)

        print("\nРезультаты сохранены в github_top_repos.json")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при обращении к API: {e}")


if __name__ == "__main__":
    monitor_popular_repos()
