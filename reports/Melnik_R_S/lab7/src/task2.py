# pylint: disable=invalid-name, R0902, R0903, R0913, R0914, R0915, W0703, W0718, W0613, W0612, W0201, import-error, no-name-in-module
"""
Модуль для Лабораторной работы №7 (Задание 2).
Построение и визуализация фрактала "Остров Минковского".
"""

import os
import math
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab


class Task2App:
    """Класс графического приложения для построения фрактала."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ЛР 7 - Задание 2: Фрактал Остров Минковского")

        self.width = 600
        self.height = 600

        control_frame = tk.Frame(root, padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        tk.Label(control_frame, text="Глубина рекурсии:").pack(anchor=tk.W)
        self.ent_depth = tk.Entry(control_frame, width=8)
        self.ent_depth.pack(anchor=tk.W)
        self.ent_depth.insert(0, "3")

        tk.Label(control_frame, text="Цвет фрактала:").pack(anchor=tk.W, pady=(10, 0))
        self.ent_color = tk.Entry(control_frame, width=8)
        self.ent_color.pack(anchor=tk.W)
        self.ent_color.insert(0, "darkblue")

        tk.Button(control_frame, text="Построить", command=self.draw_fractal).pack(
            fill=tk.X, pady=15
        )

        tk.Button(control_frame, text="Скриншот", command=self.take_screenshot).pack(
            fill=tk.X, pady=5
        )

        self.draw_fractal()

    def generate_l_system(self, depth: int) -> str:
        """Генерирует строку команд L-системы для построения фрактала."""
        path = "F+F+F+F"
        rule = "F-F+F+FF-F-F+F"
        for _ in range(depth):
            path = path.replace("F", rule)
        return path

    def draw_fractal(self):
        """Вычисляет координаты фрактала и отрисовывает их на холсте."""
        try:
            depth = int(self.ent_depth.get())
            if depth < 0 or depth > 5:
                messagebox.showwarning(
                    "Внимание", "Глубина от 0 до 5, иначе будет зависание!"
                )
                return

            color = self.ent_color.get()
            self.canvas.delete("all")

            path = self.generate_l_system(depth)

            coords = [(0.0, 0.0)]
            cur_x, cur_y = 0.0, 0.0
            angle = 0.0

            for cmd in path:
                if cmd == "F":
                    cur_x += math.cos(angle)
                    cur_y += math.sin(angle)
                    coords.append((cur_x, cur_y))
                elif cmd == "+":
                    angle += math.pi / 2
                elif cmd == "-":
                    angle -= math.pi / 2

            min_x = min(c[0] for c in coords)
            max_x = max(c[0] for c in coords)
            min_y = min(c[1] for c in coords)
            max_y = max(c[1] for c in coords)

            fractal_w = max_x - min_x
            fractal_h = max_y - min_y

            padding = 40
            scale = min(
                (self.width - padding) / fractal_w, (self.height - padding) / fractal_h
            )

            offset_x = (self.width - fractal_w * scale) / 2 - min_x * scale
            offset_y = (self.height - fractal_h * scale) / 2 - min_y * scale

            screen_coords = []
            for cx, cy in coords:
                screen_coords.extend([cx * scale + offset_x, cy * scale + offset_y])

            self.canvas.create_line(*screen_coords, fill=color, width=1)

        except ValueError:
            messagebox.showerror("Ошибка", "Неверно заданы параметры")

    def take_screenshot(self):
        """Делает скриншот области холста и сохраняет в текущую директорию."""
        root_x = self.root.winfo_rootx() + self.canvas.winfo_x()
        root_y = self.root.winfo_rooty() + self.canvas.winfo_y()
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        try:
            img = ImageGrab.grab(
                bbox=(root_x, root_y, root_x + canvas_w, root_y + canvas_h)
            )
            time_str = datetime.datetime.now().strftime("%H%M%S")
            filename = f"screenshot_task2_{time_str}.png"
            img.save(filename)
            messagebox.showinfo(
                "Скриншот", f"Сохранено в директорию:\n{os.path.abspath(filename)}"
            )
        except Exception as err:
            messagebox.showerror("Ошибка скриншота", str(err))


if __name__ == "__main__":
    main_root = tk.Tk()
    app_window = Task2App(main_root)
    main_root.mainloop()
