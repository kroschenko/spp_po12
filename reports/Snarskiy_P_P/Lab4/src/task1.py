"""Devs activity in open-source project"""

from collections import defaultdict
import requests
import matplotlib.pyplot as plt

TOKEN = (
    "github_pat_11AOUI3YQ0IMsTkos8r0cb_AJN3yBQsIoRPiRdr4AEv"
    "uS7rg1wwtjPvb1dEi5PSsZIU57KQI43fk8nYgBD"
)
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}


def get_contributors(owner, repo):
    """Gets contributors for a repo"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    response = requests.get(url, headers=HEADERS, timeout=30)
    return response.json()


def get_user_stats(owner, repo, username):
    """Gets user stats for a repo"""
    stats = defaultdict(int)

    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {"creator": username, "state": "all", "per_page": 100}
    issues = requests.get(issues_url, headers=HEADERS, params=params, timeout=30).json()

    for item in issues:
        if "pull_request" in item:
            if item["state"] == "open":
                stats["open_pr"] += 1
            else:
                stats["closed_pr"] += 1
        else:
            if item["state"] == "open":
                stats["open_issues"] += 1
            else:
                stats["closed_issues"] += 1

    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"author": username, "per_page": 1}
    commits = requests.get(
        commits_url, headers=HEADERS, params=params, timeout=30
    ).json()

    if isinstance(commits, list) and commits:
        stats["last_activity"] = commits[0]["commit"]["author"]["date"]
    else:
        stats["last_activity"] = "N/A"

    return stats


def main():
    """Main function"""
    repo_input = input("Введите репозиторий (owner/repo): ")
    owner, repo = repo_input.split("/")

    print(f'Анализируем вклад контрибьюторов в "{repo_input}"...')

    contributors = get_contributors(owner, repo)

    results = []

    for user in contributors[:10]:
        username = user["login"]
        commits = user["contributions"]

        stats = get_user_stats(owner, repo, username)

        total_score = (
            commits
            + stats["open_pr"]
            + stats["closed_pr"]
            + stats["open_issues"]
            + stats["closed_issues"]
        )

        results.append(
            {
                "user": username,
                "commits": commits,
                "open_pr": stats["open_pr"],
                "closed_pr": stats["closed_pr"],
                "open_issues": stats["open_issues"],
                "closed_issues": stats["closed_issues"],
                "last_activity": stats["last_activity"],
                "score": total_score,
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)

    print("\nТОП-5 самых активных разработчиков:")
    for i, user in enumerate(results[:5], start=1):
        print(
            f'{i}. {user["user"]} - '
            f'{user["commits"]} коммитов, '
            f'{user["open_pr"] + user["closed_pr"]} PR, '
            f'{user["open_issues"] + user["closed_issues"]} issues'
        )

    names = [u["user"] for u in results[:5]]
    scores = [u["score"] for u in results[:5]]

    plt.figure()
    plt.bar(names, scores)
    plt.title(f"Top contributors: {repo_input}")
    plt.xlabel("Developers")
    plt.ylabel("Score")
    plt.xticks(rotation=30)

    filename = f"{repo}_contributors.png"
    plt.savefig(filename)

    print(f'\nГрафик сохранен в "{filename}"')


if __name__ == "__main__":
    main()
