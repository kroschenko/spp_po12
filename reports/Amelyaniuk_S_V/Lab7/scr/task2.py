import tkinter as tk
import math

def draw_pythagoras_tree(canvas, x, y, size, angle, depth):
    if depth == 0:
        return

    # Координаты квадрата
    x1 = x + size * math.cos(angle)
    y1 = y - size * math.sin(angle)
    x2 = x1 + size * math.cos(angle + math.pi/2)
    y2 = y1 - size * math.sin(angle + math.pi/2)
    x3 = x + size * math.cos(angle + math.pi/2)
    y3 = y - size * math.sin(angle + math.pi/2)

    canvas.create_polygon(x, y, x1, y1, x2, y2, x3, y3, outline="green", fill="")

    # Рекурсия для левой и правой ветвей (под 45 градусов)
    new_size = size * math.sqrt(2) / 2
    draw_pythagoras_tree(canvas, x3, y3, new_size, angle + math.pi/4, depth - 1)
    
    # Расчет новой точки старта для правой ветви
    next_x = x3 + new_size * math.cos(angle + math.pi/4)
    next_y = y3 - new_size * math.sin(angle + math.pi/4)
    draw_pythagoras_tree(canvas, next_x, next_y, new_size, angle - math.pi/4, depth - 1)

def start_draw():
    canvas_f.delete("all")
    depth = int(scale_depth.get())
    draw_pythagoras_tree(canvas_f, 250, 450, 80, 0, depth)

root_f = tk.Tk()
root_f.title("Лаба 7 - Фрактал (Дерево Пифагора)")

canvas_f = tk.Canvas(root_f, width=600, height=500, bg='white')
canvas_f.pack()

ctrl_f = tk.Frame(root_f)
ctrl_f.pack()

tk.Label(ctrl_f, text="Глубина:").pack(side=tk.LEFT)
scale_depth = tk.Scale(ctrl_f, from_=1, to=10, orient=tk.HORIZONTAL)
scale_depth.set(5)
scale_depth.pack(side=tk.LEFT)

btn_draw = tk.Button(ctrl_f, text="Построить", command=start_draw)
btn_draw.pack(side=tk.LEFT)

root_f.mainloop()