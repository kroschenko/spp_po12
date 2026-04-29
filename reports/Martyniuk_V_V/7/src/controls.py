"""
Модуль панели управления.
Содержит классы Button, Slider и ControlPanel.
"""

import pygame
from config import PANEL_HEIGHT, MIN_SPEED, MAX_SPEED, TEXT_COLOR, PANEL_COLOR


class Button:
    """Класс кнопки."""

    def __init__(self, rect: pygame.Rect, text: str, color: tuple, hover_color: tuple):
        """
        Инициализация кнопки.

        Args:
            rect: прямоугольник кнопки
            text: текст на кнопке
            color: цвет кнопки
            hover_color: цвет при наведении
        """
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка кнопки."""
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Обработка событий кнопки.

        Returns:
            bool: True если кнопка нажата
        """
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Slider:
    """Класс ползунка для регулировки скорости."""

    def __init__(self, rect: pygame.Rect, min_val: float, max_val: float, initial_val: float):
        """
        Инициализация ползунка.

        Args:
            rect: прямоугольник ползунка
            min_val: минимальное значение
            max_val: максимальное значение
            initial_val: начальное значение
        """
        self.rect = rect
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.knob_radius = 8
        self.dragging = False
        self.font = pygame.font.Font(None, 20)

    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка ползунка."""
        # Рисуем линию
        pygame.draw.line(
            screen,
            (100, 100, 100),
            (self.rect.x, self.rect.centery),
            (self.rect.x + self.rect.width, self.rect.centery),
            3,
        )

        # Вычисляем позицию ползунка
        knob_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width

        # Рисуем ползунок
        pygame.draw.circle(screen, (100, 100, 200), (int(knob_x), self.rect.centery), self.knob_radius)
        pygame.draw.circle(screen, (0, 0, 0), (int(knob_x), self.rect.centery), self.knob_radius, 2)

        # Отображаем значение
        value_text = self.font.render(f"Скорость: {int(self.value)}", True, (0, 0, 0))
        screen.blit(value_text, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Обработка событий ползунка."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            knob_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            if (
                abs(event.pos[0] - knob_x) <= self.knob_radius
                and abs(event.pos[1] - self.rect.centery) <= self.knob_radius
            ):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x = max(0, min(self.rect.width, event.pos[0] - self.rect.x))
            self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)

    def get_value(self) -> float:
        """Получение текущего значения."""
        return self.value


class ControlPanel:
    """Панель управления анимацией."""

    def __init__(self, screen_width: int, screen_height: int):
        """Инициализация панели управления."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.panel_rect = pygame.Rect(0, screen_height - PANEL_HEIGHT, screen_width, PANEL_HEIGHT)

        # Создаём кнопки
        button_width = 100
        button_height = 40
        button_y = screen_height - PANEL_HEIGHT + (PANEL_HEIGHT - button_height) // 2

        self.pause_button = Button(
            pygame.Rect(20, button_y, button_width, button_height),
            "Пауза",
            (150, 200, 150),
            (100, 150, 100)
        )

        self.reset_button = Button(
            pygame.Rect(140, button_y, button_width, button_height),
            "Сброс",
            (200, 150, 150),
            (150, 100, 100)
        )

        self.screenshot_button = Button(
            pygame.Rect(260, button_y, button_width, button_height),
            "Скриншот",
            (150, 150, 200),
            (100, 100, 150)
        )

        # Создаём ползунок скорости
        self.speed_slider = Slider(
            pygame.Rect(400, screen_height - PANEL_HEIGHT + 20, 200, 30),
            MIN_SPEED,
            MAX_SPEED,
            50
        )

        # Информационная панель
        self.info_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

    def draw(self, screen: pygame.Surface, ball_info: dict) -> None:
        """Отрисовка панели управления."""
        # Фон панели
        pygame.draw.rect(screen, PANEL_COLOR, self.panel_rect)
        pygame.draw.line(screen, (0, 0, 0), (0, self.panel_rect.y), (self.screen_width, self.panel_rect.y), 2)

        # Отрисовка элементов управления
        self.pause_button.draw(screen)
        self.reset_button.draw(screen)
        self.screenshot_button.draw(screen)
        self.speed_slider.draw(screen)

        # Отображение информации
        info_y = self.panel_rect.y + 5
        info_texts = [
            f"Радиус: {ball_info['radius']} px",
            f"Направление: {ball_info['direction']}",
            f"Статус: {'Пауза' if ball_info['paused'] else 'Активен'}",
        ]

        for i, text in enumerate(info_texts):
            text_surface = self.info_font.render(text, True, TEXT_COLOR)
            screen.blit(text_surface, (620, info_y + i * 25))

        # Отображение подсказок
        help_y = self.panel_rect.y + 5
        help_texts = ["Управление:", "Space - Пауза", "R - Сброс", "F12 - Скриншот"]

        for i, text in enumerate(help_texts):
            text_surface = self.small_font.render(text, True, TEXT_COLOR)
            screen.blit(text_surface, (self.screen_width - 150, help_y + i * 18))

    def handle_event(self, event: pygame.event.Event):
        """
        Обработка событий на панели управления.

        Returns:
            str: действие ('pause', 'reset', 'screenshot', None)
        """
        self.speed_slider.handle_event(event)

        if self.pause_button.handle_event(event):
            return "pause"
        if self.reset_button.handle_event(event):
            return "reset"
        if self.screenshot_button.handle_event(event):
            return "screenshot"

        return None

    def get_speed(self) -> float:
        """Получение текущей скорости."""
        return self.speed_slider.get_value()
