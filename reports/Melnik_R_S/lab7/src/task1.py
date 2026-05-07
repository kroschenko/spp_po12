# pylint: disable=invalid-name, R0902, R0903, R0913, R0914, R0915, W0703, W0718, W0613, W0612, W0201, import-error, no-name-in-module
"""
Модуль для Лабораторной работы №7 (Задание 1).
Визуализация движущихся точек и их разделение прямой линией.
"""

import os
import random
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab


class Point:
    """Класс для представления движущейся точки."""

    def __init__(self, x: float, y: float, dx: float, dy: float):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


class Line:
    """Класс для представления разделяющей прямой линии."""

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_side(self, p: Point) -> float:
        """Определяет, с какой стороны от линии находится точка."""
        return (p.x - self.x1) * (self.y2 - self.y1) - (p.y - self.y1) * (
            self.x2 - self.x1
        )


class Task1App:
    """Главный класс графического приложения (Задание 1)."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ЛР 7 - Задание 1: Точки и Линия")

        self.width = 600
        self.height = 400
        self.points = []
        self.is_paused = False

        control_frame = tk.Frame(root, padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        tk.Label(control_frame, text="Линия X1, Y1:").pack(anchor=tk.W)
        self.ent_x1 = tk.Entry(control_frame, width=8)
        self.ent_x1.pack(anchor=tk.W)
        self.ent_x1.insert(0, "100")

        self.ent_y1 = tk.Entry(control_frame, width=8)
        self.ent_y1.pack(anchor=tk.W)
        self.ent_y1.insert(0, "300")

        tk.Label(control_frame, text="Линия X2, Y2:").pack(anchor=tk.W)
        self.ent_x2 = tk.Entry(control_frame, width=8)
        self.ent_x2.pack(anchor=tk.W)
        self.ent_x2.insert(0, "500")

        self.ent_y2 = tk.Entry(control_frame, width=8)
        self.ent_y2.pack(anchor=tk.W)
        self.ent_y2.insert(0, "100")

        tk.Label(control_frame, text="Кол-во точек N:").pack(anchor=tk.W, pady=(10, 0))
        self.ent_n = tk.Entry(control_frame, width=8)
        self.ent_n.pack(anchor=tk.W)
        self.ent_n.insert(0, "100")

        tk.Button(
            control_frame, text="Применить параметры", command=self.apply_params
        ).pack(fill=tk.X, pady=5)

        tk.Label(control_frame, text="Скорость:").pack(anchor=tk.W, pady=(10, 0))
        self.speed_scale = tk.Scale(
            control_frame, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL
        )
        self.speed_scale.set(1.0)
        self.speed_scale.pack(fill=tk.X)

        self.btn_pause = tk.Button(
            control_frame, text="Пауза", command=self.toggle_pause
        )
        self.btn_pause.pack(fill=tk.X, pady=5)

        tk.Button(control_frame, text="Скриншот", command=self.take_screenshot).pack(
            fill=tk.X, pady=5
        )

        self.line = Line(100, 300, 500, 100)
        self.apply_params()
        self.update_animation()

    def apply_params(self):
        """Считывает параметры из полей ввода и применяет их 'на лету'."""
        try:
            x1 = float(self.ent_x1.get())
            y1 = float(self.ent_y1.get())
            x2 = float(self.ent_x2.get())
            y2 = float(self.ent_y2.get())
            self.line = Line(x1, y1, x2, y2)

            n = int(self.ent_n.get())
            if len(self.points) != n:
                self.points = []
                for _ in range(n):
                    px = random.randint(10, self.width - 10)
                    py = random.randint(10, self.height - 10)
                    dx = random.choice([-1, 1]) * random.random() * 2
                    dy = random.choice([-1, 1]) * random.random() * 2
                    self.points.append(Point(px, py, dx, dy))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")

    def toggle_pause(self):
        """Переключает состояние паузы для анимации."""
        self.is_paused = not self.is_paused
        self.btn_pause.config(text="Возобновить" if self.is_paused else "Пауза")

    def take_screenshot(self):
        """Делает скриншот области холста и сохраняет в файл."""
        root_x = self.root.winfo_rootx() + self.canvas.winfo_x()
        root_y = self.root.winfo_rooty() + self.canvas.winfo_y()
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        try:
            img = ImageGrab.grab(
                bbox=(root_x, root_y, root_x + canvas_w, root_y + canvas_h)
            )
            time_str = datetime.datetime.now().strftime("%H%M%S")
            filename = f"screenshot_task1_{time_str}.png"
            img.save(filename)
            messagebox.showinfo(
                "Скриншот", f"Сохранено в директорию:\n{os.path.abspath(filename)}"
            )
        except Exception as err:
            messagebox.showerror("Ошибка скриншота", str(err))

    def update_animation(self):
        """Обновляет положение точек и перерисовывает холст."""
        if not self.is_paused:
            speed = self.speed_scale.get()
            self.canvas.delete("all")

            self.canvas.create_line(
                self.line.x1,
                self.line.y1,
                self.line.x2,
                self.line.y2,
                fill="black",
                width=3,
            )

            for p in self.points:
                p.x += p.dx * speed
                p.y += p.dy * speed

                if p.x < 0 or p.x > self.width:
                    p.dx *= -1
                if p.y < 0 or p.y > self.height:
                    p.dy *= -1

                side = self.line.get_side(p)
                if side > 0:
                    color = "blue"
                elif side < 0:
                    color = "red"
                else:
                    color = "green"

                self.canvas.create_oval(
                    p.x - 3, p.y - 3, p.x + 3, p.y + 3, fill=color, outline=""
                )

        self.root.after(20, self.update_animation)


if __name__ == "__main__":
    main_root = tk.Tk()
    app_window = Task1App(main_root)
    main_root.mainloop()
