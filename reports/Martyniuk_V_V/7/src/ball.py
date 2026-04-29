"""
Модуль класса Ball для анимации шара.
"""

import pygame


class Ball:
    """Класс шара, который может приближаться и удаляться."""

    def __init__(self, x: int, y: int, radius: int, color: tuple, speed: float):
        """
        Инициализация шара.

        Args:
            x: координата X центра
            y: координата Y центра
            radius: начальный радиус
            color: цвет шара (R, G, B)
            speed: скорость изменения радиуса (пикселей в секунду)
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.direction = 1
        self.min_radius = 10
        self.max_radius = 150
        self.is_running = True
        self.paused = False

    def update(self, delta_time: float) -> None:
        """Обновление состояния шара."""
        if self.paused or not self.is_running:
            return

        radius_change = self.speed * delta_time * self.direction
        self.radius += radius_change

        if self.radius >= self.max_radius:
            self.radius = self.max_radius
            self.direction = -1
        elif self.radius <= self.min_radius:
            self.radius = self.min_radius
            self.direction = 1

    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка шара на экране."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), int(self.radius))

        highlight_radius = max(3, int(self.radius * 0.3))
        highlight_x = self.x - int(self.radius * 0.3)
        highlight_y = self.y - int(self.radius * 0.3)
        pygame.draw.circle(screen, (255, 255, 255), (highlight_x, highlight_y), highlight_radius)

    def set_speed(self, speed: float) -> None:
        """Установка скорости движения."""
        self.speed = max(10, min(200, speed))

    def toggle_pause(self) -> None:
        """Пауза/продолжение анимации."""
        self.paused = not self.paused

    def reset(self) -> None:
        """Сброс шара в начальное состояние."""
        self.radius = 30
        self.direction = 1
        self.paused = False

    def get_info(self) -> dict:
        """Получение информации о состоянии шара."""
        return {
            "radius": int(self.radius),
            "direction": "Приближается" if self.direction == 1 else "Удаляется",
            "speed": self.speed,
            "paused": self.paused,
        }


class BallWithTrail(Ball):
    """Шар с эффектом следа."""

    def __init__(self, x: int, y: int, radius: int, color: tuple, speed: float):
        """Инициализация шара со следом."""
        super().__init__(x, y, radius, color, speed)
        self.trail = []
        self.trail_length = 10

    def update(self, delta_time: float) -> None:
        """Обновление с сохранением следа."""
        self.trail.append(self.radius)
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        super().update(delta_time)

    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка шара со следом."""
        for i, trail_radius in enumerate(self.trail):
            alpha = 255 * (i + 1) // (self.trail_length + 1)
            trail_color = (*self.color, alpha)
            trail_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (self.x, self.y), int(trail_radius))
            screen.blit(trail_surface, (0, 0))
        super().draw(screen)
        