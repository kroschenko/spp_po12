"""Модуль для анализа и визуализации связей GitHub разработчика."""
import json

import matplotlib.pyplot as plt
import networkx as nx
import requests

# Твои данные
USERNAME = "Mao2280"
# Если будет ошибка "Rate Limit", создай токен здесь https://github.com/settings/tokens
# и вставь его ниже. Для тестов можно оставить пустым.
TOKEN = ""

HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}


def get_github_data(url):
    """Получает данные с GitHub API по заданному URL."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    if response.status_code == 200:
        return response.json()
    if response.status_code == 403:
        print("Ошибка: Превышен лимит запросов API. Используйте GitHub Token.")
        return None
    return []


def build_map():
    """Строит и визуализирует карту связей разработчика на GitHub."""
    graph = nx.Graph()
    graph.add_node(USERNAME, type="user", color="orange")

    print(f"--- Анализ профиля {USERNAME} ---")

    repos = get_github_data(f"https://api.github.com/users/{USERNAME}/repos")
    starred = get_github_data(f"https://api.github.com/users/{USERNAME}/starred")

    all_projects = []
    if repos:
        all_projects.extend(repos)
    if starred:
        all_projects.extend(starred)

    if not all_projects:
        print("Репозитории не найдены. Возможно, профиль пуст или API заблокирован.")
        return

    for repo in all_projects[:10]:
        repo_name = repo["full_name"]
        owner = repo["owner"]["login"]

        print(f"Обработка проекта: {repo_name}")

        if owner != USERNAME:
            graph.add_edge(USERNAME, owner, weight=1, label="contributor/fan")

        contributors = get_github_data(
            f"https://api.github.com/repos/{repo_name}/contributors"
        )
        if contributors:
            for contributor in contributors[:5]:
                other_user = contributor["login"]
                if other_user != USERNAME:
                    graph.add_edge(USERNAME, other_user, weight=1)

    with open("github_network.json", "w", encoding="utf-8") as file:
        json.dump(nx.node_link_data(graph), file, indent=4, ensure_ascii=False)

    print(f"\nНайдено {len(graph.nodes)} узлов (разработчиков).")

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, k=0.5)

    nx.draw_networkx_nodes(
        graph, pos, nodelist=[USERNAME], node_color="orange", node_size=1000
    )
    others = [n for n in graph.nodes if n != USERNAME]
    nx.draw_networkx_nodes(graph, pos, nodelist=others, node_color="skyblue", node_size=500)

    nx.draw_networkx_edges(graph, pos, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif")

    plt.title(f"Карта связей разработчика: {USERNAME}")
    plt.axis("off")

    plt.savefig("github_network.png")
    print("Результаты сохранены в github_network.json и github_network.png")
    plt.show()


if __name__ == "__main__":
    build_map()
