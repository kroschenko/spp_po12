"""
Приложение для построения кривой Пеано.
"""

import sys
import os
from datetime import datetime

import pygame

from peano import AnimatedPeanoCurve

# Конфигурация
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (50, 50, 150)
PANEL_HEIGHT = 100
FPS = 60

# Параметры по умолчанию
DEFAULT_ORDER = 3
MAX_ORDER = 5
DEFAULT_SPEED = 80


class Button:
    """Класс кнопки."""

    def __init__(self, rect: pygame.Rect, text: str, color: tuple, hover_color: tuple):
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
        """Обработка событий кнопки."""
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
    """Класс ползунка."""

    def __init__(self, rect: pygame.Rect, min_val: float, max_val: float, initial_val: float):
        self.rect = rect
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.knob_radius = 8
        self.dragging = False
        self.font = pygame.font.Font(None, 20)

    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка ползунка."""
        pygame.draw.line(
            screen,
            (100, 100, 100),
            (self.rect.x, self.rect.centery),
            (self.rect.x + self.rect.width, self.rect.centery),
            3,
        )

        knob_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pygame.draw.circle(screen, (100, 100, 200), (int(knob_x), self.rect.centery), self.knob_radius)
        pygame.draw.circle(screen, (0, 0, 0), (int(knob_x), self.rect.centery), self.knob_radius, 2)

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


class PeanoApp:
    """Приложение для отображения кривой Пеано."""

    def __init__(self):
        """Инициализация приложения."""
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Кривая Пеано - Фрактал")
        self.clock = pygame.time.Clock()

        # Создаём папку для скриншотов
        self.screenshot_dir = "screenshots_peano"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

        # Параметры кривой
        margin = 50
        drawing_size = min(WINDOW_WIDTH - 2 * margin, WINDOW_HEIGHT - PANEL_HEIGHT - 2 * margin)
        self.drawing_x = (WINDOW_WIDTH - drawing_size) // 2
        self.drawing_y = margin

        # Создаём кривую (используем новый конструктор с одним аргументом position)
        self.curve = AnimatedPeanoCurve(
            (self.drawing_x, self.drawing_y),
            drawing_size,
            DEFAULT_ORDER,
            DEFAULT_SPEED
        )

        # Создаём элементы управления
        self.create_controls()

        # Переменные состояния
        self.running = True
        self.last_time = pygame.time.get_ticks()

    def create_controls(self):
        """Создание элементов управления."""
        panel_y = WINDOW_HEIGHT - PANEL_HEIGHT
        button_width = 100
        button_height = 40
        button_y = panel_y + (PANEL_HEIGHT - button_height) // 2

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

        self.order_down_button = Button(
            pygame.Rect(400, button_y, 40, button_height),
            "-",
            (200, 200, 200),
            (150, 150, 150)
        )

        self.order_up_button = Button(
            pygame.Rect(480, button_y, 40, button_height),
            "+",
            (200, 200, 200),
            (150, 150, 150)
        )

        self.speed_slider = Slider(
            pygame.Rect(560, panel_y + 20, 200, 30),
            10,
            200,
            DEFAULT_SPEED
        )

        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)

    def take_screenshot(self) -> None:
        """Сохранение скриншота."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"peano_screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        pygame.image.save(self.screen, filepath)
        print(f"Скриншот сохранён: {filepath}")

        flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        flash_surface.set_alpha(128)
        flash_surface.fill((255, 255, 255))
        self.screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)

    def regenerate_curve(self) -> None:
        """Перегенерация кривой с новыми параметрами."""
        self.curve = AnimatedPeanoCurve(
            (self.drawing_x, self.drawing_y),
            self.curve.size,
            self.curve.order,
            self.speed_slider.get_value(),
        )

    def change_order(self, delta: int) -> None:
        """Изменение порядка кривой."""
        new_order = self.curve.order + delta
        if 1 <= new_order <= MAX_ORDER:
            self.curve.order = new_order
            self.regenerate_curve()

    def _handle_key_events(self, event: pygame.event.Event) -> None:
        """Обработка событий клавиатуры."""
        if event.key == pygame.K_SPACE:
            self.curve.toggle_pause()
        elif event.key == pygame.K_r:
            self.curve.reset_animation()
        elif event.key == pygame.K_F12:
            self.take_screenshot()
        elif event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_UP:
            self.change_order(1)
        elif event.key == pygame.K_DOWN:
            self.change_order(-1)

    def _handle_button_events(self, event: pygame.event.Event) -> None:
        """Обработка событий кнопок."""
        if self.pause_button.handle_event(event):
            self.curve.toggle_pause()
        elif self.reset_button.handle_event(event):
            self.curve.reset_animation()
        elif self.screenshot_button.handle_event(event):
            self.take_screenshot()
        elif self.order_down_button.handle_event(event):
            self.change_order(-1)
        elif self.order_up_button.handle_event(event):
            self.change_order(1)

    def handle_events(self) -> None:
        """Обработка событий."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_key_events(event)

            self._handle_button_events(event)
            self.speed_slider.handle_event(event)

    def update(self, delta_time: float) -> None:
        """Обновление состояния."""
        self.curve.set_speed(self.speed_slider.get_value())
        self.curve.update(delta_time)

    def draw_control_panel(self) -> None:
        """Отрисовка панели управления."""
        panel_y = WINDOW_HEIGHT - PANEL_HEIGHT

        pygame.draw.rect(self.screen, (220, 220, 220), (0, panel_y, WINDOW_WIDTH, PANEL_HEIGHT))
        pygame.draw.line(self.screen, (0, 0, 0), (0, panel_y), (WINDOW_WIDTH, panel_y), 2)

        self.pause_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.screenshot_button.draw(self.screen)
        self.order_down_button.draw(self.screen)
        self.order_up_button.draw(self.screen)

        order_text = self.font.render(f"Порядок: {self.curve.order}", True, (0, 0, 0))
        self.screen.blit(order_text, (430, panel_y + 50))

        self.speed_slider.draw(self.screen)

        info = self.curve.get_info()
        info_y = panel_y + 10
        info_texts = [
            f"Точки: {info['points']}",
            f"Прогресс: {self.curve.current_point}/{info['points']}",
            f"Статус: {'Пауза' if self.curve.paused else 'Активен'}",
        ]

        for i, text in enumerate(info_texts):
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (780, info_y + i * 25))

        help_y = panel_y + 10
        help_texts = [
            "Управление:",
            "Space - Пауза",
            "R - Сброс анимации",
            "↑/↓ - Порядок",
            "F12 - Скриншот",
        ]

        small_font = pygame.font.Font(None, 16)
        for i, text in enumerate(help_texts):
            text_surface = small_font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, help_y + i * 18))

    def draw(self) -> None:
        """Отрисовка всех элементов."""
        self.screen.fill(BACKGROUND_COLOR)

        pygame.draw.rect(
            self.screen,
            (200, 200, 200),
            (self.drawing_x - 2, self.drawing_y - 2, self.curve.size + 4, self.curve.size + 4),
            2,
        )

        self.curve.draw(self.screen, LINE_COLOR, 2)

        title = self.title_font.render("Кривая Пеано (Пространственно-заполняющая кривая)", True, (0, 0, 0))
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 10))

        self.draw_control_panel()
        pygame.display.flip()

    def run(self) -> None:
        """Главный цикл приложения."""
        print("""
        ========================================
        Кривая Пеано - Фрактал
        Управление:
        Space - Пауза/Продолжить
        R - Сброс анимации
        ↑/↓ - Увеличить/уменьшить порядок
        F12 - Скриншот
        ESC - Выход
        ========================================
        """)

        while self.running:
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
    """Точка входа."""
    app = PeanoApp()
    app.run()


if __name__ == "__main__":
    main()
