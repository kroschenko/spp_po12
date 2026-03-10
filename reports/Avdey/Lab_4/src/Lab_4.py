import datetime
import requests
import matplotlib.pyplot as plt
import pandas as pd


def get_trending_repos(language, days, min_stars):
    date_since = datetime.datetime.now() - datetime.timedelta(days=days)
    date_since = date_since.strftime("%Y-%m-%d")

    url = "https://api.github.com/search/repositories"

    query = f"language:{language} created:>{date_since} stars:>{min_stars}"

    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 10}

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        print("Ошибка при обращении к GitHub API")
        return []

    data = response.json()

    repos = []

    for repo in data["items"]:
        repo_data = {
            "name": repo["name"],
            "author": repo["owner"]["login"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"],
            "description": repo["description"],
            "url": repo["html_url"],
        }

        repos.append(repo_data)

    return repos


def print_top_repos(repos):
    print("\nТОП самых быстрорастущих проектов:\n")

    for i, repo in enumerate(repos[:5], start=1):
        print(f"{i}. {repo['name']} (+{repo['stars']} ⭐) - {repo['description']}")


def plot_repos(repos):
    names = [repo["name"] for repo in repos[:5]]
    stars = [repo["stars"] for repo in repos[:5]]

    df = pd.DataFrame({"Repository": names, "Stars": stars})

    plt.figure(figsize=(10, 6))
    plt.bar(df["Repository"], df["Stars"])

    plt.title("Топ популярных GitHub репозиториев")
    plt.xlabel("Repository")
    plt.ylabel("Stars")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def main():
    language = input("Введите язык программирования: ")

    days = int(input("Выберите период (дней): "))

    min_stars = input("Минимальное количество звёзд (по желанию): ")

    if min_stars == "":
        min_stars = 0
    else:
        min_stars = int(min_stars)

    print(f"\nАнализируем популярные репозитории на {language} за последние {days} дней...")

    repos = get_trending_repos(language, days, min_stars)

    if not repos:
        print("Репозитории не найдены")
        return

    print_top_repos(repos)

    plot_repos(repos)


if __name__ == "__main__":
    main()
