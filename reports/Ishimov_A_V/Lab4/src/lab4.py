import json
import requests
import matplotlib.pyplot as plt


def get_repositories(keyword):
    url = "https://api.github.com/search/repositories"

    params = {"q": keyword, "sort": "stars", "order": "desc", "per_page": 10}

    response = requests.get(url, params=params)
    data = response.json()

    repos = []

    for repo in data["items"]:
        repo_data = {
            "name": repo["full_name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "last_commit": repo["updated_at"],
        }

        repos.append(repo_data)

    return repos


def print_repositories(repos, keyword):
    print(f"\nТоп-10 репозиториев по запросу '{keyword}':\n")

    for i, repo in enumerate(repos, 1):
        date = repo["last_commit"][:10]

        print(f"{i}. {repo['name']} - ⭐{repo['stars']}, " f"{repo['forks']} forks (Last commit: {date})")


def save_to_json(repos):
    with open("github_top_repos.json", "w", encoding="utf-8") as file:
        json.dump(repos, file, indent=4, ensure_ascii=False)

    print("\nРезультаты сохранены в github_top_repos.json")


def plot_graph(repos):
    names = [repo["name"].split("/")[1] for repo in repos]
    stars = [repo["stars"] for repo in repos]

    plt.figure(figsize=(12, 6))
    plt.barh(names, stars)

    plt.xlabel("Количество звезд")
    plt.ylabel("Репозитории")
    plt.title("Топ репозиториев GitHub")

    plt.gca().invert_yaxis()
    plt.show()


def main():
    keyword = input("Введите ключевое слово для поиска репозиториев: ")

    repos = get_repositories(keyword)

    print_repositories(repos, keyword)

    save_to_json(repos)

    plot_graph(repos)


if __name__ == "__main__":
    main()
