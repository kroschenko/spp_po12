"""
Скрипт для построения графа взаимодействий разработчика на GitHub.
"""

import json
from typing import Dict, List, Set

import requests
import networkx as nx
import matplotlib.pyplot as plt

GITHUB_API_URL = "https://api.github.com"


def get_headers() -> Dict[str, str]:
    """Возвращает HTTP-заголовки для запросов к GitHub API."""
    return {"Accept": "application/vnd.github.v3+json"}


def fetch_starred_owners(username: str) -> List[str]:
    """Возвращает список владельцев репозиториев, отмеченных пользователем."""
    url = f"{GITHUB_API_URL}/users/{username}/starred"
    response = requests.get(url, headers=get_headers(), params={"per_page": 30}, timeout=10)
    response.raise_for_status()
    return [repo["owner"]["login"] for repo in response.json()]


def fetch_event_interactions(username: str) -> List[str]:
    """Возвращает список пользователей из недавних событий."""
    url = f"{GITHUB_API_URL}/users/{username}/events"
    response = requests.get(url, headers=get_headers(), params={"per_page": 50}, timeout=10)
    response.raise_for_status()

    interacted = []
    for event in response.json():
        repo_data = event.get("repo")
        if not repo_data:
            continue
        repo_name = repo_data.get("name", "")
        if "/" in repo_name:
            owner = repo_name.split("/")[0]
            if owner != username:
                interacted.append(owner)
    return interacted


def fetch_repo_contributors(username: str) -> List[str]:
    """Возвращает список контрибьюторов репозиториев пользователя."""
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    response = requests.get(url, headers=get_headers(), params={"per_page": 5}, timeout=10)
    response.raise_for_status()

    contributors = []
    for repo in response.json():
        contrib_url = repo.get("contributors_url")
        if not contrib_url:
            continue
        try:
            contrib_resp = requests.get(contrib_url, headers=get_headers(), timeout=10)
            if contrib_resp.status_code == 200:
                for user in contrib_resp.json():
                    if user["login"] != username:
                        contributors.append(user["login"])
        except requests.exceptions.RequestException:
            continue
    return contributors


def main() -> None:
    """Основная логика сбора данных и построения графа."""
    username = input("Введите имя пользователя GitHub: ").strip()
    if not username:
        print("Имя пользователя не может быть пустым.")
        return

    print(f"Анализируем взаимодействия пользователя {username}...")
    interactions: Set[str] = set()

    try:
        interactions.update(fetch_starred_owners(username))
        interactions.update(fetch_event_interactions(username))
        interactions.update(fetch_repo_contributors(username))
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при обращении к API: {error}")
        return

    interactions.discard(username)
    print(f"Найдено {len(interactions)} связанных разработчика(ов).")

    graph = nx.Graph()
    graph.add_node(username, color="red", size=800)

    json_data = {"nodes": [{"id": username}], "links": []}

    for user in interactions:
        graph.add_node(user, color="skyblue", size=300)
        graph.add_edge(username, user)
        json_data["nodes"].append({"id": user})
        json_data["links"].append({"source": username, "target": user})

    with open("github_network.json", "w", encoding="utf-8") as file_out:
        json.dump(json_data, file_out, indent=4)
    print("Граф сохранён в github_network.json")

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)

    colors = [graph.nodes[n].get("color", "skyblue") for n in graph.nodes]
    sizes = [graph.nodes[n].get("size", 300) for n in graph.nodes]

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=sizes,
        font_size=9,
        font_weight="bold",
        edge_color="gray",
    )

    plt.title(f"Карта взаимодействий на GitHub: {username}")
    plt.savefig("github_network.png", format="png", dpi=300)
    print("Визуализация графа сохранена в github_network.png")


if __name__ == "__main__":
    main()
