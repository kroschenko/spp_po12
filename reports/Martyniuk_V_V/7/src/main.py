"""
Главный модуль приложения для анимации шара.
"""

import sys
import os
from datetime import datetime

import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, BALL_COLOR, BALL_START_RADIUS, BACKGROUND_COLOR, FPS
from ball import Ball
from controls import ControlPanel


class BallAnimationApp:
    """Главный класс приложения."""

    def __init__(self):
        """Инициализация приложения."""
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # Создаём папку для скриншотов
        self.screenshot_dir = "screenshots"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

        # Создаём шар
        ball_x = WINDOW_WIDTH // 2
        ball_y = (WINDOW_HEIGHT - 80) // 2
        self.ball = Ball(ball_x, ball_y, BALL_START_RADIUS, BALL_COLOR, 50)

        # Создаём панель управления
        self.control_panel = ControlPanel(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Переменные состояния
        self.running = True
        self.last_time = pygame.time.get_ticks()

    def take_screenshot(self) -> None:
        """Сохранение скриншота."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        pygame.image.save(self.screen, filepath)
        print(f"Скриншот сохранён: {filepath}")

        # Визуальный反馈 (мигание экрана)
        flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        flash_surface.set_alpha(128)
        flash_surface.fill((255, 255, 255))
        self.screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)

    def handle_events(self) -> None:
        """Обработка событий."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ball.toggle_pause()
                elif event.key == pygame.K_r:
                    self.ball.reset()
                elif event.key == pygame.K_F12:
                    self.take_screenshot()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            # Обработка событий панели управления
            action = self.control_panel.handle_event(event)
            if action == "pause":
                self.ball.toggle_pause()
            elif action == "reset":
                self.ball.reset()
            elif action == "screenshot":
                self.take_screenshot()

    def update(self, delta_time: float) -> None:
        """Обновление состояния приложения."""
        # Обновляем скорость шара из панели управления
        self.ball.speed = self.control_panel.get_speed()

        # Обновляем шар
        self.ball.update(delta_time)

    def draw(self) -> None:
        """Отрисовка всех элементов."""
        # Очищаем экран
        self.screen.fill(BACKGROUND_COLOR)

        # Рисуем шар
        self.ball.draw(self.screen)

        # Рисуем панель управления
        ball_info = self.ball.get_info()
        self.control_panel.draw(self.screen, ball_info)

        # Добавляем заголовок
        font = pygame.font.Font(None, 36)
        title = font.render("Приближающийся и удаляющийся шар", True, (0, 0, 0))
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 10))

        # Обновляем экран
        pygame.display.flip()

    def run(self) -> None:
        """Главный цикл приложения."""
        print("""
        ========================================
        Управление:
        Space - Пауза/Продолжить
        R - Сброс
        F12 - Скриншот
        ESC - Выход
        ========================================
        """)

        while self.running:
            # Вычисляем delta time
            current_time = pygame.time.get_ticks()
            delta_time = min((current_time - self.last_time) / 1000.0, 0.1)
            self.last_time = current_time

            self.handle_events()
            self.update(delta_time)
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Точка входа в программу."""
    app = BallAnimationApp()
    app.run()


if __name__ == "__main__":
    main()
