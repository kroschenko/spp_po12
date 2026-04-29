"""
Модуль для построения кривой Пеано (фрактал).
"""

import pygame
import math
from typing import List, Tuple


class PeanoCurve:
    """
    Класс для построения кривой Пеано.

    Кривая Пеано - это пространственно-заполняющая кривая,
    которая проходит через каждую точку квадрата.
    """

    def __init__(self, x: int, y: int, size: int, order: int):
        """
        Инициализация кривой Пеано.

        Args:
            x: координата X верхнего левого угла
            y: координата Y верхнего левого угла
            size: размер области для рисования
            order: порядок кривой (глубина рекурсии)
        """
        self.x = x
        self.y = y
        self.size = size
        self.order = order
        self.points = []
        self.generate()

    def generate(self) -> None:
        """Генерация точек кривой Пеано."""
        self.points = []
        self._peano(self.x, self.y, self.size, self.order, 0)

    def _peano(self, x: float, y: float, size: float, order: int, orientation: int) -> None:
        """
        Рекурсивная генерация кривой Пеано.

        Args:
            x, y: координаты текущего блока
            size: размер текущего блока
            order: оставшийся порядок
            orientation: ориентация (0 - горизонтальная, 1 - вертикальная)
        """
        if order == 0:
            self.points.append((x, y))
            return

        new_size = size / 3

        if orientation == 0:  # Горизонтальная ориентация
            # Рисуем 9 подблоков в порядке Пеано
            self._peano(x, y, new_size, order - 1, 1)
            self._peano(x + new_size, y, new_size, order - 1, 1)
            self._peano(x + 2 * new_size, y, new_size, order - 1, 0)
            self._peano(x + 2 * new_size, y + new_size, new_size, order - 1, 0)
            self._peano(x + new_size, y + new_size, new_size, order - 1, 1)
            self._peano(x, y + new_size, new_size, order - 1, 1)
            self._peano(x, y + 2 * new_size, new_size, order - 1, 0)
            self._peano(x + new_size, y + 2 * new_size, new_size, order - 1, 0)
            self._peano(x + 2 * new_size, y + 2 * new_size, new_size, order - 1, 1)
        else:  # Вертикальная ориентация
            self._peano(x, y, new_size, order - 1, 0)
            self._peano(x, y + new_size, new_size, order - 1, 0)
            self._peano(x, y + 2 * new_size, new_size, order - 1, 1)
            self._peano(x + new_size, y + 2 * new_size, new_size, order - 1, 1)
            self._peano(x + new_size, y + new_size, new_size, order - 1, 0)
            self._peano(x + new_size, y, new_size, order - 1, 0)
            self._peano(x + 2 * new_size, y, new_size, order - 1, 1)
            self._peano(x + 2 * new_size, y + new_size, new_size, order - 1, 1)
            self._peano(x + 2 * new_size, y + 2 * new_size, new_size, order - 1, 0)

    def draw(self, screen: pygame.Surface, color: tuple, line_width: int = 2) -> None:
        """
        Отрисовка кривой Пеано.

        Args:
            screen: поверхность pygame для рисования
            color: цвет линии
            line_width: толщина линии
        """
        if len(self.points) < 2:
            return

        # Рисуем линии между точками
        for i in range(len(self.points) - 1):
            start = (int(self.points[i][0]), int(self.points[i][1]))
            end = (int(self.points[i + 1][0]), int(self.points[i + 1][1]))
            pygame.draw.line(screen, color, start, end, line_width)

    def get_info(self) -> dict:
        """Получение информации о кривой."""
        return {"order": self.order, "points": len(self.points), "size": self.size}


class AnimatedPeanoCurve(PeanoCurve):
    """Анимированная версия кривой Пеано (строится постепенно)."""

    def __init__(self, x: int, y: int, size: int, order: int, animation_speed: float = 50):
        super().__init__(x, y, size, order)
        self.animation_speed = animation_speed  # точек в секунду
        self.current_point = 0
        self.animation_complete = False
        self.paused = False

    def update(self, delta_time: float) -> None:
        """Обновление анимации."""
        if self.paused or self.animation_complete:
            return

        # Добавляем новые точки в анимацию
        points_to_add = int(self.animation_speed * delta_time)
        self.current_point = min(self.current_point + points_to_add, len(self.points))

        if self.current_point >= len(self.points):
            self.animation_complete = True

    def draw(self, screen: pygame.Surface, color: tuple, line_width: int = 2) -> None:
        """Отрисовка анимированной кривой."""
        if self.current_point < 2:
            return

        # Рисуем только видимую часть кривой
        for i in range(min(self.current_point, len(self.points)) - 1):
            start = (int(self.points[i][0]), int(self.points[i][1]))
            end = (int(self.points[i + 1][0]), int(self.points[i + 1][1]))
            pygame.draw.line(screen, color, start, end, line_width)

    def reset_animation(self) -> None:
        """Сброс анимации."""
        self.current_point = 0
        self.animation_complete = False
        self.paused = False

    def toggle_pause(self) -> None:
        """Пауза/продолжение анимации."""
        self.paused = not self.paused

    def set_speed(self, speed: float) -> None:
        """Установка скорости анимации."""
        self.animation_speed = max(10, min(200, speed))
