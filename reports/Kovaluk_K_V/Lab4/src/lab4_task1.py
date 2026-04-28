import datetime
import json
import sys
import urllib.parse
import urllib.request
import urllib.error


class GitHubTopRepos:
    """Класс для поиска популярных репозиториев на GitHub."""

    def __init__(self):
        self.base_url = "https://api.github.com"

    def _make_request(self, url, params=None):
        """Вспомогательный метод для выполнения HTTP-запросов."""
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"

        try:
            req = urllib.request.Request(
                url,
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                return json.loads(data.decode('utf-8'))
        except (urllib.error.URLError, json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Ошибка при обращении к GitHub API: {e}")
            return None

    def search_repos(self, keyword, per_page=10):
        """Поиск репозиториев по ключевому слову."""
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": keyword,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page
        }

        data = self._make_request(url, params)

        if not data or "items" not in data:
            return []

        return data.get("items", [])

    def get_last_commit_date(self, full_name):
        """Получение даты последнего коммита для репозитория."""
        url = f"{self.base_url}/repos/{full_name}/commits"
        params = {"per_page": 1}

        try:
            data = self._make_request(url, params)
            if isinstance(data, list) and data:
                commit_info = data[0].get("commit", {}).get("committer", {})
                commit_date = commit_info.get("date", "")
                if commit_date:
                    dt_str = commit_date.replace('Z', '+00:00')
                    dt = datetime.datetime.fromisoformat(dt_str)
                    return dt.strftime("%Y-%m-%d")
            return "N/A"
        except (KeyError, IndexError, ValueError):
            return "N/A"

    def get_repo_info(self, repo):
        """Формирование словаря с краткой информацией о репозитории."""
        full_name = repo.get("full_name", "N/A")
        description = repo.get("description") or "Нет описания"

        return {
            "name": repo.get("name", "N/A"),
            "full_name": full_name,
            "description": description,
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language") or "Не указан",
            "url": repo.get("html_url", "N/A"),
            "last_commit": self.get_last_commit_date(full_name)
        }

    def display_repos(self, repos):
        """Вывод списка репозиториев в консоль."""
        print("\nТоп-10 репозиториев по запросу:")
        print("-" * 60)

        for i, repo in enumerate(repos, 1):
            print(f"{i}. {repo['full_name']}")
            print(f"   Звёзды: {repo['stars']}, Форки: {repo['forks']}")
            print(f"   Язык: {repo['language']}")
            print(f"   Последний коммит: {repo['last_commit']}")
            desc = repo['description']
            if len(desc) > 80:
                desc = desc[:80] + "..."
            print(f"   Описание: {desc}")
            print(f"   URL: {repo['url']}")
            print()

    def save_to_json(self, repos, filename="github_top_repos.json"):
        """Сохранение собранных данных в JSON файл."""
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total_repos": len(repos),
            "repositories": repos
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\nРезультаты сохранены в {filename}")
            return True
        except OSError as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


def main():
    """Основная функция программы."""
    print("Автоматический мониторинг популярных репозиториев GitHub")
    print("-" * 50)

    user_input = input("Введите ключевое слово для поиска: ").strip()

    if not user_input:
        print("Ошибка: ключевое слово не может быть пустым")
        sys.exit(1)

    monitor = GitHubTopRepos()
    print(f"\nПоиск топ-10 репозиториев по запросу \"{user_input}\"...")

    found_repos = monitor.search_repos(user_input)

    if not found_repos:
        print("Репозитории не найдены или произошла ошибка API")
        sys.exit(1)

    print(f"Найдено {len(found_repos)} репозиториев. Сбор данных...")

    repos_info = [monitor.get_repo_info(repo) for repo in found_repos]

    monitor.display_repos(repos_info)
    monitor.save_to_json(repos_info)

    print("\nМониторинг завершён!")


if __name__ == "__main__":
    main()
