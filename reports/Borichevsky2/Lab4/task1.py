#!/usr/bin/env python3
"""
Анализ активности разработчиков в open-source проекте на GitHub.

Использует GitHub REST API для сбора статистики по контрибьюторам:
- Количество коммитов
- Pull requests (открытые/закрытые)
- Issues (открытые/закрытые)
- Дата последней активности
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import time

import requests
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# Настройка стилей для графиков
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10


@dataclass
class ContributorStats:
    """Класс для хранения статистики контрибьютора."""
    username: str
    commits: int = 0
    open_prs: int = 0
    closed_prs: int = 0
    open_issues: int = 0
    closed_issues: int = 0
    last_activity: Optional[datetime] = None

    @property
    def total_prs(self) -> int:
        """Общее количество PR."""
        return self.open_prs + self.closed_prs

    @property
    def total_issues(self) -> int:
        """Общее количество issues."""
        return self.open_issues + self.closed_issues

    @property
    def total_contributions(self) -> int:
        """Суммарный вклад."""
        return self.commits + self.total_prs + self.total_issues

    @property
    def activity_score(self) -> float:
        """
        Расчетный показатель активности.
        Коммиты весят больше, так как это прямые изменения кода.
        """
        return (
                self.commits * 2.0 +  # Коммиты важнее всего
                self.total_prs * 1.5 +  # PR тоже важны
                self.total_issues * 0.5  # Issues менее значимы
        )

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь."""
        data = asdict(self)
        data['total_prs'] = self.total_prs
        data['total_issues'] = self.total_issues
        data['total_contributions'] = self.total_contributions
        data['activity_score'] = round(self.activity_score, 2)
        data['last_activity'] = (
            self.last_activity.strftime('%Y-%m-%d %H:%M')
            if self.last_activity else 'N/A'
        )
        return data


