"""
Модуль для выполнения лабораторной работы №7.
Реализует оконное приложение на Tkinter с двумя заданиями:
1. Вращающийся отрезок, движущийся по другому отрезку.
2. Построение фрактала "Снежинка Коха".
Обеспечивает настройку параметров "на лету" и создание скриншотов.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
import os
from PIL import ImageGrab


class MovingRotatingLine:
    """Класс, описывающий математическую модель вращающегося отрезка."""

    def __init__(self, path_length, line_length):
        self.path_length = path_length
        self.line_length = line_length
        self.t = 0.0  # Параметр движения по отрезку (от 0 до 1)
        self.angle = 0.0  # Текущий угол поворота
        self.direction = 1  # Направление движения (1 - вперед, -1 - назад)

    def update(self, move_speed, rot_speed):
        """Обновляет состояние модели (координаты на отрезке и угол поворота)."""
        # Обновление позиции на пути
        self.t += (move_speed / 1000.0) * self.direction
        if self.t >= 1.0:
            self.t = 1.0
            self.direction = -1
        elif self.t <= 0.0:
            self.t = 0.0
            self.direction = 1

        # Обновление угла
        self.angle += rot_speed / 100.0

    def get_coords(self, c_x, c_y):
        """
        Вычисляет экранные координаты.
        Возвращает (x1, y1, x2, y2, p_x, p_y), где:
        x1...y2 - концы вращающегося отрезка, p_x, p_y - центр вращения.
        """
        # Координаты центра вращения (движется по горизонтальному отрезку)
        p_x = c_x - self.path_length / 2 + self.t * self.path_length
        p_y = c_y

        # Координаты концов вращающегося отрезка
        d_x = (self.line_length / 2) * math.cos(self.angle)
        d_y = (self.line_length / 2) * math.sin(self.angle)

        return p_x - d_x, p_y - d_y, p_x + d_x, p_y + d_y, p_x, p_y


class Task1Frame(ttk.Frame):
    """Фрейм для задания 1: Вращающийся отрезок."""

    # pylint: disable=too-many-ancestors, too-many-instance-attributes

    def __init__(self, parent):
        super().__init__(parent)
        self.is_paused = False

        # Настройки модели
        self.model = MovingRotatingLine(path_length=400, line_length=150)

        # Объявление атрибутов интерфейса
        self.move_speed = None
        self.rot_speed = None
        self.line_len = None
        self.btn_pause = None
        self.btn_screen = None
        self.canvas = None

        self.setup_ui()
        self.animate()

    def setup_ui(self):
        """Создает и размещает элементы управления на фрейме."""
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(control_frame, text="Скорость движения:").pack(pady=(10, 0))
        self.move_speed = tk.Scale(control_frame, from_=0, to=50, orient=tk.HORIZONTAL)
        self.move_speed.set(15)
        self.move_speed.pack()

        ttk.Label(control_frame, text="Скорость вращения:").pack(pady=(10, 0))
        self.rot_speed = tk.Scale(control_frame, from_=0, to=50, orient=tk.HORIZONTAL)
        self.rot_speed.set(10)
        self.rot_speed.pack()

        ttk.Label(control_frame, text="Длина отрезка:").pack(pady=(10, 0))
        self.line_len = tk.Scale(
            control_frame,
            from_=50,
            to=300,
            orient=tk.HORIZONTAL,
            command=self.update_params,
        )
        self.line_len.set(150)
        self.line_len.pack()

        self.btn_pause = ttk.Button(
            control_frame, text="Пауза", command=self.toggle_pause
        )
        self.btn_pause.pack(pady=20)

        self.btn_screen = ttk.Button(
            control_frame, text="Скриншот", command=self.take_screenshot
        )
        self.btn_screen.pack(pady=5)

        self.canvas = tk.Canvas(self, bg="white", width=600, height=500)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_params(self, _event=None):
        """Обновляет параметры модели при изменении ползунков."""
        self.model.line_length = self.line_len.get()

    def toggle_pause(self):
        """Ставит анимацию на паузу или возобновляет ее."""
        self.is_paused = not self.is_paused
        self.btn_pause.config(text="Возобновить" if self.is_paused else "Пауза")

    def animate(self):
        """Основной цикл отрисовки анимации."""
        if not self.is_paused:
            self.canvas.delete("all")

            # Размеры холста
            c_x = int(self.canvas.winfo_width() / 2)
            c_y = int(self.canvas.winfo_height() / 2)
            if c_x <= 1:
                c_x, c_y = 300, 250  # Дефолт до отрисовки

            # Рисуем путь (траекторию)
            path_l = self.model.path_length
            self.canvas.create_line(
                c_x - path_l / 2, c_y, c_x + path_l / 2, c_y, dash=(4, 4), fill="gray"
            )

            # Обновляем модель
            self.model.update(self.move_speed.get(), self.rot_speed.get())
            x_1, y_1, x_2, y_2, p_x, p_y = self.model.get_coords(c_x, c_y)

            # Рисуем вращающийся отрезок и точку-центр
            self.canvas.create_line(x_1, y_1, x_2, y_2, width=3, fill="blue")
            self.canvas.create_oval(p_x - 4, p_y - 4, p_x + 4, p_y + 4, fill="red")

        self.after(30, self.animate)  # 30 мс ~ 33 FPS

    def take_screenshot(self):
        """Вызывает общую функцию сохранения скриншота для первого задания."""
        take_canvas_screenshot(self.canvas, "task1_rot_line")


def calculate_koch_points(point1, point2, depth):
    """Рекурсивно вычисляет точки для фрактала 'Снежинка Коха'."""
    if depth == 0:
        return [point1, point2]

    x_1, y_1 = point1
    x_2, y_2 = point2

    # Точки, делящие отрезок на 3 части
    x_a = x_1 + (x_2 - x_1) / 3
    y_a = y_1 + (y_2 - y_1) / 3
    x_c = x_1 + (x_2 - x_1) * 2 / 3
    y_c = y_1 + (y_2 - y_1) * 2 / 3

    # Вершина треугольника (поворот вектора на 60 градусов)
    angle = -math.pi / 3  # минус, т.к. ось Y в Canvas направлена вниз
    x_b = x_a + (x_c - x_a) * math.cos(angle) - (y_c - y_a) * math.sin(angle)
    y_b = y_a + (x_c - x_a) * math.sin(angle) + (y_c - y_a) * math.cos(angle)

    # Рекурсивный вызов для 4 новых отрезков
    pts = []
    pts.extend(calculate_koch_points((x_1, y_1), (x_a, y_a), depth - 1)[:-1])
    pts.extend(calculate_koch_points((x_a, y_a), (x_b, y_b), depth - 1)[:-1])
    pts.extend(calculate_koch_points((x_b, y_b), (x_c, y_c), depth - 1)[:-1])
    pts.extend(calculate_koch_points((x_c, y_c), (x_2, y_2), depth - 1))

    return pts


class Task2Frame(ttk.Frame):
    """Фрейм для задания 2: Снежинка Коха."""

    # pylint: disable=too-many-ancestors

    def __init__(self, parent):
        super().__init__(parent)

        self.depth_scale = None
        self.size_scale = None
        self.btn_screen = None
        self.canvas = None

        self.setup_ui()
        self.after(100, self.draw_fractal)

    def setup_ui(self):
        """Создает и размещает элементы управления на фрейме."""
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(control_frame, text="Глубина рекурсии:").pack(pady=(10, 0))
        self.depth_scale = tk.Scale(
            control_frame,
            from_=0,
            to=6,
            orient=tk.HORIZONTAL,
            command=self.draw_fractal,
        )
        self.depth_scale.set(3)
        self.depth_scale.pack()

        ttk.Label(control_frame, text="Размер (масштаб):").pack(pady=(10, 0))
        self.size_scale = tk.Scale(
            control_frame,
            from_=100,
            to=500,
            orient=tk.HORIZONTAL,
            command=self.draw_fractal,
        )
        self.size_scale.set(300)
        self.size_scale.pack()

        self.btn_screen = ttk.Button(
            control_frame, text="Скриншот", command=self.take_screenshot
        )
        self.btn_screen.pack(pady=20)

        self.canvas = tk.Canvas(self, bg="white", width=600, height=500)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def draw_fractal(self, _event=None):
        """Отрисовывает фрактал на холсте на основе заданных параметров."""
        self.canvas.delete("all")
        depth = self.depth_scale.get()
        size = self.size_scale.get()

        c_x = int(self.canvas.winfo_width() / 2)
        c_y = int(self.canvas.winfo_height() / 2)
        if c_x <= 1:
            c_x, c_y = 300, 250

        # Расчет вершин равностороннего треугольника
        height = size * math.sqrt(3) / 2
        p_1 = (c_x - size / 2, c_y + height / 3)
        p_2 = (c_x, c_y - 2 * height / 3)
        p_3 = (c_x + size / 2, c_y + height / 3)

        # Получаем все точки для 3 сторон
        points = []
        points.extend(calculate_koch_points(p_1, p_2, depth)[:-1])
        points.extend(calculate_koch_points(p_2, p_3, depth)[:-1])
        points.extend(calculate_koch_points(p_3, p_1, depth))

        # Отрисовка
        flat_points = [coord for pt in points for coord in pt]
        self.canvas.create_polygon(
            flat_points, outline="cyan", fill="darkblue", width=1.5
        )

    def take_screenshot(self):
        """Вызывает общую функцию сохранения скриншота для второго задания."""
        take_canvas_screenshot(self.canvas, "task2_koch_snowflake")


def take_canvas_screenshot(canvas, prefix):
    """Делает скриншот области холста и сохраняет в текущую директорию."""
    canvas.update()

    x_pos = canvas.winfo_rootx()
    y_pos = canvas.winfo_rooty()
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    try:
        img = ImageGrab.grab(bbox=(x_pos, y_pos, x_pos + width, y_pos + height))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = os.path.join(os.getcwd(), filename)

        img.save(filepath)
        messagebox.showinfo(
            "Скриншот сохранен", f"Скриншот успешно сохранен:\n{filepath}"
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        messagebox.showerror("Ошибка", f"Не удалось сделать скриншот:\n{error}")


class MainApp(tk.Tk):
    """Главный класс приложения."""

    # pylint: disable=too-many-ancestors

    def __init__(self):
        super().__init__()
        self.title("Лабораторная работа №7 (Вариант 7)")
        self.geometry("850x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = Task1Frame(self.notebook)
        self.notebook.add(self.tab1, text="Задание 1: Вращающийся отрезок")

        self.tab2 = Task2Frame(self.notebook)
        self.notebook.add(self.tab2, text="Задание 2: Снежинка Коха")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
