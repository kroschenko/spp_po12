"""GitHub repository contributors analyzer.

This module analyzes the most active contributors in a GitHub repository
over a specified time period using the GitHub API.
"""

import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import requests


HEADERS = {}


def get_user_input():
    """Get repository analysis parameters from user."""
    repository = input("Введите репозиторий (owner/repo): ").strip()
    days = int(input("Выберите период (7 / 30 / 365 дней): ").strip())
    min_commits_input = input(
        "Минимальное количество коммитов для рейтинга (Enter, чтобы пропустить): "
    ).strip()
    min_commits_value = int(min_commits_input) if min_commits_input.isdigit() else 0
    return repository, days, min_commits_value


def fetch_contributors(repository):
    """Fetch all contributors from a GitHub repository."""
    url = f"https://api.github.com/repos/{repository}/contributors"
    params = {"anon": "false", "per_page": 100}
    contributors = []
    page = 1

    while True:
        try:
            params["page"] = page
            response = requests.get(
                url, headers=HEADERS, params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            contributors.extend([c for c in data if c.get("login")])
            page += 1
            time.sleep(0.1)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении списка контрибьюторов: {e}")
            break
    return {c["login"]: c["contributions"] for c in contributors}


def fetch_commits_since(repository, since_date):
    """Fetch commits from a repository since a specific date."""
    url = f"https://api.github.com/repos/{repository}/commits"
    params = {"since": since_date, "per_page": 100}
    authors_commits = {}
    page = 1

    while True:
        try:
            params["page"] = page
            response = requests.get(
                url, headers=HEADERS, params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            for commit in data:
                author_login = commit.get("author")
                if author_login and author_login.get("login"):
                    login = author_login["login"]
                    authors_commits[login] = authors_commits.get(login, 0) + 1
            page += 1
            if page % 3 == 0:
                time.sleep(0.5)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении коммитов: {e}")
            break
    return authors_commits


def fetch_user_prs(repository, author, since_date):
    """Fetch number of PRs created by a user since a specific date."""
    url = "https://api.github.com/search/issues"
    query = f"repo:{repository} type:pr author:{author} created:>={since_date}"
    params = {"q": query}
    try:
        response = requests.get(
            url, headers=HEADERS, params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data["total_count"]
    except requests.exceptions.RequestException:
        return 0


def fetch_user_issues(repository, author, since_date):
    """Fetch number of issues created by a user since a specific date."""
    url = "https://api.github.com/search/issues"
    query = f"repo:{repository} type:issue author:{author} created:>={since_date}"
    params = {"q": query}
    try:
        response = requests.get(
            url, headers=HEADERS, params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data["total_count"]
    except requests.exceptions.RequestException:
        return 0


def fetch_user_comments(repository, author, since_date):
    """Fetch number of comments by a user since a specific date."""
    url = "https://api.github.com/search/issues"
    query = f"repo:{repository} commenter:{author} updated:>={since_date}"
    params = {"q": query}
    try:
        response = requests.get(
            url, headers=HEADERS, params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data["total_count"]
    except requests.exceptions.RequestException:
        return 0


def analyze_contributors(repository, period_days, min_commits_threshold):
    """Analyze contributors and return top 5 by activity."""
    since = (datetime.now() - timedelta(days=period_days)).isoformat() + "Z"
    print(f"Анализ активности с {since}...")

    fetch_contributors(repository)
    active_committers = fetch_commits_since(repository, since)

    results = []
    for login, commits in active_committers.items():
        if commits < min_commits_threshold:
            continue

        print(f"Обработка {login}...")
        prs = fetch_user_prs(repository, login, since)
        issues = fetch_user_issues(repository, login, since)
        comments = fetch_user_comments(repository, login, since)

        total_activity_score = commits + prs + issues + comments

        results.append(
            {
                "login": login,
                "commits": commits,
                "prs": prs,
                "issues": issues,
                "comments": comments,
                "score": total_activity_score,
            }
        )
        time.sleep(0.2)

    top_5 = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
    return top_5


def plot_top_contributors(top_5, repo_name):
    """Generate and save a bar chart of top contributors."""
    if not top_5:
        print("Нет данных для построения графика.")
        return

    logins = [f"@{c['login']}" for c in top_5]
    commits = [c["commits"] for c in top_5]
    prs = [c["prs"] for c in top_5]
    issues = [c["issues"] for c in top_5]

    x = np.arange(len(logins))
    width = 0.25

    _, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width, commits, width, label="Коммиты", color="skyblue")
    rects2 = ax.bar(x, prs, width, label="Pull Requests", color="lightcoral")
    rects3 = ax.bar(x + width, issues, width, label="Issues", color="lightgreen")

    ax.set_xlabel("Контрибьюторы")
    ax.set_ylabel("Количество")
    ax.set_title(f"ТОП-5 активных контрибьюторов в {repo_name}")
    ax.set_xticks(x)
    ax.set_xticklabels(logins, rotation=45, ha="right")
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.bar_label(rects3, padding=3)

    plt.tight_layout()

    filename = repo_name.replace("/", "_") + "_contributors.png"
    plt.savefig(filename, dpi=150)
    print(f"График активности сохранен в '{filename}'")
    plt.show()


def print_top_table(top_5):
    """Print top contributors in a formatted table."""
    print("\n" + "=" * 80)
    print("ТОП-5 активных контрибьюторов:")
    print("=" * 80)
    for i, contributor in enumerate(top_5, 1):
        print(
            f"{i}. @{contributor['login']} - {contributor['commits']} коммитов, "
            f"{contributor['prs']} PR, {contributor['issues']} issues, "
            f"{contributor['comments']} комментариев"
        )
    print("=" * 80)


if __name__ == "__main__":
    REPO, PERIOD, MIN_COMMITS = get_user_input()
    top_contributors = analyze_contributors(REPO, PERIOD, MIN_COMMITS)

    if top_contributors:
        print_top_table(top_contributors)
        plot_top_contributors(top_contributors, REPO)
    else:
        print("Не найдено контрибьюторов, удовлетворяющих условиям.")
