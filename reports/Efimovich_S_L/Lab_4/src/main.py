import time
import json
import requests
import networkx as nx
import matplotlib.pyplot as plt

GITHUB_TOKEN = ""

headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"


def get_repos(github_username):
    url = f"https://api.github.com/users/{github_username}/repos"
    repos = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        data = response.json()

        if not data:
            break

        repos.extend(data)
        page += 1

    return repos


def get_contributors(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/contributors"
    response = requests.get(url, headers=headers)
    return response.json()


def get_issues(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/issues"
    response = requests.get(url, headers=headers)
    return response.json()


def get_pulls(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/pulls"
    response = requests.get(url, headers=headers)
    return response.json()


def analyze_user(github_username):
    print(f"Анализируем взаимодействия пользователя {github_username}...")

    repos = get_repos(github_username)

    G = nx.Graph()
    G.add_node(github_username)

    interactions = set()

    for repo in repos:
        repo_name = repo["full_name"]

        print(f"Обрабатываем репозиторий: {repo_name}")

        contributors = get_contributors(repo_name)
        for user in contributors:
            if user["login"] != github_username:
                interactions.add(user["login"])
                G.add_edge(github_username, user["login"], type="commit")

        issues = get_issues(repo_name)
        for issue in issues:
            if "user" in issue and issue["user"]:
                login = issue["user"]["login"]
                if login != github_username:
                    interactions.add(login)
                    G.add_edge(github_username, login, type="issue")

        pulls = get_pulls(repo_name)
        for pr in pulls:
            if "user" in pr and pr["user"]:
                login = pr["user"]["login"]
                if login != github_username:
                    interactions.add(login)
                    G.add_edge(github_username, login, type="pr")

        time.sleep(0.5)

    print(f"Найдено {len(interactions)} связанных разработчиков.")

    return G


def save_graph(G):
    data = nx.readwrite.json_graph.node_link_data(G)
    with open("github_network.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print("Граф сохранён в github_network.json")

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=800, font_size=14)

    plt.title("GitHub Interaction Network")
    plt.savefig("github_network.png")
    plt.close()

    print("Визуализация сохранена в github_network.png")


if __name__ == "__main__":
    username = input("Введите имя пользователя GitHub: ")
    graph = analyze_user(username)
    save_graph(graph)