class GitHubAnalyzer:
    """Класс для анализа GitHub репозитория."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        """
        Инициализация анализатора.

        Args:
            token: GitHub Personal Access Token (опционально, но рекомендуется)
        """
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Contributor-Analyzer"
        })

        if token:
            self.session.headers["Authorization"] = f"token {token}"

        self.rate_limit_remaining = None
        self.rate_limit_reset = None

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Выполнение запроса к GitHub API с обработкой rate limiting.

        Args:
            endpoint: API endpoint (без базового URL)
            params: Query parameters

        Returns:
            JSON ответ

        Raises:
            requests.exceptions.RequestException: при ошибках запроса
        """
        url = f"{self.BASE_URL}/{endpoint}"

        # Проверка rate limit
        if self.rate_limit_remaining == 0:
            reset_time = datetime.fromtimestamp(self.rate_limit_reset or 0)
            wait_seconds = (reset_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"⏳ Ожидание сброса rate limit ({int(wait_seconds)} сек)...")
                time.sleep(min(wait_seconds + 1, 60))  # Максимум 60 сек ожидания

        try:
            response = self.session.get(url, params=params or {}, timeout=30)

            # Обновление rate limit info
            self.rate_limit_remaining = int(
                response.headers.get('X-RateLimit-Remaining', 1)
            )
            self.rate_limit_reset = int(
                response.headers.get('X-RateLimit-Reset', 0)
            )

            if response.status_code == 403 and 'rate limit' in response.text.lower():
                print("⚠️ Достигнут rate limit. Используйте GitHub токен для увеличения лимита.")
                print("Создайте токен: https://github.com/settings/tokens")
                raise requests.exceptions.RequestException("Rate limit exceeded")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка запроса: {e}")
            raise

    def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        """
        Получение списка контрибьюторов через API contributors.

        GitHub API возвращает только топ-100 контрибьюторов по коммитам.
        """
        print(f"📊 Получение списка контрибьюторов...")

        contributors = []
        page = 1

        while True:
            try:
                data = self._make_request(
                    f"repos/{owner}/{repo}/contributors",
                    params={"page": page, "per_page": 100}
                )

                if not data:
                    break

                contributors.extend(data)

                # GitHub возвращает максимум 100 контрибьюторов через этот endpoint
                if len(data) < 100:
                    break

                page += 1

                # Защита от бесконечного цикла
                if page > 5:
                    print("⚠️ Достигнут лимит страниц контрибьюторов")
                    break

            except requests.exceptions.RequestException:
                break

        print(f"✅ Найдено {len(contributors)} контрибьюторов")
        return contributors

    def get_user_commits_count(self, owner: str, repo: str,
                               username: str) -> int:
        """
        Получение точного количества коммитов пользователя.
        """
        try:
            # Используем search API для подсчета коммитов
            data = self._make_request(
                "search/commits",
                params={
                    "q": f"repo:{owner}/{repo} author:{username}",
                    "per_page": 1
                }
            )
            return data.get("total_count", 0)
        except:
            # Fallback: используем данные из списка контрибьюторов
            return 0

    def get_pull_requests(self, owner: str, repo: str,
                          username: str, state: str) -> int:
        """
        Получение количества PR пользователя с определенным статусом.

        Args:
            state: 'open', 'closed', или 'all'
        """
        try:
            data = self._make_request(
                f"repos/{owner}/{repo}/pulls",
                params={
                    "state": state,
                    "creator": username,
                    "per_page": 100
                }
            )
            # Если вернулось 100, возможно есть еще
            if len(data) == 100:
                # Пробуем получить точное количество через search
                search_data = self._make_request(
                    "search/issues",
                    params={
                        "q": f"repo:{owner}/{repo} type:pr author:{username} state:{state}",
                        "per_page": 1
                    }
                )
                return search_data.get("total_count", len(data))
            return len(data)
        except:
            return 0

    def get_issues(self, owner: str, repo: str,
                   username: str, state: str) -> int:
        """
        Получение количества issues пользователя с определенным статусом.

        Args:
            state: 'open', 'closed', или 'all'
        """
        try:
            # Issues созданные пользователем (не PR)
            search_data = self._make_request(
                "search/issues",
                params={
                    "q": f"repo:{owner}/{repo} type:issue author:{username} state:{state}",
                    "per_page": 1
                }
            )
            return search_data.get("total_count", 0)
        except:
            return 0

    def get_user_events(self, username: str) -> List[Dict]:
        """
        Получение публичных событий пользователя для определения активности.
        """
        try:
            return self._make_request(
                f"users/{username}/events/public",
                params={"per_page": 30}
            )
        except:
            return []

    def analyze_repository(self, owner: str, repo: str,
                           top_n: int = 10) -> List[ContributorStats]:
        """
        Полный анализ репозитория.

        Args:
            owner: Владелец репозитория
            repo: Название репозитория
            top_n: Количество топ-контрибьюторов для детального анализа

        Returns:
            Список статистики контрибьюторов
        """
        print(f"\n{'=' * 60}")
        print(f"🔍 Анализ репозитория: {owner}/{repo}")
        print(f"{'=' * 60}\n")

        # Получаем базовый список контрибьюторов
        contributors = self.get_contributors(owner, repo)

        if not contributors:
            print("❌ Не удалось получить список контрибьюторов")
            return []

        # Ограничиваем для детального анализа (API лимиты)
        contributors_to_analyze = contributors[:min(top_n, len(contributors))]

        stats_list = []

        for i, contrib in enumerate(contributors_to_analyze, 1):
            username = contrib["login"]
            print(f"\n[{i}/{len(contributors_to_analyze)}] Анализ {username}...")

            stats = ContributorStats(username=username)

            # Коммиты (из базовых данных contributors API)
            stats.commits = contrib.get("contributions", 0)

            # Pull Requests
            print(f"  📥 Получение PR...")
            stats.open_prs = self.get_pull_requests(owner, repo, username, "open")
            stats.closed_prs = self.get_pull_requests(owner, repo, username, "closed")

            # Issues
            print(f"  🐛 Получение issues...")
            stats.open_issues = self.get_issues(owner, repo, username, "open")
            stats.closed_issues = self.get_issues(owner, repo, username, "closed")

            # Последняя активность
            print(f"  🕐 Получение активности...")
            events = self.get_user_events(username)
            if events:
                # События отсортированы по времени (новые первые)
                last_event_time = events[0].get("created_at")
                if last_event_time:
                    stats.last_activity = datetime.fromisoformat(
                        last_event_time.replace("Z", "+00:00")
                    ).replace(tzinfo=None)

            stats_list.append(stats)

            # Небольшая задержка чтобы не перегружать API
            if i < len(contributors_to_analyze):
                time.sleep(0.5)

        # Сортировка по активности (score)
        stats_list.sort(key=lambda x: x.activity_score, reverse=True)

        return stats_list


