"""
Лабораторная работа №7
"""

import math
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from dataclasses import dataclass
from PIL import ImageGrab


@dataclass
class Point:
    """Класс для представления точки на плоскости."""

    x: float
    y: float

    def to_tuple(self):
        """Возвращает координаты в виде кортежа."""
        return self.x, self.y


class Triangle:
    """Класс треугольника с методами вращения и отрисовки."""

    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = [p1, p2, p3]

    def get_centroid(self) -> Point:
        """Вычисляет центр тяжести треугольника."""
        cx = sum(p.x for p in self.points) / 3
        cy = sum(p.y for p in self.points) / 3
        return Point(cx, cy)

    def rotate(self, angle_deg: float):
        """Вращает треугольник вокруг его центра тяжести."""
        centroid = self.get_centroid()
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        new_points = []
        for p in self.points:
            # Смещение к началу координат (относительно центра)
            tx_val, ty_val = p.x - centroid.x, p.y - centroid.y
            # Поворот
            rx_val = tx_val * cos_a - ty_val * sin_a
            ry_val = tx_val * sin_a + ty_val * cos_a
            # Обратное смещение
            new_points.append(Point(rx_val + centroid.x, ry_val + centroid.y))
        self.points = new_points


class App(tk.Tk):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()
        self.title("Лабораторная работа №7 - Крощенко А.А.")
        self.geometry("1000x700")

        # Состояние анимации
        self.is_running = False
        self.angle_step = 2.0
        self.triangle = Triangle(Point(100, 100), Point(250, 150), Point(150, 300))
        self.peano_points = []

        # Элементы интерфейса
        self.canvas = None
        self.speed_scale = None
        self.depth_entry = None

        self.setup_ui()

    def setup_ui(self):
        """Создание элементов интерфейса."""
        control_panel = tk.Frame(self, width=250, bg="#f0f0f0")
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(
            control_panel, text="Задание 1: Треугольник", font=("Arial", 10, "bold")
        ).pack()
        tk.Button(
            control_panel, text="Старт/Пауза", command=self.toggle_animation
        ).pack(fill=tk.X)

        tk.Label(control_panel, text="Скорость вращения:").pack()
        self.speed_scale = tk.Scale(control_panel, from_=0, to=20, orient=tk.HORIZONTAL)
        self.speed_scale.set(2)
        self.speed_scale.pack(fill=tk.X)

        tk.Label(
            control_panel, text="\nЗадание 2: Кривая Пеано", font=("Arial", 10, "bold")
        ).pack()
        tk.Label(control_panel, text="Глубина рекурсии:").pack()
        self.depth_entry = tk.Entry(control_panel)
        self.depth_entry.insert(0, "3")
        self.depth_entry.pack(fill=tk.X)
        tk.Button(
            control_panel, text="Нарисовать Пеано", command=self.draw_peano_fractal
        ).pack(fill=tk.X)

        tk.Label(control_panel, text="\nОпции:").pack()
        tk.Button(control_panel, text="Скриншот", command=self.take_screenshot).pack(
            fill=tk.X
        )
        tk.Button(control_panel, text="Очистить", command=self.clear_canvas).pack(
            fill=tk.X
        )

        self.canvas = tk.Canvas(
            self, bg="white", highlightthickness=1, highlightbackground="black"
        )
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

    def toggle_animation(self):
        """Запуск и остановка анимации."""
        self.is_running = not self.is_running
        if self.is_running:
            self.animate_triangle()

    def animate_triangle(self):
        """Цикл анимации вращения."""
        if not self.is_running:
            return

        self.canvas.delete("triangle")
        self.angle_step = self.speed_scale.get()
        self.triangle.rotate(self.angle_step)

        coords = []
        for p in self.triangle.points:
            coords.extend([p.x, p.y])

        self.canvas.create_polygon(
            coords, outline="blue", fill="lightblue", tags="triangle", width=2
        )
        self.after(20, self.animate_triangle)

    def draw_peano_fractal(self):
        """Подготовка к отрисовке кривой Пеано."""
        self.is_running = False
        self.clear_canvas()
        try:
            depth = int(self.depth_entry.get())
            if depth > 5:
                messagebox.showwarning(
                    "Внимание", "Глубина > 5 может замедлить систему"
                )

            padding = 50
            size = (
                min(self.canvas.winfo_width(), self.canvas.winfo_height()) - 2 * padding
            )
            self.peano_points = []
            self._generate_peano(padding, padding, size, depth)
            self._render_curve()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")

    def _generate_peano(self, x_pos, y_pos, size, depth):
        """Рекурсивный алгоритм генерации точек кривой Пеано."""
        if depth == 0:
            self.peano_points.append((x_pos + size / 2, y_pos + size / 2))
            return

        new_size = size / 3
        for i in range(3):
            # Зигзагообразный порядок обхода для непрерывности
            row = i
            for j in range(3):
                col = j if i % 2 == 0 else 2 - j
                self._generate_peano(
                    x_pos + col * new_size, y_pos + row * new_size, new_size, depth - 1
                )

    def _render_curve(self):
        """Отрисовка накопленных точек."""
        if len(self.peano_points) < 2:
            return
        for i in range(len(self.peano_points) - 1):
            p1_val = self.peano_points[i]
            p2_val = self.peano_points[i + 1]
            self.canvas.create_line(
                p1_val[0], p1_val[1], p2_val[0], p2_val[1], fill="red"
            )

    def take_screenshot(self):
        """Сохранение скриншота области холста."""
        x_root = self.winfo_rootx() + self.canvas.winfo_x()
        y_root = self.winfo_rooty() + self.canvas.winfo_y()
        x_end = x_root + self.canvas.winfo_width()
        y_end = y_root + self.canvas.winfo_height()

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{now}.png"
        ImageGrab.grab().crop((x_root, y_root, x_end, y_end)).save(filename)
        messagebox.showinfo("Успех", f"Скриншот сохранен как {filename}")

    def clear_canvas(self):
        """Очистка холста."""
        self.canvas.delete("all")


if __name__ == "__main__":
    app = App()
    app.mainloop()
