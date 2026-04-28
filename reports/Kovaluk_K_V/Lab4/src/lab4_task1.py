import datetime
import json
import sys
import urllib.request
import urllib.error


class GitHubTopRepos:
    def __init__(self):
        self.base_url = "https://api.github.com"

    def _make_request(self, url, params=None):
        if params:
            url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

        try:
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                return json.loads(data.decode('utf-8'))
        except urllib.error.URLError as e:
            print(f"Ошибка при обращении к GitHub API: {e}")
            return None

    def search_repos(self, keyword, per_page=10):
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": keyword,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page
        }

        data = self._make_request(url, params)

        if not data or "items" not in data:
            print("Ошибка при обращении к GitHub API")
            return []

        return data.get("items", [])

    def get_last_commit_date(self, full_name):
        url = f"{self.base_url}/repos/{full_name}/commits"
        params = {"per_page": 1}

        try:
            data = self._make_request(url, params)
            if data and len(data) > 0:
                commit_date = data[0].get("commit", {}).get("committer", {}).get("date", "")
                if commit_date:
                    dt = datetime.datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
                    return dt.strftime("%Y-%m-%d")
            return "N/A"
        except Exception:
            return "N/A"

    def get_repo_info(self, repo):
        full_name = repo.get("full_name", "N/A")
        description = repo.get("description", "Нет описания")
        if description is None:
            description = "Нет описания"

        return {
            "name": repo.get("name", "N/A"),
            "full_name": full_name,
            "description": description,
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", "Не указан"),
            "url": repo.get("html_url", "N/A"),
            "last_commit": self.get_last_commit_date(full_name)
        }

    def display_repos(self, repos):
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
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False


def main():
    print("Автоматический мониторинг популярных репозиториев GitHub")
    print("-" * 50)

    keyword = input("Введите ключевое слово для поиска репозиториев: ").strip()

    if not keyword:
        print("Ошибка: ключевое слово не может быть пустым")
        sys.exit(1)

    monitor = GitHubTopRepos()

    print(f"\nПоиск топ-10 репозиториев по запросу \"{keyword}\"...")

    repos = monitor.search_repos(keyword)

    if not repos:
        print("Репозитории не найдены")
        sys.exit(1)

    print(f"Найдено {len(repos)} репозиториев. Сбор данных...")

    repos_info = []
    for repo in repos:
        repos_info.append(monitor.get_repo_info(repo))

    monitor.display_repos(repos_info)
    monitor.save_to_json(repos_info)

    print("\nМониторинг завершён!")


if __name__ == "__main__":
    main()
