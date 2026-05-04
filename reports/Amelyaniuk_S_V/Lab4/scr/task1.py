import requests
import networkx as nx
import matplotlib.pyplot as plt
import json

# Твои данные
USERNAME = "Mao2280"
# Если будет ошибка "Rate Limit", создай токен здесь https://github.com/settings/tokens
# и вставь его ниже. Для тестов можно оставить пустым.
TOKEN = ""

HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}


def get_github_data(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        print("Ошибка: Превышен лимит запросов API. Используйте GitHub Token.")
        return None
    return []


def build_map():
    G = nx.Graph()
    G.add_node(USERNAME, type="user", color="orange")

    print(f"--- Анализ профиля {USERNAME} ---")

    # 1. Получаем твои репозитории
    repos = get_github_data(f"https://api.github.com/users/{USERNAME}/repos")
    # 2. Получаем репозитории, которые ты отметил звездой (Starred)
    starred = get_github_data(f"https://api.github.com/users/{USERNAME}/starred")

    all_projects = []
    if repos:
        all_projects.extend(repos)
    if starred:
        all_projects.extend(starred)

    if not all_projects:
        print("Репозитории не найдены. Возможно, профиль пуст или API заблокирован.")
        return

    # Ограничим до 10 проектов для наглядности графа
    for repo in all_projects[:10]:
        repo_name = repo["full_name"]
        owner = repo["owner"]["login"]

        print(f"Обработка проекта: {repo_name}")

        # Добавляем связь с владельцем репозитория
        if owner != USERNAME:
            G.add_edge(USERNAME, owner, weight=1, label="contributor/fan")

        # 3. Ищем других контрибьюторов в этих репозиториях
        contributors = get_github_data(
            f"https://api.github.com/repos/{repo_name}/contributors"
        )
        if contributors:
            for c in contributors[:5]:  # Берем топ-5 человек из каждого репо
                other_user = c["login"]
                if other_user != USERNAME:
                    G.add_edge(USERNAME, other_user, weight=1)

    # Сохранение в JSON
    with open("github_network.json", "w", encoding="utf-8") as f:
        json.dump(nx.node_link_data(G), f, indent=4, ensure_ascii=False)

    print(f"\nНайдено {len(G.nodes)} узлов (разработчиков).")

    # Визуализация
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5)

    # Рисуем тебя
    nx.draw_networkx_nodes(
        G, pos, nodelist=[USERNAME], node_color="orange", node_size=1000
    )
    # Рисуем остальных
    others = [n for n in G.nodes if n != USERNAME]
    nx.draw_networkx_nodes(G, pos, nodelist=others, node_color="skyblue", node_size=500)

    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    plt.title(f"Карта связей разработчика: {USERNAME}")
    plt.axis("off")

    # Сохранение фото
    plt.savefig("github_network.png")
    print("Результаты сохранены в github_network.json и github_network.png")
    plt.show()


if __name__ == "__main__":
    build_map()
