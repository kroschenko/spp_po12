"""
Модуль для автоматизированного мониторинга активности репозиториев GitHub.
Использует GitHub REST API для сбора статистики за указанный период.
"""
import re
from datetime import datetime, timezone, timedelta
import requests

GITHUB_TOKEN = ""

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


def get_time_threshold(hours):
    """Вычисляет время N часов назад в формате ISO 8601 (UTC)."""
    threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
    return threshold.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_commits(repo, since_time):
    """Возвращает количество новых коммитов с момента since_time."""
    url = f"https://api.github.com/repos/{repo}/commits"
    params = {"since": since_time}
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if response.status_code == 200:
        return len(response.json())
    return 0


def get_issues_and_prs(repo, since_time):
    """Собирает статистику по новым и закрытым Issues и Pull Requests."""
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {"since": since_time, "state": "all"}
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)

    stats = [0, 0, 0, 0]

    if response.status_code == 200:
        for item in response.json():
            is_pr = "pull_request" in item
            is_closed = item["state"] == "closed"
            if is_pr:
                stats[0] += 1
                if is_closed:
                    stats[1] += 1
            else:
                stats[2] += 1
                if is_closed:
                    stats[3] += 1
    return stats


def get_mentions(repo, since_time):
    """Ищет уникальные упоминания @username в комментариях к Issues."""
    url = f"https://api.github.com/repos/{repo}/issues/comments"
    params = {"since": since_time}
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)

    mentions = set()
    if response.status_code == 200:
        for comment in response.json():
            body = comment.get("body", "")
            if body:
                found = re.findall(r'@([A-Za-z0-9_-]+)', body)
                mentions.update(found)
    return list(mentions)


def get_events_stats(repo, since_time):
    """Собирает данные о звездах, форках и контрибьюторах через ленту событий."""
    url = f"https://api.github.com/repos/{repo}/events"
    new_stars, new_forks = 0, 0
    contributors = set()

    for page in range(1, 4):
        params = {"per_page": 100, "page": page}
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code != 200:
            break

        events = response.json()
        if not events:
            break

        for event in events:
            if event["created_at"] < since_time:
                return new_stars, new_forks, list(contributors)

            if event["type"] == "WatchEvent":
                new_stars += 1
            elif event["type"] == "ForkEvent":
                new_forks += 1
            elif event["type"] in ["PullRequestEvent", "PushEvent"]:
                contributors.add(event["actor"]["display_login"])

    return new_stars, new_forks, list(contributors)


def print_report(repo, hours_text, stats):
    """Выводит итоговый отчет в консоль."""
    i_s = stats["i_stats"]
    e_s = stats["e_stats"]

    print(f"\nМониторинг активности в \"{repo}\" за последние {hours_text} часа(ов):")
    print(f"{stats['commits']} новых коммитов")
    print(f"{i_s[0]} новых pull requests ({i_s[1]} закрыто)")
    print(f"{i_s[2]} новых issues ({i_s[3]} закрыто)")

    if e_s[2]:
        contrib_str = ", ".join([f"@{c}" for c in e_s[2]])
        print(f"{len(e_s[2])} новых контрибьютора: {contrib_str}")
    else:
        print("0 новых контрибьюторов")

    print(f"{e_s[0]} новых звёзд, {e_s[1]} новых форка")

    mentions = stats["mentions"]
    if mentions:
        if len(mentions) > 10:
            m_str = ", ".join([f"@{m}" for m in mentions[:10]]) + "..."
        else:
            m_str = ", ".join([f"@{m}" for m in mentions])
        print(f"{len(mentions)} упоминания пользователей: {m_str}")
    else:
        print("0 упоминаний пользователей")


def main():
    """Основная логика: ввод данных и вызов API."""
    repo = input("Введите репозиторий для мониторинга (owner/repo): ").strip()
    hours_input = input("Введите временной диапазон (в часах): ").strip()

    try:
        hours = float(hours_input)
    except ValueError:
        print("Ошибка: Время должно быть числом.")
        return

    since_time = get_time_threshold(hours)

    all_stats = {
        "commits": get_commits(repo, since_time),
        "i_stats": get_issues_and_prs(repo, since_time),
        "e_stats": get_events_stats(repo, since_time),
        "mentions": get_mentions(repo, since_time)
    }

    print_report(repo, hours_input, all_stats)


if __name__ == "__main__":
    main()