class Visualizer:
    """Класс для визуализации результатов анализа."""

    @staticmethod
    def create_contribution_chart(stats: List[ContributorStats],
                                  repo_name: str,
                                  output_file: Optional[str] = None) -> str:
        """
        Создание комплексного графика вклада разработчиков.

        Returns:
            Путь к сохраненному файлу
        """
        if not stats:
            print("❌ Нет данных для визуализации")
            return ""

        # Ограничиваем до топ-10 для читаемости
        top_stats = stats[:10]

        # Создаем фигуру с подграфиками
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(f'Анализ активности разработчиков\n{repo_name}',
                     fontsize=16, fontweight='bold', y=0.98)

        # 1. Общий вклад (stacked bar)
        ax1 = plt.subplot(2, 2, 1)
        usernames = [s.username[:15] for s in top_stats]  # Обрезаем длинные имена

        commits = [s.commits for s in top_stats]
        prs = [s.total_prs for s in top_stats]
        issues = [s.total_issues for s in top_stats]

        x = range(len(usernames))
        width = 0.6

        p1 = ax1.bar(x, commits, width, label='Коммиты', color='#2ecc71', alpha=0.8)
        p2 = ax1.bar(x, prs, width, bottom=commits, label='PR', color='#3498db', alpha=0.8)
        p3 = ax1.bar(x, issues, width,
                     bottom=[c + p for c, p in zip(commits, prs)],
                     label='Issues', color='#e74c3c', alpha=0.8)

        ax1.set_ylabel('Количество')
        ax1.set_title('Распределение вклада по типам')
        ax1.set_xticks(x)
        ax1.set_xticklabels(usernames, rotation=45, ha='right')
        ax1.legend(loc='upper right')
        ax1.grid(axis='y', alpha=0.3)

        # Добавляем значения на столбцы
        for i, (c, p, iss) in enumerate(zip(commits, prs, issues)):
            total = c + p + iss
            ax1.text(i, total + max(commits) * 0.02, str(total),
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

        # 2. Activity Score (horizontal bar)
        ax2 = plt.subplot(2, 2, 2)
        scores = [s.activity_score for s in top_stats]
        colors = plt.cm.viridis([s / max(scores) for s in scores])

        bars = ax2.barh(range(len(usernames)), scores, color=colors, alpha=0.8)
        ax2.set_yticks(range(len(usernames)))
        ax2.set_yticklabels(usernames)
        ax2.invert_yaxis()
        ax2.set_xlabel('Activity Score')
        ax2.set_title('Рейтинг активности (взвешенный)')
        ax2.grid(axis='x', alpha=0.3)

        # Добавляем значения
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax2.text(score + max(scores) * 0.01, i, f'{score:.0f}',
                     va='center', fontsize=9)

        # 3. PR статистика (grouped bar)
        ax3 = plt.subplot(2, 2, 3)
        open_prs = [s.open_prs for s in top_stats]
        closed_prs = [s.closed_prs for s in top_stats]

        x = range(len(usernames))
        width = 0.35

        ax3.bar([i - width / 2 for i in x], open_prs, width,
                label='Открытые', color='#f39c12', alpha=0.8)
        ax3.bar([i + width / 2 for i in x], closed_prs, width,
                label='Закрытые', color='#27ae60', alpha=0.8)

        ax3.set_ylabel('Количество PR')
        ax3.set_title('Pull Requests (открытые vs закрытые)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(usernames, rotation=45, ha='right')
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)

        # 4. Issues статистика (grouped bar)
        ax4 = plt.subplot(2, 2, 4)
        open_issues = [s.open_issues for s in top_stats]
        closed_issues = [s.closed_issues for s in top_stats]

        ax4.bar([i - width / 2 for i in x], open_issues, width,
                label='Открытые', color='#e74c3c', alpha=0.8)
        ax4.bar([i + width / 2 for i in x], closed_issues, width,
                label='Закрытые', color='#9b59b6', alpha=0.8)

        ax4.set_ylabel('Количество Issues')
        ax4.set_title('Issues (открытые vs закрытые)')
        ax4.set_xticks(x)
        ax4.set_xticklabels(usernames, rotation=45, ha='right')
        ax4.legend()
        ax4.grid(axis='y', alpha=0.3)

        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Сохранение
        if not output_file:
            safe_repo_name = repo_name.replace("/", "_")
            output_file = f"{safe_repo_name}_contributors.png"

        plt.savefig(output_file, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f"\n📊 График сохранен: {output_file}")
        plt.close()

        return output_file

    @staticmethod
    def print_report(stats: List[ContributorStats], repo_name: str,
                     top_n: int = 5) -> None:
        """
        Вывод текстового отчета в консоль.
        """
        print(f"\n{'=' * 60}")
        print(f"📋 ОТЧЕТ: ТОП-{top_n} самых активных разработчиков")
        print(f"Репозиторий: {repo_name}")
        print(f"{'=' * 60}\n")

        for i, s in enumerate(stats[:top_n], 1):
            print(f"{i}. 🏆 {s.username}")
            print(f"   📊 Коммитов: {s.commits} | "
                  f"PR: {s.open_prs} открыто, {s.closed_prs} закрыто | "
                  f"Issues: {s.open_issues} открыто, {s.closed_issues} закрыто")
            print(f"   📈 Activity Score: {s.activity_score:.1f}")
            print(f"   🕐 Последняя активность: "
                  f"{s.last_activity.strftime('%Y-%m-%d') if s.last_activity else 'N/A'}")
            print()

        if len(stats) > top_n:
            print(f"... и еще {len(stats) - top_n} контрибьюторов\n")


def main():
    """Основная функция."""
    print("🔧 GitHub Repository Contributor Analyzer")
    print("=" * 50)

    # Проверка зависимостей
    try:
        import requests
        import matplotlib
        import seaborn
    except ImportError as e:
        print(f"❌ Отсутствует библиотека: {e}")
        print("Установите зависимости: pip install requests matplotlib seaborn")
        sys.exit(1)

    # Ввод репозитория
    repo_input = input("\nВведите репозиторий для анализа (owner/repo): ").strip()

    if not repo_input or "/" not in repo_input:
        print("❌ Неверный формат. Используйте формат: owner/repo")
        print("Примеры: fastapi/fastapi, microsoft/vscode, python/cpython")
        sys.exit(1)

    owner, repo = repo_input.split("/", 1)

    # Проверка токена
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("\n⚠️  Внимание: GITHUB_TOKEN не установлен.")
        print("Рекомендуется создать токен для увеличения лимитов API.")
        print("https://github.com/settings/tokens")
        print("Без токена доступно 60 запросов в час.")
        print("\nПродолжить без токена? (y/n): ", end="")
        if input().lower() != 'y':
            sys.exit(0)

    # Анализ
    try:
        analyzer = GitHubAnalyzer(token)
        stats = analyzer.analyze_repository(owner, repo, top_n=10)

        if not stats:
            print("❌ Не удалось получить данные")
            sys.exit(1)

        # Вывод отчета
        visualizer = Visualizer()
        visualizer.print_report(stats, repo_input, top_n=5)

        # Создание графика
        output_file = visualizer.create_contribution_chart(stats, repo_input)

        print(f"\n{'=' * 60}")
        print("✅ Анализ завершен успешно!")
        print(f"{'=' * 60}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Анализ прерван пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
