import requests
import json
import os


def get_latest_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github+json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print(
                f" (!) Превышен лимит запросов GitHub (Rate Limit). Попробуйте позже."
            )
            return None
        elif response.status_code == 404:
            return get_latest_tag(repo)
        else:
            print(f" (!) Ошибка API: {response.status_code}")
            return None
    except Exception as e:
        print(f" (!) Ошибка сети: {e}")
        return None


def get_latest_tag(repo):
    url = f"https://api.github.com/repos/{repo}/tags?per_page=1"
    headers = {"Accept": "application/vnd.github+json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            tags = response.json()
            if tags:
                return {
                    "tag_name": tags[0]["name"],
                    "published_at": "",
                    "html_url": f"https://github.com/{repo}/releases/tag/{tags[0]['name']}",
                    "body": "Информация о версии из тега (релизов нет)",
                }
        return None
    except Exception as e:
        print(f" (!) Ошибка при получении тегов: {e}")
        return None


def main():
    user_input = input("Введите репозитории для отслеживания (через запятую): ")
    repos = [r.strip() for r in user_input.split(",") if r.strip()]

    db_file = "last_versions.json"
    last_versions = {}
    if os.path.exists(db_file):
        with open(db_file, "r") as f:
            try:
                last_versions = json.load(f)
            except:
                pass

    for repo in repos:
        print(f"Проверяем {repo}...")
        release = get_latest_release(repo)

        if release:
            tag = release.get("tag_name")
            date = release.get("published_at", "")[:10]
            link = release.get("html_url")
            body = (release.get("body") or "Нет описания").replace("\n", " ")

            if last_versions.get(repo) != tag:
                print(f"✅ Найден новый релиз: {tag} ({date})")
                print(f"🔗 {link}")
                print(f"📝 Изменения: {body[:150]}...\n")
                last_versions[repo] = tag
            else:
                print(f"ℹ️ Обновлений для {repo} нет (текущая: {tag}).\n")
        else:
            print(f"❌ Не удалось получить данные для {repo}.\n")

    with open(db_file, "w") as f:
        json.dump(last_versions, f, indent=4)


if __name__ == "__main__":
    main()
