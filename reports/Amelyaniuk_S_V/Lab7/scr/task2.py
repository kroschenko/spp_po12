"""Модуль с приложением для рисования фрактала Дерево Пифагора."""
import tkinter as tk
import math


def draw_pythagoras_tree(canvas, x, y, size, angle, depth):  # pylint: disable=R0913,R0917
    """Рекурсивно рисует дерево Пифагора на canvas.

    Args:
        canvas: Canvas для рисования.
        x, y: Координаты начальной точки.
        size: Размер квадрата.
        angle: Угол наклона.
        depth: Глубина рекурсии.
    """
    if depth == 0:
        return

    x1 = x + size * math.cos(angle)
    y1 = y - size * math.sin(angle)
    x2 = x1 + size * math.cos(angle + math.pi / 2)
    y2 = y1 - size * math.sin(angle + math.pi / 2)
    x3 = x + size * math.cos(angle + math.pi / 2)
    y3 = y - size * math.sin(angle + math.pi / 2)

    canvas.create_polygon(x, y, x1, y1, x2, y2, x3, y3, outline="green", fill="")

    new_size = size * math.sqrt(2) / 2
    draw_pythagoras_tree(canvas, x3, y3, new_size, angle + math.pi / 4, depth - 1)

    next_x = x3 + new_size * math.cos(angle + math.pi / 4)
    next_y = y3 - new_size * math.sin(angle + math.pi / 4)
    draw_pythagoras_tree(canvas, next_x, next_y, new_size, angle - math.pi / 4, depth - 1)


def start_draw(canvas, scale_depth):
    """Очищает canvas и рисует дерево Пифагора заданной глубины."""
    canvas.delete("all")
    depth = int(scale_depth.get())
    draw_pythagoras_tree(canvas, 250, 450, 80, 0, depth)


def create_application():
    """Создает и запускает приложение с фракталом."""
    root = tk.Tk()
    root.title("Лаба 7 - Фрактал (Дерево Пифагора)")

    canvas = tk.Canvas(root, width=600, height=500, bg="white")
    canvas.pack()

    ctrl = tk.Frame(root)
    ctrl.pack()

    tk.Label(ctrl, text="Глубина:").pack(side=tk.LEFT)
    scale_depth = tk.Scale(ctrl, from_=1, to=10, orient=tk.HORIZONTAL)
    scale_depth.set(5)
    scale_depth.pack(side=tk.LEFT)

    btn_draw = tk.Button(ctrl, text="Построить", command=lambda: start_draw(canvas, scale_depth))
    btn_draw.pack(side=tk.LEFT)

    root.mainloop()


if __name__ == "__main__":
    create_application()
